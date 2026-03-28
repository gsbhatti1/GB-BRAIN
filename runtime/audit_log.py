"""
GB-BRAIN — Audit Log (Phase 8)
================================
Immutable append-only log of all trading decisions.
Every order, fill, rejection, risk limit hit, kill switch trip is logged here.
Separate from SQLite — written to flat JSONL file that cannot be overwritten.

Usage:
    from runtime.audit_log import AuditLog
    audit = AuditLog()
    audit.log_order(symbol, side, units, price, broker, reason)
    audit.log_rejection(symbol, reason, risk_state)
    audit.log_kill_switch(state, reason)
    audit.tail(n=20)      # Last 20 entries
"""

import csv
import json
import logging
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv

load_dotenv(ROOT / ".env")

logger = logging.getLogger("gb_brain.audit_log")

AUDIT_LOG_PATH = ROOT / "db" / "audit.jsonl"

# Event type constants
EV_ORDER       = "ORDER"
EV_FILL        = "FILL"
EV_REJECTION   = "REJECTION"
EV_KILL_SWITCH = "KILL_SWITCH"
EV_ERROR       = "ERROR"
EV_CALIBRATION = "CALIBRATION"


class AuditLog:
    """
    Append-only JSONL audit log for all trading decisions and system events.

    Design principles:
      - NEVER overwrites existing entries
      - Each entry is one JSON object per line
      - Each entry has: timestamp (UTC ISO), event_type, data dict
      - Thread-safe via file append mode (OS-level atomicity for small writes)
      - Readable by any tool that understands JSONL
    """

    def __init__(self, path: Path | None = None):
        self._path = Path(path) if path else AUDIT_LOG_PATH
        self._path.parent.mkdir(parents=True, exist_ok=True)
        # Touch file to ensure it exists
        if not self._path.exists():
            self._path.touch()
        logger.debug("AuditLog initialised at %s", self._path)

    # ------------------------------------------------------------------
    # Internal writer — single point of truth for append
    # ------------------------------------------------------------------
    def _append(self, event_type: str, data: dict):
        """
        Append a single JSON line to the audit log.
        This is the only method that writes to the file.
        """
        entry = {
            "timestamp":  datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            "data":       data,
        }
        line = json.dumps(entry, default=str) + "\n"
        with open(self._path, "a", encoding="utf-8") as fh:
            fh.write(line)

    # ------------------------------------------------------------------
    # Logging methods
    # ------------------------------------------------------------------
    def log_order(
        self,
        symbol:   str,
        side:     str,
        units:    float,
        price:    float | None,
        broker:   str,
        reason:   str,
        strategy: str | None = None,
    ):
        """Log an order submission attempt."""
        self._append(
            EV_ORDER,
            {
                "symbol":   symbol,
                "side":     side,
                "units":    units,
                "price":    price,
                "broker":   broker,
                "reason":   reason,
                "strategy": strategy,
            },
        )
        logger.debug("AUDIT ORDER — %s %s %s @ %s (%s)", side, units, symbol, price, broker)

    def log_fill(
        self,
        symbol:       str,
        side:         str,
        fill_price:   float | None,
        signal_price: float | None,
        slippage:     float | None,
        broker:       str,
    ):
        """Log a confirmed fill with slippage data."""
        self._append(
            EV_FILL,
            {
                "symbol":       symbol,
                "side":         side,
                "fill_price":   fill_price,
                "signal_price": signal_price,
                "slippage_pct": slippage,
                "broker":       broker,
            },
        )
        logger.debug(
            "AUDIT FILL — %s %s fill=%.5f signal=%.5f slip=%.4f%%",
            side, symbol,
            fill_price   or 0,
            signal_price or 0,
            slippage     or 0,
        )

    def log_rejection(
        self,
        symbol:         str,
        reason:         str,
        risk_state_dict: dict | None = None,
    ):
        """Log a trade rejection (risk manager, kill switch, policy gate, etc.)."""
        self._append(
            EV_REJECTION,
            {
                "symbol":     symbol,
                "reason":     reason,
                "risk_state": risk_state_dict or {},
            },
        )
        logger.debug("AUDIT REJECTION — %s: %s", symbol, reason)

    def log_kill_switch(
        self,
        state:      str,
        reason:     str,
        tripped_by: str = "unknown",
    ):
        """Log a kill switch state change."""
        self._append(
            EV_KILL_SWITCH,
            {
                "state":      state,
                "reason":     reason,
                "tripped_by": tripped_by,
            },
        )
        logger.warning("AUDIT KILL_SWITCH — state=%s reason=%s by=%s", state, reason, tripped_by)

    def log_error(
        self,
        component:     str,
        error_msg:     str,
        traceback_str: str | None = None,
    ):
        """Log a system error with optional traceback."""
        self._append(
            EV_ERROR,
            {
                "component": component,
                "error":     error_msg,
                "traceback": traceback_str,
            },
        )
        logger.debug("AUDIT ERROR — %s: %s", component, error_msg)

    def log_calibration(self, changes_dict: dict):
        """Log the result of a calibration run (lane promotions/demotions/pauses)."""
        self._append(EV_CALIBRATION, changes_dict)
        logger.debug("AUDIT CALIBRATION — %d keys logged", len(changes_dict))

    # ------------------------------------------------------------------
    # Tail / view
    # ------------------------------------------------------------------
    def tail(self, n: int = 20):
        """Print the last n entries in a human-readable format."""
        entries = self._read_last_n(n)
        if not entries:
            print("Audit log is empty.")
            return

        print(f"\n{'=' * 72}")
        print(f"  GB-BRAIN Audit Log — last {n} entries")
        print(f"{'=' * 72}")
        for entry in entries:
            ts         = entry.get("timestamp", "?")
            event_type = entry.get("event_type", "?")
            data       = entry.get("data", {})

            # Format the data dict as compact one-liner for readability
            data_str = json.dumps(data, default=str)
            if len(data_str) > 120:
                data_str = data_str[:117] + "..."

            print(f"  [{ts}]  {event_type:<14}  {data_str}")
        print(f"{'=' * 72}\n")

    def _read_last_n(self, n: int) -> list[dict]:
        """Efficiently read last n lines from the JSONL file."""
        if not self._path.exists():
            return []

        lines: list[str] = []
        try:
            with open(self._path, "r", encoding="utf-8") as fh:
                # Read all lines — for large logs, a deque approach is used
                from collections import deque
                dq = deque(fh, maxlen=n)
                lines = list(dq)
        except OSError as exc:
            logger.error("Failed to read audit log: %s", exc)
            return []

        entries = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue
        return entries

    # ------------------------------------------------------------------
    # CSV export
    # ------------------------------------------------------------------
    def export_csv(self, path: str, days: int = 30):
        """
        Export audit log entries from the last `days` days to a CSV file.
        Flattens each entry's data dict into columns.
        """
        cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()

        try:
            all_entries = self._read_all()
        except Exception as exc:
            logger.error("Failed to read audit log for export: %s", exc)
            return

        recent = [e for e in all_entries if e.get("timestamp", "") >= cutoff]

        if not recent:
            print(f"No audit entries in last {days} days.")
            return

        # Collect all unique keys across data dicts
        all_keys: set[str] = set()
        for e in recent:
            all_keys.update(e.get("data", {}).keys())
        data_keys = sorted(all_keys)

        fieldnames = ["timestamp", "event_type"] + data_keys

        out_path = Path(path)
        with open(out_path, "w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            for e in recent:
                row = {
                    "timestamp":  e.get("timestamp"),
                    "event_type": e.get("event_type"),
                }
                row.update(e.get("data", {}))
                writer.writerow(row)

        logger.info("Exported %d audit entries to %s", len(recent), out_path)
        print(f"Exported {len(recent)} entries to {out_path}")

    def _read_all(self) -> list[dict]:
        """Read all entries from the JSONL file."""
        if not self._path.exists():
            return []
        entries = []
        with open(self._path, "r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
        return entries


# ---------------------------------------------------------------------------
# CLI — simple tail + export utility
# ---------------------------------------------------------------------------
def main():
    import argparse

    p = argparse.ArgumentParser(
        description="GB-BRAIN Audit Log — view and export the immutable trading audit trail",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--tail",   type=int, metavar="N", default=20, help="Show last N entries (default 20)")
    p.add_argument("--export", metavar="PATH", help="Export last --days entries to CSV")
    p.add_argument("--days",   type=int, default=30, help="Days to export (default 30)")
    p.add_argument("--log-level", default="WARNING", choices=["DEBUG", "INFO", "WARNING", "ERROR"])
    args = p.parse_args()

    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    )

    audit = AuditLog()

    if args.export:
        audit.export_csv(args.export, days=args.days)
    else:
        audit.tail(n=args.tail)


if __name__ == "__main__":
    main()
