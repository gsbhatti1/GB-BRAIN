"""
GB-BRAIN — Capital Allocator (Phase 9)
========================================
Controls how much capital is allocated to each lane.
Implements micro-size-first rollout strategy.

Rollout stages:
  Stage 0: Paper only (0% real capital)
  Stage 1: Micro live (0.5% per trade, 1 symbol, 1 bot)
  Stage 2: Small live (1% per trade, 2 symbols, 2 bots)
  Stage 3: Normal live (2% per trade, all confirmed lanes)
  Stage 4: Full (2-5% per trade, dynamic sizing)

Usage:
    from runtime.capital_allocator import CapitalAllocator
    allocator = CapitalAllocator(stage=1)
    size = allocator.get_position_size(symbol="ETH", balance=5000, risk_pts=50)
    if allocator.can_add_position(symbol):
        ...
"""

import json
import logging
import sys
from enum import IntEnum
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv

load_dotenv(ROOT / ".env")

logger = logging.getLogger("gb_brain.capital_allocator")

KILL_SWITCH_PATH = ROOT / "db" / "kill_switch.json"

# ---------------------------------------------------------------------------
# Allocation stage enum
# ---------------------------------------------------------------------------
class AllocationStage(IntEnum):
    PAPER  = 0  # 0% real capital — paper only
    MICRO  = 1  # 0.5% per trade, max 1 symbol, max 1 open position
    SMALL  = 2  # 1.0% per trade, max 2 symbols, max 2 open positions
    NORMAL = 3  # 2.0% per trade, all confirmed lanes, max 5 positions
    FULL   = 4  # 2–5% per trade, dynamic sizing, max 10 positions


# ---------------------------------------------------------------------------
# Per-stage configuration
# ---------------------------------------------------------------------------
STAGE_LIMITS: dict[AllocationStage, dict] = {
    AllocationStage.PAPER: {
        "risk_pct":          0.0,
        "max_positions":     0,
        "max_symbols":       0,
        "max_daily_loss_pct": 0.0,
        "dynamic_sizing":    False,
        "description":       "Paper only — no real capital deployed",
    },
    AllocationStage.MICRO: {
        "risk_pct":          0.5,
        "max_positions":     1,
        "max_symbols":       1,
        "max_daily_loss_pct": 1.0,
        "dynamic_sizing":    False,
        "description":       "Micro live — 0.5% risk, 1 symbol, 1 position",
    },
    AllocationStage.SMALL: {
        "risk_pct":          1.0,
        "max_positions":     2,
        "max_symbols":       2,
        "max_daily_loss_pct": 2.0,
        "dynamic_sizing":    False,
        "description":       "Small live — 1.0% risk, 2 symbols, 2 positions",
    },
    AllocationStage.NORMAL: {
        "risk_pct":          2.0,
        "max_positions":     5,
        "max_symbols":       10,
        "max_daily_loss_pct": 4.0,
        "dynamic_sizing":    False,
        "description":       "Normal live — 2.0% risk, all confirmed lanes, 5 positions",
    },
    AllocationStage.FULL: {
        "risk_pct":          2.0,   # base; can scale to 5% with dynamic sizing
        "max_risk_pct":      5.0,   # ceiling for dynamic sizing
        "max_positions":     10,
        "max_symbols":       20,
        "max_daily_loss_pct": 6.0,
        "dynamic_sizing":    True,
        "description":       "Full — 2–5% dynamic risk, all lanes, 10 positions",
    },
}

# Minimum position size sanity limits
MIN_UNITS = 0.001   # crypto (e.g. 0.001 ETH)
MIN_NOTIONAL = 5.0  # USD — don't trade below $5 notional


