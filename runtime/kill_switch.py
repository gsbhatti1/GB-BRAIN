"""
GB-BRAIN — Kill Switch (Phase 8)
==================================
Emergency stop system. Can halt all trading immediately.
Multiple trigger methods: file-based, API, Telegram command.

Kill switch states:
  ARMED    — Normal operation
  TRIPPED  — All new orders blocked, open positions flagged
  HALTED   — All positions closed, all processes stopped

Usage:
    python runtime/kill_switch.py arm         # Enable trading
    python runtime/kill_switch.py trip        # Stop new orders  
    python runtime/kill_switch.py halt        # Full stop + close positions
    python runtime/kill_switch.py status      # Check current state
    python runtime/kill_switch.py reset       # Reset to ARMED (manual only)
"""

import argparse
import json
import logging
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv

load_dotenv(ROOT / ".env")

logger = logging.getLogger("gb_brain.kill_switch")

KILL_SWITCH_PATH = ROOT / "db" / "kill_switch.json"

# Valid states
STATE_ARMED   = "ARMED"
STATE_TRIPPED = "TRIPPED"
STATE_HALTED  = "HALTED"
VALID_STATES  = {STATE_ARMED, STATE_TRIPPED, STATE_HALTED}


# ---------------------------------------------------------------------------
# Telegram helper — standalone import guard
# ---------------------------------------------------------------------------
def _import_telegram():
    try:
        from notifications.telegram_alert import send_alert
        return send_alert
    except ImportError:
        return None


