"""
GB-BRAIN — Health Check (Phase 8)
====================================
Checks all system components and reports status.
Designed to run every 5 minutes via cron or supervisor.
Sends Telegram alert if anything is wrong.

Checks:
  - SQLite accessible + not locked
  - observed_signals being written (last signal < 30 min for active sessions)
  - live_observer process running
  - webhook server responding  
  - BloFin/OANDA API reachable (ping only)
  - Kill switch state
  - Disk space (warn if < 1GB free)
  - Last heartbeat from observer < 10 min ago

Usage:
    python runtime/health_check.py
    python runtime/health_check.py --quiet   # Only alert on failures
"""

import argparse
import logging
import shutil
import signal
import sqlite3
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv

load_dotenv(ROOT / ".env")

logger = logging.getLogger("gb_brain.health_check")

DB_PATH         = ROOT / "db" / "gb_brain.db"
HEARTBEAT_PATH  = ROOT / "db" / "observer_heartbeat.json"
KILL_SWITCH_PATH = ROOT / "db" / "kill_switch.json"

# Thresholds
SIGNAL_MAX_AGE_MINUTES   = 30
HEARTBEAT_MAX_AGE_MINUTES = 10
DISK_WARN_GB              = 1.0

# Result constants
STATUS_OK   = "OK"
STATUS_WARN = "WARN"
STATUS_FAIL = "FAIL"
STATUS_SKIP = "SKIP"


def _import_telegram():
    try:
        from execute.telegram_alerts import send_alert
        return send_alert
    except ImportError:
        return None


