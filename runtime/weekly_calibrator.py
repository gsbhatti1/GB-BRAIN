"""
GB-BRAIN — Weekly Calibrator
==============================
Reads observed_signals + live_trades from SQLite.
Promotes strong lanes to "confirmed", demotes weak ones, pauses broken ones.
Writes results back to config/gb_strategy_gems.json.

Run weekly (every Sunday or Monday morning).

Usage:
    python runtime/weekly_calibrator.py
    python runtime/weekly_calibrator.py --dry-run   # Show what would change
    python runtime/weekly_calibrator.py --days 14   # Look back 14 days

Promotion threshold:
    composite_score >= 0.65  AND  total_trades >= 30  AND  win_rate >= 55%

Demotion threshold:
    win_rate < 40%  OR  profit_factor < 0.9

Conventions:
    - SQLite is truth — read from db/gb_brain.db, write to config/gb_strategy_gems.json
    - Capital is priority — paused lanes block all order routing
    - .env for secrets — no credentials needed here
    - Deterministic — same DB state → same calibration output
"""

from __future__ import annotations

import argparse
import json
import logging
import sqlite3
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# ROOT path (project root = two levels up from this file)
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Logger
# ---------------------------------------------------------------------------
logger = logging.getLogger("gb_brain.calibrator")

# ---------------------------------------------------------------------------
# Thresholds
# ---------------------------------------------------------------------------
PROMOTE_MIN_SCORE       = 0.65
PROMOTE_MIN_TRADES      = 30
PROMOTE_MIN_WIN_RATE    = 55.0   # percent
DEMOTE_MAX_WIN_RATE     = 40.0   # percent
DEMOTE_MAX_PF           = 0.9    # profit_factor


# ---------------------------------------------------------------------------
# WeeklyCalibrator
# ---------------------------------------------------------------------------