class KillSwitch:
    """
    File-based kill switch for GB-BRAIN.

    State is stored in db/kill_switch.json so it persists across process
    restarts. Any component can read is_armed() cheaply without DB access.

    Schema of kill_switch.json:
    {
        "state":       "ARMED" | "TRIPPED" | "HALTED",
        "reason":      "<human readable>",
        "tripped_at":  "<ISO timestamp or null>",
        "tripped_by":  "<system | manual | risk_manager>",
        "stage":       <int 0-4, used by CapitalAllocator>
    }
    """

    def __init__(self):
        KILL_SWITCH_PATH.parent.mkdir(parents=True, exist_ok=True)
        self._send_alert = _import_telegram()

        # Initialise file if missing
        if not KILL_SWITCH_PATH.exists():
            self._write_state(
                state=STATE_ARMED,
                reason="Initial state",
                tripped_by="system",
            )

    # ------------------------------------------------------------------
    # State management
    # ------------------------------------------------------------------
    def _read_state(self) -> dict:
        """Read and return the current state dict from JSON file."""
        try:
            with open(KILL_SWITCH_PATH, "r", encoding="utf-8") as fh:
                return json.load(fh)
        except (json.JSONDecodeError, OSError) as exc:
            logger.error("Failed to read kill_switch.json: %s — defaulting to HALTED", exc)
            # Fail safe: treat as halted if file is corrupt
            return {
                "state":      STATE_HALTED,
                "reason":     f"Read error: {exc}",
                "tripped_at": datetime.utcnow().isoformat(),
                "tripped_by": "system",
                "stage":      0,
            }

    def _write_state(
        self,
        state: str,
        reason: str,
        tripped_by: str,
        extra: dict | None = None,
    ):
        """Atomically write state to JSON file."""
        if state not in VALID_STATES:
            raise ValueError(f"Invalid state '{state}' — must be one of {VALID_STATES}")

        current = {}
        if KILL_SWITCH_PATH.exists():
            try:
                with open(KILL_SWITCH_PATH, "r", encoding="utf-8") as fh:
                    current = json.load(fh)
            except Exception:
                pass

        payload = {
            "state":      state,
            "reason":     reason,
            "tripped_at": datetime.utcnow().isoformat() if state != STATE_ARMED else None,
            "tripped_by": tripped_by,
            "stage":      current.get("stage", 0),
        }
        if extra:
            payload.update(extra)

        tmp_path = KILL_SWITCH_PATH.with_suffix(".tmp")
        with open(tmp_path, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2)
        tmp_path.replace(KILL_SWITCH_PATH)  # atomic rename

        logger.info("KillSwitch → %s (reason=%s by=%s)", state, reason, tripped_by)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def arm(self, reason: str = "manual"):
        """Set state to ARMED — enable trading."""
        self._write_state(STATE_ARMED, reason, tripped_by="manual")
        msg = f"[KILL SWITCH] ARMED — {reason}"
        logger.info(msg)
        self._notify(msg)

    def trip(self, reason: str = "manual"):
        """
        Set state to TRIPPED — block new orders, flag open positions.
        This is the first-level emergency stop.
        """
        self._write_state(STATE_TRIPPED, reason, tripped_by="manual")
        msg = f"[URGENT] KILL SWITCH TRIPPED — {reason}. All new orders blocked."
        logger.warning(msg)
        self._notify(msg)

    def halt(self, reason: str = "manual", close_positions: bool = False):
        """
        Set state to HALTED — full stop.
        Optionally attempt to close all open positions via connected bridges.
        """
        self._write_state(
            STATE_HALTED,
            reason,
            tripped_by="manual",
            extra={"close_positions_requested": close_positions},
        )
        msg = f"[CRITICAL] KILL SWITCH HALTED — {reason}. All trading stopped."
        logger.critical(msg)
        self._notify(msg)

        if close_positions:
            self._attempt_close_all_positions()

    def status(self) -> dict:
        """Return the current state dict."""
        return self._read_state()

    def is_armed(self) -> bool:
        """
        Returns True only if state is ARMED.
        All trading loops should call this before placing any order.
        """
        try:
            state = self._read_state()
            return state.get("state") == STATE_ARMED
        except Exception as exc:
            logger.error("is_armed() read error: %s — defaulting to False (safe)", exc)
            return False  # Fail safe

    def reset(self, reason: str = "manual reset"):
        """
        Reset to ARMED state. Requires interactive confirmation.
        This is intentionally manual-only to prevent accidental automation.
        """
        current = self._read_state()
        print(f"\n Current kill switch state: {current.get('state')}")
        print(f" Reason: {current.get('reason')}")
        print(f" Tripped at: {current.get('tripped_at')}")
        print()
        confirm = input("Type 'CONFIRM RESET' to reset kill switch to ARMED: ").strip()
        if confirm != "CONFIRM RESET":
            print("Reset aborted.")
            return
        self.arm(reason=reason)
        print(f"Kill switch reset to ARMED.")

    # ------------------------------------------------------------------
    # Auto-trip from risk manager
    # ------------------------------------------------------------------
    def check_and_trip_if_needed(self, risk_manager) -> bool:
        """
        Auto-trips the kill switch if risk limits are breached.

        risk_manager must expose:
          - daily_loss_exceeded() -> bool
          - max_drawdown_exceeded() -> bool  (optional)
          - get_risk_state() -> dict          (optional)

        Returns True if tripped, False otherwise.
        """
        if not self.is_armed():
            return False  # Already tripped/halted

        reasons = []

        try:
            if hasattr(risk_manager, "daily_loss_exceeded") and risk_manager.daily_loss_exceeded():
                reasons.append("daily loss limit exceeded")
        except Exception as exc:
            logger.error("Risk check error (daily_loss): %s", exc)

        try:
            if hasattr(risk_manager, "max_drawdown_exceeded") and risk_manager.max_drawdown_exceeded():
                reasons.append("max drawdown exceeded")
        except Exception as exc:
            logger.error("Risk check error (max_drawdown): %s", exc)

        if reasons:
            combined_reason = " | ".join(reasons)
            logger.warning("Auto-tripping kill switch: %s", combined_reason)
            self.trip(reason=f"auto: {combined_reason}")
            return True

        return False

    # ------------------------------------------------------------------
    # Position closing (best-effort)
    # ------------------------------------------------------------------
    def _attempt_close_all_positions(self):
        """
        Best-effort attempt to close all open positions via available bridges.
        Logs errors but does not raise — the kill switch is already set.
        """
        logger.warning("Attempting to close all open positions...")
        bridges_tried = 0

        for bridge_name, bridge_module in [
            ("BloFin", "brokers.blofin_bridge"),
            ("OANDA",  "brokers.oanda_bridge"),
        ]:
            try:
                import importlib
                mod    = importlib.import_module(bridge_module)
                bridge = mod.__dict__.get("BloFinBridge") or mod.__dict__.get("OandaBridge")
                if bridge:
                    b = bridge()
                    if hasattr(b, "close_all_positions"):
                        b.close_all_positions()
                        logger.info("Closed all positions via %s", bridge_name)
                        bridges_tried += 1
            except Exception as exc:
                logger.error("Failed to close positions via %s: %s", bridge_name, exc)

        if bridges_tried == 0:
            logger.warning("No bridges available — positions may remain open. MANUAL ACTION REQUIRED.")
            self._notify(
                "[CRITICAL] GB-BRAIN could not auto-close positions — MANUAL CLOSE REQUIRED."
            )

    # ------------------------------------------------------------------
    # Telegram
    # ------------------------------------------------------------------
    def _notify(self, message: str):
        if self._send_alert:
            try:
                self._send_alert(message)
            except Exception as exc:
                logger.warning("Telegram notification failed: %s", exc)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="GB-BRAIN Kill Switch — emergency trading stop control",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    sub = p.add_subparsers(dest="command", required=True)

    arm_p = sub.add_parser("arm",   help="Enable trading (ARMED state)")
    arm_p.add_argument("--reason", default="manual arm", help="Reason for arming")

    trip_p = sub.add_parser("trip",  help="Stop new orders (TRIPPED state)")
    trip_p.add_argument("--reason", default="manual trip", help="Reason for tripping")

    halt_p = sub.add_parser("halt",  help="Full stop + optional position close (HALTED state)")
    halt_p.add_argument("--reason", default="manual halt", help="Reason for halting")
    halt_p.add_argument(
        "--close-positions", action="store_true",
        help="Attempt to close all open positions via bridges",
    )

    sub.add_parser("status", help="Print current kill switch state")
    sub.add_parser("reset",  help="Reset to ARMED state (requires interactive confirmation)")

    p.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
    )
    return p


def main():
    args = _build_parser().parse_args()
    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    ks = KillSwitch()

    if args.command == "arm":
        ks.arm(reason=args.reason)
        print(f"Kill switch ARMED — {args.reason}")

    elif args.command == "trip":
        ks.trip(reason=args.reason)
        print(f"Kill switch TRIPPED — {args.reason}")

    elif args.command == "halt":
        ks.halt(reason=args.reason, close_positions=args.close_positions)
        print(f"Kill switch HALTED — {args.reason}")

    elif args.command == "status":
        state = ks.status()
        print(json.dumps(state, indent=2))

    elif args.command == "reset":
        ks.reset()


if __name__ == "__main__":
    main()