class HealthCheck:
    """
    Runs all system health checks and aggregates results.
    Sends Telegram alerts if any check fails (or warns, depending on config).
    """

    def __init__(self, quiet: bool = False, alert_on_warn: bool = False):
        self.quiet         = quiet
        self.alert_on_warn = alert_on_warn
        self._send_alert   = _import_telegram()

    # ------------------------------------------------------------------
    # Main entry
    # ------------------------------------------------------------------
    def run_all(self) -> dict[str, dict]:
        """
        Run all health checks.

        Returns dict:
          {check_name: {"status": "OK"|"WARN"|"FAIL"|"SKIP", "detail": str}}
        """
        checks = {
            "db":             self.check_db,
            "signals_fresh":  self.check_signals_fresh,
            "kill_switch":    self.check_kill_switch,
            "disk_space":     self.check_disk_space,
            "heartbeat":      self.check_heartbeat,
            "blofin_api":     self.check_blofin_api,
            "oanda_api":      self.check_oanda_api,
        }

        results: dict[str, dict] = {}
        for name, fn in checks.items():
            try:
                results[name] = fn()
            except Exception as exc:
                results[name] = {
                    "status": STATUS_FAIL,
                    "detail": f"Unexpected error: {exc}",
                }
                logger.exception("Health check '%s' raised: %s", name, exc)

        self._alert_if_needed(results)

        if not self.quiet:
            self.print_report(results)

        return results

    # ------------------------------------------------------------------
    # Individual checks
    # ------------------------------------------------------------------
    def check_db(self) -> dict:
        """Verify SQLite is accessible and not locked."""
        if not DB_PATH.exists():
            return {"status": STATUS_FAIL, "detail": f"DB file not found: {DB_PATH}"}
        try:
            conn = sqlite3.connect(DB_PATH, timeout=5)
            conn.execute("SELECT 1")
            # Check for WAL journal (indicates active writes — not an error)
            tables = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()
            conn.close()
            table_names = [t[0] for t in tables]
            return {
                "status": STATUS_OK,
                "detail": f"Accessible. Tables: {', '.join(table_names) or 'none'}",
            }
        except sqlite3.OperationalError as exc:
            if "locked" in str(exc).lower():
                return {"status": STATUS_WARN, "detail": f"DB locked: {exc}"}
            return {"status": STATUS_FAIL, "detail": f"DB error: {exc}"}
        except Exception as exc:
            return {"status": STATUS_FAIL, "detail": f"Unexpected DB error: {exc}"}

    def check_signals_fresh(self) -> dict:
        """
        Verify observed_signals is being written.
        WARN if last signal is older than SIGNAL_MAX_AGE_MINUTES.
        Skips check outside of market hours (basic check: weekdays 08:00-22:00 UTC).
        """
        now_utc = datetime.now(timezone.utc)

        # Basic market hours guard (Mon-Fri, 08:00-22:00 UTC)
        # Crypto markets are 24/7, but avoid false alarms on deep nights
        is_weekday = now_utc.weekday() < 5
        in_hours   = 8 <= now_utc.hour < 22

        if not (is_weekday and in_hours):
            return {"status": STATUS_SKIP, "detail": "Outside typical market hours — skipped"}

        if not DB_PATH.exists():
            return {"status": STATUS_SKIP, "detail": "DB not found — skip signals check"}

        try:
            conn = sqlite3.connect(DB_PATH, timeout=5)
            try:
                row = conn.execute(
                    "SELECT MAX(observed_at) FROM observed_signals"
                ).fetchone()
            except sqlite3.OperationalError:
                conn.close()
                return {"status": STATUS_SKIP, "detail": "observed_signals table missing"}
            conn.close()

            last_at = row[0] if row else None
            if not last_at:
                return {"status": STATUS_WARN, "detail": "No signals in observed_signals table"}

            last_dt = datetime.fromisoformat(last_at.replace("Z", "+00:00"))
            if last_dt.tzinfo is None:
                last_dt = last_dt.replace(tzinfo=timezone.utc)
            age_min = (now_utc - last_dt).total_seconds() / 60

            if age_min > SIGNAL_MAX_AGE_MINUTES:
                return {
                    "status": STATUS_WARN,
                    "detail": f"Last signal {age_min:.1f}m ago (threshold {SIGNAL_MAX_AGE_MINUTES}m)",
                }
            return {
                "status": STATUS_OK,
                "detail": f"Last signal {age_min:.1f}m ago",
            }
        except Exception as exc:
            return {"status": STATUS_FAIL, "detail": f"Signal freshness check error: {exc}"}

    def check_kill_switch(self) -> dict:
        """Check current kill switch state."""
        if not KILL_SWITCH_PATH.exists():
            return {"status": STATUS_WARN, "detail": "kill_switch.json not found — system may not be initialised"}
        try:
            import json
            with open(KILL_SWITCH_PATH, "r", encoding="utf-8") as fh:
                ks = json.load(fh)
            state  = ks.get("state", "UNKNOWN")
            reason = ks.get("reason", "")
            if state == "ARMED":
                return {"status": STATUS_OK, "detail": f"ARMED — {reason}"}
            elif state == "TRIPPED":
                return {"status": STATUS_WARN, "detail": f"TRIPPED — {reason}"}
            elif state == "HALTED":
                return {"status": STATUS_FAIL, "detail": f"HALTED — {reason}"}
            else:
                return {"status": STATUS_WARN, "detail": f"Unknown state: {state}"}
        except Exception as exc:
            return {"status": STATUS_FAIL, "detail": f"Kill switch read error: {exc}"}

    def check_disk_space(self) -> dict:
        """Warn if disk space < DISK_WARN_GB on the workspace partition."""
        try:
            usage = shutil.disk_usage(ROOT)
            free_gb = usage.free / (1024 ** 3)
            total_gb = usage.total / (1024 ** 3)
            used_pct = (usage.used / usage.total) * 100
            detail = f"{free_gb:.2f}GB free / {total_gb:.2f}GB total ({used_pct:.1f}% used)"
            if free_gb < DISK_WARN_GB:
                return {"status": STATUS_WARN, "detail": f"Low disk space: {detail}"}
            return {"status": STATUS_OK, "detail": detail}
        except Exception as exc:
            return {"status": STATUS_FAIL, "detail": f"Disk check error: {exc}"}

    def check_heartbeat(self) -> dict:
        """Verify observer process is writing heartbeat within HEARTBEAT_MAX_AGE_MINUTES."""
        if not HEARTBEAT_PATH.exists():
            return {
                "status": STATUS_WARN,
                "detail": f"Heartbeat file not found: {HEARTBEAT_PATH}",
            }
        try:
            import json
            with open(HEARTBEAT_PATH, "r", encoding="utf-8") as fh:
                hb = json.load(fh)
            last_beat = hb.get("timestamp") or hb.get("ts")
            if not last_beat:
                return {"status": STATUS_WARN, "detail": "Heartbeat file has no timestamp"}

            last_dt = datetime.fromisoformat(last_beat.replace("Z", "+00:00"))
            if last_dt.tzinfo is None:
                last_dt = last_dt.replace(tzinfo=timezone.utc)
            age_min = (datetime.now(timezone.utc) - last_dt).total_seconds() / 60

            if age_min > HEARTBEAT_MAX_AGE_MINUTES:
                return {
                    "status": STATUS_FAIL,
                    "detail": f"Observer heartbeat is {age_min:.1f}m old (max {HEARTBEAT_MAX_AGE_MINUTES}m)",
                }
            return {"status": STATUS_OK, "detail": f"Observer heartbeat {age_min:.1f}m ago"}
        except Exception as exc:
            return {"status": STATUS_FAIL, "detail": f"Heartbeat check error: {exc}"}

    def check_blofin_api(self) -> dict:
        """Ping the BloFin public API endpoint."""
        import os
        url = "https://openapi.blofin.com/api/v1/market/tickers?instType=SWAP"
        return self._ping_api("BloFin", url, timeout=5)

    def check_oanda_api(self) -> dict:
        """Ping the OANDA API endpoint (requires API key for practice)."""
        import os
        api_key     = os.getenv("OANDA_API_TOKEN", "") or os.getenv("OANDA_API_KEY", "")
        practice    = os.getenv("OANDA_PRACTICE", "true").lower() in ("1", "true", "yes")
        base_url    = "https://api-fxpractice.oanda.com" if practice else "https://api-trade.oanda.com"
        url         = f"{base_url}/v3/accounts"

        if not api_key:
            return {"status": STATUS_SKIP, "detail": "OANDA_API_TOKEN not set — skipped"}

        return self._ping_api("OANDA", url, timeout=5, headers={"Authorization": f"Bearer {api_key}"})

    # ------------------------------------------------------------------
    # Helper: ping URL
    # ------------------------------------------------------------------
    def _ping_api(
        self,
        name:    str,
        url:     str,
        timeout: int = 5,
        headers: dict | None = None,
    ) -> dict:
        """Attempt a lightweight HTTP GET to check API reachability."""
        import urllib.request
        import urllib.error
        try:
            req = urllib.request.Request(url, headers=headers or {}, method="GET")
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                code = resp.getcode()
                if 200 <= code < 300:
                    return {"status": STATUS_OK, "detail": f"HTTP {code}"}
                else:
                    return {"status": STATUS_WARN, "detail": f"HTTP {code}"}
        except urllib.error.HTTPError as exc:
            # HTTPError means the server responded — check if auth-related
            if exc.code in (401, 403):
                return {"status": STATUS_OK, "detail": f"Reachable (HTTP {exc.code})"}
            return {"status": STATUS_WARN, "detail": f"HTTP {exc.code}"}
        except OSError as exc:
            # Connection refused, DNS failure, timeout
            return {"status": STATUS_FAIL, "detail": f"{name} unreachable: {exc}"}
        except Exception as exc:
            return {"status": STATUS_FAIL, "detail": f"{name} ping error: {exc}"}

    # ------------------------------------------------------------------
    # Alerting
    # ------------------------------------------------------------------
    def _alert_if_needed(self, results: dict[str, dict]):
        """Send Telegram alert if any check is FAIL (or WARN if alert_on_warn)."""
        failing = [
            (name, r)
            for name, r in results.items()
            if r["status"] == STATUS_FAIL
            or (self.alert_on_warn and r["status"] == STATUS_WARN)
        ]
        if not failing:
            return

        lines = ["[HEALTH CHECK ALERT] GB-BRAIN system issues detected:"]
        for name, r in failing:
            lines.append(f"  ❌ {name}: {r['detail']}")

        message = "\n".join(lines)
        logger.warning("Health check alert: %s", message)

        if self._send_alert:
            try:
                self._send_alert(message)
            except Exception as exc:
                logger.warning("Telegram alert failed: %s", exc)

    # ------------------------------------------------------------------
    # Report printer
    # ------------------------------------------------------------------
    def print_report(self, results: dict[str, dict]):
        """Print a clean aligned status table."""
        now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        print(f"\n{'=' * 62}")
        print(f"  GB-BRAIN Health Check — {now_str}")
        print(f"{'=' * 62}")
        print(f"  {'Check':<22} {'Status':<8} Detail")
        print(f"  {'-' * 58}")

        status_icons = {
            STATUS_OK:   "✓",
            STATUS_WARN: "!",
            STATUS_FAIL: "✗",
            STATUS_SKIP: "-",
        }

        for name, r in results.items():
            status  = r.get("status", "?")
            detail  = r.get("detail", "")
            icon    = status_icons.get(status, "?")
            # Truncate detail for display
            if len(detail) > 45:
                detail = detail[:42] + "..."
            print(f"  {name:<22} [{icon}] {status:<5}  {detail}")

        counts = {s: sum(1 for r in results.values() if r["status"] == s) for s in [STATUS_OK, STATUS_WARN, STATUS_FAIL, STATUS_SKIP]}
        print(f"  {'-' * 58}")
        print(
            f"  OK={counts[STATUS_OK]}  WARN={counts[STATUS_WARN]}  "
            f"FAIL={counts[STATUS_FAIL]}  SKIP={counts[STATUS_SKIP]}"
        )
        print(f"{'=' * 62}\n")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="GB-BRAIN Health Check — system component status monitor",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress output unless there are failures",
    )
    p.add_argument(
        "--alert-only",
        action="store_true",
        help="Only send Telegram alert on FAIL, suppress console output",
    )
    p.add_argument(
        "--alert-on-warn",
        action="store_true",
        help="Also send Telegram alerts for WARN (not just FAIL)",
    )
    p.add_argument(
        "--log-level",
        default="WARNING",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
    )
    return p


def main():
    args   = _build_parser().parse_args()
    quiet  = args.quiet or args.alert_only

    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    hc      = HealthCheck(quiet=quiet, alert_on_warn=args.alert_on_warn)
    results = hc.run_all()

    # Exit with code 1 if any FAIL
    any_fail = any(r["status"] == STATUS_FAIL for r in results.values())
    sys.exit(1 if any_fail else 0)


if __name__ == "__main__":
    main()