class WeeklyCalibrator:
    """
    Reads signal and trade statistics from SQLite, computes composite scores,
    and updates status fields in config/gb_strategy_gems.json.

    Parameters
    ----------
    lookback_days : int  Number of days of data to analyse. Default 7.
    dry_run       : bool If True, compute and print without writing any files.
    """

    def __init__(
        self,
        lookback_days: int = 7,
        dry_run: bool = False,
    ) -> None:
        self.lookback_days = lookback_days
        self.dry_run = dry_run
        self._db_path   = ROOT / "db" / "gb_brain.db"
        self._gems_path = ROOT / "config" / "gb_strategy_gems.json"
        self._report_lines: list[str] = []

        logger.info(
            "WeeklyCalibrator init | lookback=%dd dry_run=%s db=%s gems=%s",
            self.lookback_days, self.dry_run, self._db_path, self._gems_path,
        )

    # ------------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------------

    def run(self) -> dict:
        """
        Main calibration cycle:

        1. Load current gems from JSON
        2. Query observed_signals and live_trades from SQLite
        3. Score each symbol × strategy lane
        4. Promote / demote entries
        5. Save updated gems (unless dry_run)
        6. Print report

        Returns
        -------
        dict  Updated gems payload (regardless of dry_run).
        """
        logger.info("=== Weekly Calibrator START (lookback=%dd) ===", self.lookback_days)

        # Load gems
        gems = self._load_gems()

        # Query stats
        signal_stats = self._load_signal_stats(self.lookback_days)
        trade_stats  = self._load_trade_stats(self.lookback_days)

        # Walk every strategy + symbol combo in gems
        changes: list[dict] = []
        for strategy_name, strategy_block in gems.items():
            if strategy_name.startswith("_"):
                continue   # skip _meta, _description keys
            if not isinstance(strategy_block, dict):
                continue
            for symbol, entry in strategy_block.items():
                if symbol.startswith("_") or not isinstance(entry, dict):
                    continue

                sig_stats   = signal_stats.get((symbol, strategy_name), {})
                trd_stats   = trade_stats.get((symbol, strategy_name), {})
                score       = self._score_lane(sig_stats, trd_stats)
                old_status  = entry.get("status", "candidate")

                new_status = self._determine_status(entry, score, sig_stats, trd_stats)

                if new_status != old_status:
                    changes.append({
                        "strategy":   strategy_name,
                        "symbol":     symbol,
                        "old_status": old_status,
                        "new_status": new_status,
                        "score":      round(score, 4),
                        "win_rate":   trd_stats.get("win_rate", 0.0),
                        "trades":     trd_stats.get("total_trades", 0),
                        "pf":         trd_stats.get("profit_factor", 0.0),
                    })

                    if new_status == "confirmed":
                        self._promote(entry, score)
                    elif new_status == "paused":
                        self._demote(entry, score)
                    else:
                        entry["status"] = new_status

                # Attach calibration metadata to the entry
                if not self.dry_run:
                    entry.setdefault("calibration", {})
                    entry["calibration"].update({
                        "last_score":   round(score, 4),
                        "last_run":     datetime.now(tz=timezone.utc).strftime("%Y-%m-%d"),
                        "lookback_days": self.lookback_days,
                        "total_signals": sig_stats.get("total_signals", 0),
                        "total_trades":  trd_stats.get("total_trades", 0),
                        "win_rate":      round(trd_stats.get("win_rate", 0.0), 2),
                        "profit_factor": round(trd_stats.get("profit_factor", 0.0), 4),
                    })

        # Update meta
        if not self.dry_run:
            gems["_meta"]["last_updated"] = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")

        self._print_report(signal_stats, trade_stats, changes)

        if self.dry_run:
            logger.info("[DRY-RUN] No files written.")
        else:
            self._save_gems(gems)

        logger.info("=== Weekly Calibrator DONE | %d status changes ===", len(changes))
        return gems

    # ------------------------------------------------------------------
    # Data loading
    # ------------------------------------------------------------------

    def _load_gems(self) -> dict:
        """Load gb_strategy_gems.json. Returns empty dict on error."""
        if not self._gems_path.exists():
            logger.warning("gems file not found: %s — starting empty.", self._gems_path)
            return {"_meta": {}}
        try:
            with open(self._gems_path, "r", encoding="utf-8") as fh:
                return json.load(fh)
        except (json.JSONDecodeError, OSError) as exc:
            logger.error("Failed to load gems file: %s", exc)
            return {"_meta": {}}

    def _load_signal_stats(self, days: int) -> dict[tuple[str, str], dict]:
        """
        Query observed_signals table aggregated by symbol + strategy.

        Returns
        -------
        dict keyed by (symbol, strategy) with fields:
            total_signals, signal_rate (signals per day), last_signal
        """
        cutoff = (datetime.now(tz=timezone.utc) - timedelta(days=days)).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        sql = """
            SELECT
                symbol,
                strategy,
                COUNT(*)                          AS total_signals,
                CAST(COUNT(*) AS REAL) / ?        AS signal_rate,
                MAX(observed_at)                  AS last_signal
            FROM observed_signals
            WHERE observed_at >= ?
            GROUP BY symbol, strategy
        """
        return self._query_stats(sql, (days, cutoff), ("symbol", "strategy"))

    def _load_trade_stats(self, days: int) -> dict[tuple[str, str], dict]:
        """
        Query live_trades table aggregated by symbol + strategy.

        Expects live_trades to have columns:
          symbol, strategy, pnl (signed P&L per trade), closed_at

        Returns
        -------
        dict keyed by (symbol, strategy) with fields:
            total_trades, win_rate (%), profit_factor, net_pnl
        """
        cutoff = (datetime.now(tz=timezone.utc) - timedelta(days=days)).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        sql = """
            SELECT
                symbol,
                strategy,
                COUNT(*)                                        AS total_trades,
                ROUND(
                    100.0 * SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END)
                    / NULLIF(COUNT(*), 0), 2
                )                                               AS win_rate,
                ROUND(
                    SUM(CASE WHEN pnl > 0 THEN pnl ELSE 0 END)
                    / NULLIF(ABS(SUM(CASE WHEN pnl < 0 THEN pnl ELSE 0 END)), 0),
                4)                                              AS profit_factor,
                ROUND(SUM(pnl), 4)                              AS net_pnl
            FROM live_trades
            WHERE closed_at >= ?
            GROUP BY symbol, strategy
        """
        return self._query_stats(sql, (cutoff,), ("symbol", "strategy"))

    def _query_stats(
        self,
        sql: str,
        params: tuple,
        key_cols: tuple[str, str],
    ) -> dict[tuple[str, str], dict]:
        """Execute a SQL query against the GB-BRAIN SQLite database."""
        result: dict[tuple[str, str], dict] = {}
        if not self._db_path.exists():
            logger.warning(
                "DB not found at %s — no stats available. "
                "Run live_observer first to generate data.",
                self._db_path,
            )
            return result
        try:
            with sqlite3.connect(self._db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute(sql, params)
                for row in cursor:
                    row_dict = dict(row)
                    key = (row_dict.get(key_cols[0], ""), row_dict.get(key_cols[1], ""))
                    result[key] = row_dict
        except sqlite3.OperationalError as exc:
            # Table may not exist yet — that's expected on first run
            logger.info("SQLite query skipped (table may not exist yet): %s", exc)
        except sqlite3.Error as exc:
            logger.error("SQLite error in _query_stats: %s", exc)
        return result

    # ------------------------------------------------------------------
    # Scoring
    # ------------------------------------------------------------------

    def _score_lane(
        self,
        signal_stats: dict,
        trade_stats: dict,
    ) -> float:
        """
        Compute composite lane quality score in [0, 1].

        Formula:
            score = signal_rate_norm * win_rate_norm * profit_factor_norm

        Where:
            signal_rate_norm  = min(signal_rate / 10, 1.0)  (cap at 10 signals/day)
            win_rate_norm     = win_rate_pct / 100
            pf_norm           = min(profit_factor / 2.0, 1.0) (cap at PF=2.0)

        A lane with no trade data scores 0.0 (not yet eligible for promotion).

        Returns
        -------
        float  Score in [0.0, 1.0]
        """
        if not trade_stats:
            return 0.0

        win_rate_pct   = float(trade_stats.get("win_rate", 0.0) or 0.0)
        profit_factor  = float(trade_stats.get("profit_factor", 0.0) or 0.0)
        signal_rate    = float(signal_stats.get("signal_rate", 0.0) or 0.0)

        win_rate_norm  = win_rate_pct / 100.0
        pf_norm        = min(profit_factor / 2.0, 1.0)
        sig_rate_norm  = min(signal_rate / 10.0, 1.0)

        score = sig_rate_norm * win_rate_norm * pf_norm
        return round(score, 6)

    def _determine_status(
        self,
        entry: dict,
        score: float,
        signal_stats: dict,
        trade_stats: dict,
    ) -> str:
        """
        Determine the new status for a gem entry.

        Priority:
          1. Demote to "paused" if demotion thresholds exceeded
          2. Promote to "confirmed" if promotion thresholds met
          3. Keep current status

        Parameters
        ----------
        entry       : dict  Current gem entry
        score       : float Composite score
        signal_stats: dict
        trade_stats : dict
        """
        current_status = entry.get("status", "candidate")
        total_trades   = int(trade_stats.get("total_trades", 0) or 0)
        win_rate       = float(trade_stats.get("win_rate", 0.0) or 0.0)
        pf             = float(trade_stats.get("profit_factor", 0.0) or 0.0)

        # ── Demotion check (highest priority) ───────────────────────────────
        if total_trades >= 10:   # Need enough data before demoting
            if win_rate < DEMOTE_MAX_WIN_RATE or (pf > 0 and pf < DEMOTE_MAX_PF):
                return "paused"

        # ── Promotion check ──────────────────────────────────────────────────
        if (
            current_status in ("candidate", "paused")
            and score >= PROMOTE_MIN_SCORE
            and total_trades >= PROMOTE_MIN_TRADES
            and win_rate >= PROMOTE_MIN_WIN_RATE
        ):
            return "confirmed"

        # Re-evaluate paused → candidate if demotion no longer triggered
        if current_status == "paused" and total_trades >= 10:
            if win_rate >= DEMOTE_MAX_WIN_RATE and (pf == 0 or pf >= DEMOTE_MAX_PF):
                return "candidate"

        return current_status

    # ------------------------------------------------------------------
    # Promote / Demote
    # ------------------------------------------------------------------

    def _promote(self, entry: dict, score: float) -> None:
        """
        Set entry status to "confirmed".

        Criteria (enforced by _determine_status before calling):
            score >= 0.65  AND  trades >= 30  AND  win_rate >= 55%

        Parameters
        ----------
        entry : dict  Gem entry dict (mutated in place)
        score : float Composite score at time of promotion
        """
        entry["status"] = "confirmed"
        entry.setdefault("promotion", {})
        entry["promotion"].update({
            "promoted_at": datetime.now(tz=timezone.utc).strftime("%Y-%m-%d"),
            "score_at_promotion": round(score, 4),
        })
        logger.info(
            "PROMOTED → confirmed | score=%.4f | entry=%s",
            score, entry.get("promotion", {}),
        )

    def _demote(self, entry: dict, score: float) -> None:
        """
        Set entry status to "paused".

        Criteria (enforced by _determine_status before calling):
            win_rate < 40%  OR  profit_factor < 0.9

        Parameters
        ----------
        entry : dict  Gem entry dict (mutated in place)
        score : float Composite score at time of demotion
        """
        entry["status"] = "paused"
        entry.setdefault("demotion", {})
        entry["demotion"].update({
            "paused_at":  datetime.now(tz=timezone.utc).strftime("%Y-%m-%d"),
            "score_at_pause": round(score, 4),
        })
        logger.warning(
            "DEMOTED → paused | score=%.4f | entry=%s",
            score, entry.get("demotion", {}),
        )

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def _save_gems(self, updated_gems: dict) -> None:
        """
        Write the updated gems payload back to config/gb_strategy_gems.json.

        Creates a .bak backup of the previous file before overwriting.

        Parameters
        ----------
        updated_gems : dict  Full gems payload to serialize
        """
        try:
            # Backup existing file
            if self._gems_path.exists():
                bak_path = self._gems_path.with_suffix(".json.bak")
                bak_path.write_bytes(self._gems_path.read_bytes())
                logger.debug("Backup written to %s.", bak_path)

            self._gems_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self._gems_path, "w", encoding="utf-8") as fh:
                json.dump(updated_gems, fh, indent=2)
            logger.info("Gems saved to %s.", self._gems_path)

        except OSError as exc:
            logger.error("Failed to save gems file: %s", exc)

    # ------------------------------------------------------------------
    # Reporting
    # ------------------------------------------------------------------

    def _print_report(
        self,
        signal_stats: dict,
        trade_stats: dict,
        changes: list[dict],
    ) -> None:
        """
        Print a formatted summary table to stdout and logger.

        Shows per-lane stats and any status changes.
        """
        now_utc = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        sep     = "=" * 88
        lines: list[str] = [
            "",
            sep,
            f"  GB-BRAIN Weekly Calibrator Report — {now_utc}",
            f"  Lookback: {self.lookback_days}d | dry_run={self.dry_run}",
            sep,
        ]

        # ── Signal stats table ───────────────────────────────────────────────
        if signal_stats:
            lines.append(f"\n  {'SYMBOL':<10} {'STRATEGY':<12} {'SIGNALS':<10} {'SIG/DAY':<10} {'LAST SIGNAL'}")
            lines.append("  " + "-" * 70)
            for (symbol, strategy), s in sorted(signal_stats.items()):
                lines.append(
                    f"  {symbol:<10} {strategy:<12} "
                    f"{s.get('total_signals', 0):<10} "
                    f"{s.get('signal_rate', 0.0):<10.2f} "
                    f"{s.get('last_signal', 'n/a')}"
                )
        else:
            lines.append("\n  No signal data in observed_signals (run live_observer first).")

        # ── Trade stats table ────────────────────────────────────────────────
        lines.append("")
        if trade_stats:
            lines.append(
                f"  {'SYMBOL':<10} {'STRATEGY':<12} {'TRADES':<8} {'WIN%':<8} {'PF':<8} {'NET PNL':<10} {'SCORE'}"
            )
            lines.append("  " + "-" * 70)
            for (symbol, strategy), t in sorted(trade_stats.items()):
                sig = signal_stats.get((symbol, strategy), {})
                score = self._score_lane(sig, t)
                lines.append(
                    f"  {symbol:<10} {strategy:<12} "
                    f"{t.get('total_trades', 0):<8} "
                    f"{t.get('win_rate', 0.0):<8.1f} "
                    f"{t.get('profit_factor', 0.0):<8.4f} "
                    f"{t.get('net_pnl', 0.0):<10.4f} "
                    f"{score:.4f}"
                )
        else:
            lines.append("  No trade data in live_trades (run paper/demo trades first).")

        # ── Status changes ───────────────────────────────────────────────────
        lines.append("")
        if changes:
            lines.append(f"  STATUS CHANGES ({len(changes)}):")
            lines.append("  " + "-" * 70)
            for c in changes:
                arrow = "↑ PROMOTED" if c["new_status"] == "confirmed" else "↓ DEMOTED "
                lines.append(
                    f"  {arrow} | {c['strategy']:<12} {c['symbol']:<10} "
                    f"{c['old_status']:>10} → {c['new_status']:<10} | "
                    f"score={c['score']:.4f} wr={c['win_rate']:.1f}% "
                    f"trades={c['trades']} pf={c['pf']:.4f}"
                )
        else:
            lines.append("  No status changes this cycle.")

        lines.append(sep)
        lines.append("")

        report = "\n".join(lines)
        print(report)
        self._report_lines = lines
        logger.info("Report printed (%d lines).", len(lines))


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="GB-BRAIN Weekly Calibrator — promote/demote strategy GEMs.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="Compute and print results without modifying gb_strategy_gems.json.",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=7,
        help="Number of lookback days for statistics. Use 14 for two-week view.",
    )
    return parser.parse_args(argv)


def _setup_logging(level: int = logging.INFO) -> None:
    log_dir = ROOT / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(log_dir / "calibrator.log", encoding="utf-8"),
        ],
    )


if __name__ == "__main__":
    _setup_logging()
    args = _parse_args()
    calibrator = WeeklyCalibrator(
        lookback_days=args.days,
        dry_run=args.dry_run,
    )
    calibrator.run()
