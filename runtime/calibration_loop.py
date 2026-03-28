"""
GB-BRAIN — Calibration Loop (Phase 7)
=======================================
Wraps weekly_calibrator.py into a schedulable loop.
Can be run manually or via cron/supervisor.

Weekly workflow:
  1. Load signal + trade data for past N days
  2. Score each lane
  3. Promote strong lanes (candidate → confirmed)
  4. Demote weak lanes (confirmed → paused)
  5. Pause broken lanes (no signals / error rate high)
  6. Generate weekly report
  7. Send Telegram summary

Usage:
    python runtime/calibration_loop.py                  # Run now
    python runtime/calibration_loop.py --dry-run
    python runtime/calibration_loop.py --days 14
    python runtime/calibration_loop.py --force-demote ETH parallax
"""

import argparse
import logging
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv

load_dotenv(ROOT / ".env")

logger = logging.getLogger("gb_brain.calibration_loop")

REPORTS_DIR = ROOT / "monitor" / "reports"


# ---------------------------------------------------------------------------
# Lazy imports
# ---------------------------------------------------------------------------
def _import_calibrator():
    try:
        from runtime.weekly_calibrator import WeeklyCalibrator
        return WeeklyCalibrator
    except ImportError as exc:
        logger.warning("WeeklyCalibrator not found: %s", exc)
        return None


def _import_telegram():
    try:
        from execute.telegram_alerts import send_alert
        return send_alert
    except ImportError as exc:
        logger.warning("Telegram alert not found: %s", exc)
        return None