class CapitalAllocator:
    """
    Determines position size and enforces stage-based capital controls.

    Stage is loaded from kill_switch.json if present (supports centralised
    stage management). Pass stage= to override at construction time.

    Position sizing formula (risk-based):
        risk_amount = balance * risk_pct / 100
        units       = risk_amount / risk_pts_in_currency

    For crypto, risk_pts is in the same currency as the price (USD).
    For indices (OANDA), risk_pts is in points — caller must convert to USD.
    """

    def __init__(self, stage: int | AllocationStage | None = None):
        # Load from kill_switch.json if stage not provided
        if stage is None:
            stage = self._load_stage_from_ks()

        try:
            self._stage = AllocationStage(int(stage))
        except ValueError:
            logger.warning("Invalid stage %s — defaulting to PAPER", stage)
            self._stage = AllocationStage.PAPER

        logger.info(
            "CapitalAllocator initialised — stage=%s (%s)",
            self._stage.name,
            STAGE_LIMITS[self._stage]["description"],
        )

    # ------------------------------------------------------------------
    # Stage persistence
    # ------------------------------------------------------------------
    def _load_stage_from_ks(self) -> int:
        """Read stage field from kill_switch.json. Defaults to 0 (PAPER)."""
        if not KILL_SWITCH_PATH.exists():
            return 0
        try:
            with open(KILL_SWITCH_PATH, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            return int(data.get("stage", 0))
        except Exception as exc:
            logger.warning("Could not read stage from kill_switch.json: %s — using PAPER", exc)
            return 0

    def _save_stage_to_ks(self):
        """Persist current stage to kill_switch.json stage field."""
        KILL_SWITCH_PATH.parent.mkdir(parents=True, exist_ok=True)
        current: dict = {}
        if KILL_SWITCH_PATH.exists():
            try:
                with open(KILL_SWITCH_PATH, "r", encoding="utf-8") as fh:
                    current = json.load(fh)
            except Exception:
                pass
        current["stage"] = int(self._stage)
        tmp = KILL_SWITCH_PATH.with_suffix(".tmp")
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(current, fh, indent=2)
        tmp.replace(KILL_SWITCH_PATH)
        logger.info("Stage saved to kill_switch.json: %s", self._stage.name)

    # ------------------------------------------------------------------
    # Core sizing
    # ------------------------------------------------------------------
    def get_position_size(
        self,
        symbol:      str,
        balance:     float,
        risk_pts:    float,
        entry_price: float = 1.0,
    ) -> float:
        """
        Compute position size (units/contracts) using the risk-based formula.

        Args:
            symbol:       Trading symbol (e.g. "ETH", "NAS100")
            balance:      Account balance in USD
            risk_pts:     Stop-loss distance in price points (USD per unit)
            entry_price:  Entry price (used for notional sanity check)

        Returns:
            Float units to trade. Returns 0.0 for PAPER stage.

        Notes:
            - PAPER stage always returns 0.0
            - Returns 0.0 if balance / risk_pts are invalid or produce sub-minimum size
        """
        if self._stage == AllocationStage.PAPER:
            logger.debug("get_position_size: PAPER stage — returning 0")
            return 0.0

        if balance <= 0 or risk_pts <= 0:
            logger.warning("get_position_size: invalid balance=%.2f risk_pts=%.4f", balance, risk_pts)
            return 0.0

        risk_pct    = self.get_risk_pct(symbol)
        risk_amount = balance * risk_pct / 100.0

        # Dynamic sizing: scale up slightly above 2% based on recent win rate
        # (stub — full implementation would query performance stats)
        if STAGE_LIMITS[self._stage].get("dynamic_sizing") and risk_pct < STAGE_LIMITS[self._stage].get("max_risk_pct", risk_pct):
            # Placeholder: could scale based on performance_compare stats
            pass

        units = risk_amount / risk_pts

        # Sanity checks
        if units < MIN_UNITS:
            logger.debug(
                "Computed units %.6f below MIN_UNITS %.6f for %s — returning 0",
                units, MIN_UNITS, symbol,
            )
            return 0.0

        notional = units * entry_price
        if notional < MIN_NOTIONAL:
            logger.debug(
                "Notional $%.2f below MIN_NOTIONAL $%.2f for %s — returning 0",
                notional, MIN_NOTIONAL, symbol,
            )
            return 0.0

        logger.debug(
            "get_position_size: %s balance=%.2f risk_pct=%.2f%% risk_pts=%.4f → %.6f units",
            symbol, balance, risk_pct, risk_pts, units,
        )
        return round(units, 6)

    def can_add_position(
        self,
        symbol:                str,
        open_positions_count:  int = 0,
    ) -> bool:
        """
        Returns True if the allocator allows opening another position.

        Checks:
          - Stage is not PAPER
          - open_positions_count < max_positions for current stage
          - Kill switch is armed (via file check — cheap)
        """
        if self._stage == AllocationStage.PAPER:
            logger.debug("can_add_position: PAPER stage — False")
            return False

        limits      = STAGE_LIMITS[self._stage]
        max_pos     = limits["max_positions"]

        if open_positions_count >= max_pos:
            logger.info(
                "can_add_position: %s — at max positions (%d/%d)",
                symbol, open_positions_count, max_pos,
            )
            return False

        # Check kill switch (cheap file read)
        if not self._is_kill_switch_armed():
            logger.warning("can_add_position: kill switch not ARMED — False")
            return False

        return True

    def get_risk_pct(self, symbol: str) -> float:
        """
        Return the risk percentage for a given symbol at the current stage.
        Future enhancement: per-symbol risk adjustments (e.g. BTC > ETH > SOL).
        """
        base_pct = STAGE_LIMITS[self._stage]["risk_pct"]
        # Symbol-level adjustments (stub — extend as needed)
        adjustments: dict[str, float] = {
            # e.g. "SOL": 0.75,  # slightly less risk on SOL
        }
        return adjustments.get(symbol.upper(), base_pct)

    # ------------------------------------------------------------------
    # Stage transitions
    # ------------------------------------------------------------------
    def advance_stage(self, reason: str = "manual") -> AllocationStage:
        """
        Move to the next allocation stage.
        Requires kill switch to be ARMED.

        Returns the new stage.
        """
        if not self._is_kill_switch_armed():
            raise RuntimeError("Cannot advance stage: kill switch is not ARMED")

        if self._stage == AllocationStage.FULL:
            logger.warning("Already at FULL stage — cannot advance further")
            return self._stage

        new_stage    = AllocationStage(int(self._stage) + 1)
        old_name     = self._stage.name
        self._stage  = new_stage
        self._save_stage_to_ks()

        logger.info("Stage advanced: %s → %s (reason: %s)", old_name, new_stage.name, reason)
        return new_stage

    def rollback_stage(self, reason: str = "manual") -> AllocationStage:
        """
        Move to the previous allocation stage.
        Does not require kill switch arm (can be used as safety measure).

        Returns the new stage.
        """
        if self._stage == AllocationStage.PAPER:
            logger.warning("Already at PAPER stage — cannot roll back further")
            return self._stage

        new_stage    = AllocationStage(int(self._stage) - 1)
        old_name     = self._stage.name
        self._stage  = new_stage
        self._save_stage_to_ks()

        logger.info("Stage rolled back: %s → %s (reason: %s)", old_name, new_stage.name, reason)
        return new_stage

    # ------------------------------------------------------------------
    # Status
    # ------------------------------------------------------------------
    def get_status(self) -> dict:
        """Return a dict summarising current stage and limits."""
        limits = STAGE_LIMITS[self._stage]
        return {
            "stage":             int(self._stage),
            "stage_name":        self._stage.name,
            "description":       limits["description"],
            "risk_pct":          limits["risk_pct"],
            "max_positions":     limits["max_positions"],
            "max_symbols":       limits["max_symbols"],
            "max_daily_loss_pct": limits["max_daily_loss_pct"],
            "dynamic_sizing":    limits.get("dynamic_sizing", False),
            "kill_switch_armed": self._is_kill_switch_armed(),
        }

    def print_status(self):
        """Print a formatted summary of the current allocation configuration."""
        s = self.get_status()
        print("\n" + "=" * 55)
        print("  GB-BRAIN Capital Allocator Status")
        print("=" * 55)
        print(f"  Stage         : {s['stage']} — {s['stage_name']}")
        print(f"  Description   : {s['description']}")
        print(f"  Risk % / trade: {s['risk_pct']}%")
        print(f"  Max positions : {s['max_positions']}")
        print(f"  Max symbols   : {s['max_symbols']}")
        print(f"  Max daily loss: {s['max_daily_loss_pct']}%")
        print(f"  Dynamic sizing: {'Yes' if s['dynamic_sizing'] else 'No'}")
        print(f"  Kill switch   : {'ARMED ✓' if s['kill_switch_armed'] else 'NOT ARMED ✗'}")
        print("=" * 55)
        print()

        # Print all stages for reference
        print("  All Stages:")
        print(f"  {'Stage':<7} {'Name':<8} {'Risk%':>7} {'MaxPos':>7} {'MaxSym':>8} {'MaxDD%':>7}")
        print("  " + "-" * 46)
        for stage in AllocationStage:
            lim    = STAGE_LIMITS[stage]
            marker = " ←" if stage == self._stage else ""
            print(
                f"  {int(stage):<7} {stage.name:<8} "
                f"{lim['risk_pct']:>6.1f}% "
                f"{lim['max_positions']:>7} "
                f"{lim['max_symbols']:>8} "
                f"{lim['max_daily_loss_pct']:>6.1f}%"
                f"{marker}"
            )
        print()

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------
    def _is_kill_switch_armed(self) -> bool:
        """Cheap file-based kill switch check without importing KillSwitch class."""
        if not KILL_SWITCH_PATH.exists():
            return True  # No kill switch file = assume armed (fresh install)
        try:
            with open(KILL_SWITCH_PATH, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            return data.get("state", "ARMED") == "ARMED"
        except Exception:
            return False  # Fail safe


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    import argparse

    p = argparse.ArgumentParser(
        description="GB-BRAIN Capital Allocator — manage live rollout stage and position sizing",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--status",   action="store_true", help="Print current stage and limits")
    p.add_argument("--advance",  metavar="REASON", help="Advance to next stage")
    p.add_argument("--rollback", metavar="REASON", help="Roll back to previous stage")
    p.add_argument(
        "--calc",
        nargs=4,
        metavar=("SYMBOL", "BALANCE", "RISK_PTS", "ENTRY"),
        help="Calculate position size: --calc ETH 5000 50 3000",
    )
    p.add_argument("--stage",     type=int, help="Override stage (0-4)")
    p.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR"])
    args = p.parse_args()

    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    allocator = CapitalAllocator(stage=args.stage)

    if args.status or not any([args.advance, args.rollback, args.calc]):
        allocator.print_status()

    if args.advance:
        new_stage = allocator.advance_stage(reason=args.advance)
        print(f"Advanced to stage {int(new_stage)}: {new_stage.name}")

    if args.rollback:
        new_stage = allocator.rollback_stage(reason=args.rollback)
        print(f"Rolled back to stage {int(new_stage)}: {new_stage.name}")

    if args.calc:
        symbol, balance, risk_pts, entry = args.calc
        units = allocator.get_position_size(
            symbol=symbol,
            balance=float(balance),
            risk_pts=float(risk_pts),
            entry_price=float(entry),
        )
        print(
            f"Position size for {symbol}: {units} units "
            f"(balance=${float(balance):,.2f}, risk_pts={float(risk_pts)}, entry={float(entry)})"
        )


if __name__ == "__main__":
    main()
