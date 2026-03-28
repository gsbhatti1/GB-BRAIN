"""
GB-BRAIN — Runtime Policy
==========================
Lane-based trading policy system.
Each lane = one symbol + one strategy + one broker.
Policy controls: enabled/disabled, max_trades_per_day, max_position_pct,
required_status (candidate/confirmed), session_filter, cooldown_minutes.

Lanes:
  MANUAL-SIGNALS  → Webhook-driven, any broker, no session filter
  GB-INDICES      → Parallax/Cipher on NAS100/US30/SPX via OANDA
  GB-CRYPTO-BOT   → Parallax/Cipher on BTC/ETH/SOL via BloFin

Usage:
    from runtime.runtime_policy import RuntimePolicy, get_lane
    policy = RuntimePolicy()
    lane = policy.get_lane("GB-INDICES", "NAS100", "parallax")
    if policy.can_trade(lane):
        ...

Conventions:
    - SQLite is truth — trade state tracked externally in db/gb_brain.db
    - Capital is priority — max_position_pct hard ceiling enforced here
    - .env for secrets — broker credentials never stored in policy
    - Deterministic — same lane key always returns same Lane object
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional

logger = logging.getLogger("gb_brain.policy")

# ---------------------------------------------------------------------------
# ROOT path (project root = two levels up from this file)
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# Dataclass
# ---------------------------------------------------------------------------

@dataclass
class Lane:
    """Represents a single trading lane: symbol × strategy × broker tuple."""

    lane_name: str
    symbol: str
    strategy: str
    broker: str
    enabled: bool
    max_trades_per_day: int
    max_position_pct: float
    required_status: str = "candidate"
    session_filter: list = field(default_factory=list)   # e.g. ["NY"] or [] for always-on
    cooldown_minutes: int = 30
    notes: str = ""

    @property
    def key(self) -> str:
        """Canonical lookup key: lane_name:symbol:strategy (lowercase)."""
        return f"{self.lane_name}:{self.symbol}:{self.strategy}".lower()

    def __repr__(self) -> str:  # pragma: no cover
        sessions = ",".join(self.session_filter) if self.session_filter else "always"
        status_icon = "✓" if self.enabled else "✗"
        return (
            f"Lane({status_icon} {self.lane_name} | {self.symbol} | {self.strategy} | "
            f"{self.broker} | max={self.max_trades_per_day}/day | "
            f"pos≤{self.max_position_pct:.0%} | session={sessions})"
        )


# ---------------------------------------------------------------------------
# Default LANES definition
# ---------------------------------------------------------------------------
# Format: (lane_name, symbol, strategy, broker, enabled, max_trades_per_day,
#           max_position_pct, required_status, session_filter, cooldown_minutes, notes)

_LANE_DEFS: list[tuple] = [
    # ── MANUAL-SIGNALS ──────────────────────────────────────────────────────
    # Webhook-driven manual signals — any broker, no session restriction
    ("MANUAL-SIGNALS", "ANY",    "manual",   "any",    True,  5,  0.10, "candidate", [],     0,  "Webhook-driven manual signals"),
    ("MANUAL-SIGNALS", "US30",   "manual",   "any",    True,  5,  0.10, "candidate", [],     0,  "Manual US30 override"),
    ("MANUAL-SIGNALS", "NAS100", "manual",   "any",    True,  5,  0.10, "candidate", [],     0,  "Manual NAS100 override"),
    ("MANUAL-SIGNALS", "SPX500", "manual",   "any",    True,  5,  0.10, "candidate", [],     0,  "Manual SPX500 override"),
    ("MANUAL-SIGNALS", "BTC",    "manual",   "any",    True,  5,  0.10, "candidate", [],     0,  "Manual BTC override"),
    ("MANUAL-SIGNALS", "ETH",    "manual",   "any",    True,  5,  0.10, "candidate", [],     0,  "Manual ETH override"),
    ("MANUAL-SIGNALS", "SOL",    "manual",   "any",    True,  5,  0.10, "candidate", [],     0,  "Manual SOL override"),

    # ── GB-INDICES — OANDA, NY session ──────────────────────────────────────
    ("GB-INDICES",     "US30",   "parallax", "oanda",  True,  6,  0.08, "candidate", ["NY"], 30, "Parallax trend on US30"),
    ("GB-INDICES",     "US30",   "cipher",   "oanda",  True,  6,  0.08, "candidate", ["NY"], 30, "Cipher momentum on US30"),
    ("GB-INDICES",     "NAS100", "parallax", "oanda",  True,  6,  0.08, "candidate", ["NY"], 30, "Parallax trend on NAS100"),
    ("GB-INDICES",     "NAS100", "cipher",   "oanda",  True,  6,  0.08, "candidate", ["NY"], 30, "Cipher momentum on NAS100"),
    ("GB-INDICES",     "SPX500", "parallax", "oanda",  True,  6,  0.08, "candidate", ["NY"], 30, "Parallax trend on SPX500"),
    ("GB-INDICES",     "SPX500", "cipher",   "oanda",  True,  6,  0.08, "candidate", ["NY"], 30, "Cipher momentum on SPX500"),

    # ── GB-CRYPTO-BOT — BloFin, always-on (24/7 market) ─────────────────────
    ("GB-CRYPTO-BOT",  "BTC",    "parallax", "blofin", True,  8,  0.06, "candidate", [],     20, "Parallax trend on BTC"),
    ("GB-CRYPTO-BOT",  "BTC",    "cipher",   "blofin", True,  8,  0.06, "candidate", [],     20, "Cipher momentum on BTC"),
    ("GB-CRYPTO-BOT",  "ETH",    "parallax", "blofin", True,  8,  0.06, "candidate", [],     20, "Parallax trend on ETH"),
    ("GB-CRYPTO-BOT",  "ETH",    "cipher",   "blofin", True,  8,  0.06, "candidate", [],     20, "Cipher momentum on ETH"),
    ("GB-CRYPTO-BOT",  "SOL",    "parallax", "blofin", True,  8,  0.06, "candidate", [],     20, "Parallax trend on SOL"),
    ("GB-CRYPTO-BOT",  "SOL",    "cipher",   "blofin", True,  8,  0.06, "candidate", [],     20, "Cipher momentum on SOL"),
]


def _build_lanes() -> dict[str, Lane]:
    """Construct the default LANES dict keyed by Lane.key."""
    lanes: dict[str, Lane] = {}
    for (lane_name, symbol, strategy, broker, enabled,
         max_trades, max_pos_pct, req_status, session, cooldown, notes) in _LANE_DEFS:
        lane = Lane(
            lane_name=lane_name,
            symbol=symbol,
            strategy=strategy,
            broker=broker,
            enabled=enabled,
            max_trades_per_day=max_trades,
            max_position_pct=max_pos_pct,
            required_status=req_status,
            session_filter=session,
            cooldown_minutes=cooldown,
            notes=notes,
        )
        lanes[lane.key] = lane
    return lanes


# Module-level default — immutable after import
LANES: dict[str, Lane] = _build_lanes()


# ---------------------------------------------------------------------------
# RuntimePolicy class
# ---------------------------------------------------------------------------

class RuntimePolicy:
    """
    Lane-based trading policy manager.

    Manages which symbol × strategy × broker combinations are active,
    enforces per-lane trade limits, and supports JSON override files for
    runtime configuration without code changes.

    Examples
    --------
    >>> policy = RuntimePolicy()
    >>> lane = policy.get_lane("GB-INDICES", "NAS100", "parallax")
    >>> policy.can_trade(lane, trades_today=2)
    True
    """

    def __init__(self) -> None:
        # Deep-copy the module-level LANES so instances are independent
        self._lanes: dict[str, Lane] = {k: Lane(**asdict(v)) for k, v in LANES.items()}
        logger.debug("RuntimePolicy initialised with %d lanes.", len(self._lanes))

    # ------------------------------------------------------------------
    # Lookup
    # ------------------------------------------------------------------

    def get_lane(
        self,
        lane_name: str,
        symbol: str,
        strategy: str,
    ) -> Optional[Lane]:
        """
        Return the Lane for the given (lane_name, symbol, strategy) triple,
        or None if not found.

        Parameters
        ----------
        lane_name : str  e.g. "GB-INDICES"
        symbol    : str  e.g. "NAS100"
        strategy  : str  e.g. "parallax"
        """
        key = f"{lane_name}:{symbol}:{strategy}".lower()
        lane = self._lanes.get(key)
        if lane is None:
            logger.debug("get_lane: no lane found for key '%s'.", key)
        return lane

    # ------------------------------------------------------------------
    # Guard
    # ------------------------------------------------------------------

    def can_trade(self, lane: Optional[Lane], trades_today: int = 0) -> bool:
        """
        Return True if trading is permitted on this lane right now.

        Checks:
          1. lane is not None
          2. lane.enabled is True
          3. trades_today < lane.max_trades_per_day

        Note: session window enforcement is handled by LiveObserver._should_run_now().

        Parameters
        ----------
        lane        : Lane | None
        trades_today: int — number of completed trades today on this lane
        """
        if lane is None:
            logger.debug("can_trade: lane is None — blocked.")
            return False
        if not lane.enabled:
            logger.debug("can_trade: lane '%s' is disabled.", lane.key)
            return False
        if trades_today >= lane.max_trades_per_day:
            logger.debug(
                "can_trade: lane '%s' daily limit reached (%d/%d).",
                lane.key, trades_today, lane.max_trades_per_day,
            )
            return False
        return True

    # ------------------------------------------------------------------
    # Listings
    # ------------------------------------------------------------------

    def all_lanes(self) -> list[Lane]:
        """Return all Lane objects (enabled and disabled)."""
        return list(self._lanes.values())

    def enabled_lanes(self) -> list[Lane]:
        """Return only enabled Lane objects."""
        return [lane for lane in self._lanes.values() if lane.enabled]

    # ------------------------------------------------------------------
    # Serialisation
    # ------------------------------------------------------------------

    def save_overrides(self, path: str | Path) -> None:
        """
        Serialize current policy state to a JSON file.

        The file can later be loaded via load_overrides() to restore or
        share non-default configurations.

        Parameters
        ----------
        path : str | Path — destination file path
        """
        out_path = Path(path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {k: asdict(v) for k, v in self._lanes.items()}
        with open(out_path, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2)
        logger.info("Policy overrides saved to %s (%d lanes).", out_path, len(payload))

    def load_overrides(self, path: str | Path) -> None:
        """
        Load a JSON override file and merge into the current policy.

        Only fields present in the JSON are overwritten; lanes not in
        the file remain unchanged. New lanes in the file are added.

        Parameters
        ----------
        path : str | Path — source JSON file path
        """
        in_path = Path(path)
        if not in_path.exists():
            logger.warning("load_overrides: file not found: %s — skipping.", in_path)
            return
        with open(in_path, "r", encoding="utf-8") as fh:
            raw: dict = json.load(fh)
        merged = 0
        for key, lane_dict in raw.items():
            if key in self._lanes:
                # Merge: update only fields present in the override
                existing = asdict(self._lanes[key])
                existing.update(lane_dict)
                self._lanes[key] = Lane(**existing)
            else:
                # New lane from override file
                self._lanes[key] = Lane(**lane_dict)
            merged += 1
        logger.info("Loaded overrides from %s — %d lanes merged.", in_path, merged)

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------

    def __repr__(self) -> str:  # pragma: no cover
        header = f"RuntimePolicy ({len(self._lanes)} lanes)\n"
        sep = "-" * 90 + "\n"
        col = f"{'LANE':<18} {'SYMBOL':<10} {'STRATEGY':<12} {'BROKER':<10} {'ON':<5} {'MAX/DAY':<9} {'MAX_POS%':<10} {'SESSION'}\n"
        rows = []
        for lane in sorted(self._lanes.values(), key=lambda l: (l.lane_name, l.symbol, l.strategy)):
            sessions = ",".join(lane.session_filter) if lane.session_filter else "always"
            rows.append(
                f"{lane.lane_name:<18} {lane.symbol:<10} {lane.strategy:<12} "
                f"{lane.broker:<10} {'Y' if lane.enabled else 'N':<5} "
                f"{lane.max_trades_per_day:<9} {lane.max_position_pct * 100:.0f}%{'':<7} {sessions}"
            )
        return header + sep + col + sep + "\n".join(rows) + "\n" + sep


# ---------------------------------------------------------------------------
# Module-level convenience wrapper
# ---------------------------------------------------------------------------

_default_policy: Optional[RuntimePolicy] = None


def get_lane(lane_name: str, symbol: str, strategy: str) -> Optional[Lane]:
    """
    Module-level shortcut using a shared default RuntimePolicy instance.

    Examples
    --------
    >>> from runtime.runtime_policy import get_lane
    >>> lane = get_lane("GB-INDICES", "NAS100", "parallax")
    """
    global _default_policy
    if _default_policy is None:
        _default_policy = RuntimePolicy()
    return _default_policy.get_lane(lane_name, symbol, strategy)