# ---------------------------------------------------------------------------
# CalibrationLoop
# ---------------------------------------------------------------------------
class CalibrationLoop:
    """
    Orchestrates the weekly calibration workflow:

      1. Instantiate WeeklyCalibrator with the desired lookback window.
      2. Run scoring → promotion → demotion → pause logic.
      3. Generate a markdown report saved under monitor/reports/.
      4. Send a Telegram summary.

    dry_run=True will log all intended changes without committing them to the DB.
    """

    def __init__(self, dry_run: bool = False, days: int = 7):
        self.dry_run      = dry_run
        self.days         = days
        self._send_alert  = _import_telegram()
        self._calibrator  = None

        REPORTS_DIR.mkdir(parents=True, exist_ok=True)

        WC = _import_calibrator()
        if WC:
            self._calibrator = WC(dry_run=dry_run, lookback_days=days)
        else:
            logger.warning(
                "WeeklyCalibrator unavailable — calibration_loop will run in stub mode"
            )

    # ------------------------------------------------------------------
    # Main entry
    # ------------------------------------------------------------------
    def run(self) -> dict:
        """
        Execute full calibration workflow.

        Returns summary dict with keys:
          promoted, demoted, paused, scores, dry_run, timestamp
        """
        logger.info(
            "CalibrationLoop.run() — dry_run=%s days=%d", self.dry_run, self.days
        )

        if self._calibrator is None:
            logger.error("No calibrator available — aborting")
            return {}

        # --- Step 1-5: delegate to WeeklyCalibrator ---
        try:
            result = self._calibrator.run()
        except Exception as exc:
            logger.exception("WeeklyCalibrator.run() failed: %s", exc)
            self._send_telegram(f"[CALIBRATION ERROR] {exc}")
            return {}

        # --- Step 6: generate report ---
        report_md = self._generate_report(result)

        # --- Step 7: send Telegram ---
        self._send_telegram_summary(report_md)

        return result

    # ------------------------------------------------------------------
    # Force promote / demote
    # ------------------------------------------------------------------
    def _force_demote(self, symbol: str, strategy: str):
        """
        Manually demote a lane regardless of its score.
        Useful for bad-actor lanes that need immediate attention.
        """
        logger.warning(
            "FORCE DEMOTE — symbol=%s strategy=%s dry_run=%s",
            symbol, strategy, self.dry_run,
        )
        if self.dry_run:
            print(f"[DRY RUN] Would demote lane: {symbol} / {strategy}")
            return

        if self._calibrator and hasattr(self._calibrator, "force_demote"):
            self._calibrator.force_demote(symbol, strategy)
            msg = f"[FORCED DEMOTE] Lane {symbol}/{strategy} demoted by manual override"
            logger.info(msg)
            self._send_telegram(msg)
        else:
            # Fallback: direct DB update
            import sqlite3

            db_path = ROOT / "db" / "gb_brain.db"
            conn    = sqlite3.connect(db_path)
            try:
                conn.execute(
                    """
                    UPDATE lanes
                    SET    status = 'paused',
                           updated_at = ?
                    WHERE  symbol   = ?
                      AND  strategy = ?
                    """,
                    (datetime.utcnow().isoformat(), symbol.upper(), strategy.lower()),
                )
                affected = conn.execute("SELECT changes()").fetchone()[0]
                conn.commit()
                if affected:
                    msg = f"[FORCED DEMOTE] Lane {symbol}/{strategy} → paused (direct DB)"
                    logger.info(msg)
                    self._send_telegram(msg)
                else:
                    logger.warning("force_demote: no lane found for %s / %s", symbol, strategy)
            finally:
                conn.close()

    def _force_promote(self, symbol: str, strategy: str):
        """
        Manually promote a lane after manual review.
        """
        logger.info(
            "FORCE PROMOTE — symbol=%s strategy=%s dry_run=%s",
            symbol, strategy, self.dry_run,
        )
        if self.dry_run:
            print(f"[DRY RUN] Would promote lane: {symbol} / {strategy}")
            return

        if self._calibrator and hasattr(self._calibrator, "force_promote"):
            self._calibrator.force_promote(symbol, strategy)
            msg = f"[FORCED PROMOTE] Lane {symbol}/{strategy} promoted by manual override"
            logger.info(msg)
            self._send_telegram(msg)
        else:
            import sqlite3

            db_path = ROOT / "db" / "gb_brain.db"
            conn    = sqlite3.connect(db_path)
            try:
                conn.execute(
                    """
                    UPDATE lanes
                    SET    status = 'confirmed',
                           updated_at = ?
                    WHERE  symbol   = ?
                      AND  strategy = ?
                    """,
                    (datetime.utcnow().isoformat(), symbol.upper(), strategy.lower()),
                )
                affected = conn.execute("SELECT changes()").fetchone()[0]
                conn.commit()
                if affected:
                    msg = f"[FORCED PROMOTE] Lane {symbol}/{strategy} → confirmed (direct DB)"
                    logger.info(msg)
                    self._send_telegram(msg)
                else:
                    logger.warning("force_promote: no lane found for %s / %s", symbol, strategy)
            finally:
                conn.close()

    # ------------------------------------------------------------------
    # Report generation
    # ------------------------------------------------------------------
    def _generate_report(self, result: dict) -> str:
        """
        Build a markdown-formatted calibration report and save it to
        monitor/reports/calibration_YYYYMMDD.md.

        Returns the report string.
        """
        now       = datetime.utcnow()
        date_str  = now.strftime("%Y%m%d")
        ts_str    = now.strftime("%Y-%m-%d %H:%M UTC")
        file_name = f"calibration_{date_str}.md"
        file_path = REPORTS_DIR / file_name

        promoted = result.get("promoted", [])
        demoted  = result.get("demoted",  [])
        paused   = result.get("paused",   [])
        scores   = result.get("scores",   {})

        lines = [
            f"# GB-BRAIN Calibration Report",
            f"",
            f"**Generated:** {ts_str}  ",
            f"**Lookback:** {self.days} days  ",
            f"**Dry Run:** {'YES — no changes committed' if self.dry_run else 'NO — changes applied'}",
            f"",
            f"---",
            f"",
            f"## Summary",
            f"",
            f"| Category | Count |",
            f"|----------|-------|",
            f"| Promoted (candidate → confirmed) | {len(promoted)} |",
            f"| Demoted  (confirmed → paused)    | {len(demoted)}  |",
            f"| Paused   (broken / no signals)   | {len(paused)}   |",
            f"",
        ]

        if promoted:
            lines += ["## Promoted Lanes", ""]
            for lane in promoted:
                sym  = lane.get("symbol", "?")
                strat = lane.get("strategy", "?")
                score = lane.get("score", "N/A")
                lines.append(f"- **{sym} / {strat}** — score: {score}")
            lines.append("")

        if demoted:
            lines += ["## Demoted Lanes", ""]
            for lane in demoted:
                sym  = lane.get("symbol", "?")
                strat = lane.get("strategy", "?")
                score = lane.get("score", "N/A")
                reason = lane.get("reason", "")
                lines.append(f"- **{sym} / {strat}** — score: {score}  reason: {reason}")
            lines.append("")

        if paused:
            lines += ["## Paused Lanes", ""]
            for lane in paused:
                sym  = lane.get("symbol", "?")
                strat = lane.get("strategy", "?")
                reason = lane.get("reason", "")
                lines.append(f"- **{sym} / {strat}** — {reason}")
            lines.append("")

        if scores:
            lines += ["## Lane Scores", ""]
            lines.append("| Symbol | Strategy | Score | Status |")
            lines.append("|--------|----------|-------|--------|")
            for key, info in sorted(scores.items()):
                if isinstance(info, dict):
                    sym   = info.get("symbol", key)
                    strat = info.get("strategy", "")
                    sc    = info.get("score", "N/A")
                    st    = info.get("status", "")
                else:
                    sym, strat, sc, st = key, "", info, ""
                lines.append(f"| {sym} | {strat} | {sc} | {st} |")
            lines.append("")

        lines += [
            "---",
            "",
            f"*Report saved to: monitor/reports/{file_name}*",
        ]

        report_md = "\n".join(lines)

        try:
            file_path.write_text(report_md, encoding="utf-8")
            logger.info("Calibration report saved to %s", file_path)
        except Exception as exc:
            logger.error("Failed to save report: %s", exc)

        return report_md

    # ------------------------------------------------------------------
    # Telegram
    # ------------------------------------------------------------------
    def _send_telegram_summary(self, report_md: str):
        """
        Send a concise Telegram summary (not the full markdown report).
        Telegram has a 4096-char limit; truncate if needed.
        """
        MAX_LEN = 3800

        # Extract first few meaningful lines as the summary
        lines   = [ln.strip() for ln in report_md.splitlines() if ln.strip()]
        summary_lines = lines[:30]  # first 30 non-blank lines
        summary = "\n".join(summary_lines)

        if len(summary) > MAX_LEN:
            summary = summary[:MAX_LEN] + "\n…(truncated)"

        self._send_telegram(summary)

    def _send_telegram(self, message: str):
        if self._send_alert:
            try:
                self._send_alert(message)
            except Exception as exc:
                logger.warning("Telegram send failed: %s", exc)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="GB-BRAIN Calibration Loop — weekly lane scoring and state transitions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument(
        "--dry-run", action="store_true",
        help="Compute changes but do NOT commit to database",
    )
    p.add_argument(
        "--days", type=int, default=7,
        help="Lookback window in days (default 7)",
    )
    p.add_argument(
        "--force-demote", nargs=2, metavar=("SYMBOL", "STRATEGY"),
        help="Force-demote a specific lane, e.g. --force-demote ETH parallax",
    )
    p.add_argument(
        "--force-promote", nargs=2, metavar=("SYMBOL", "STRATEGY"),
        help="Force-promote a specific lane after manual review",
    )
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

    loop = CalibrationLoop(dry_run=args.dry_run, days=args.days)

    if args.force_demote:
        symbol, strategy = args.force_demote
        loop._force_demote(symbol, strategy)
        return

    if args.force_promote:
        symbol, strategy = args.force_promote
        loop._force_promote(symbol, strategy)
        return

    result = loop.run()
    if result:
        print(f"Calibration complete — promoted={len(result.get('promoted', []))}, "
              f"demoted={len(result.get('demoted', []))}, "
              f"paused={len(result.get('paused', []))}")


if __name__ == "__main__":
    main()
