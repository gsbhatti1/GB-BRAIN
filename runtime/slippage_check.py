"""
GB-BRAIN — Slippage Check
===========================
Quick CLI tool to check slippage on recent demo/live fills.
Reads from SQLite, no exchange API needed.

Usage:
    python runtime/slippage_check.py                 # All brokers, 7 days
    python runtime/slippage_check.py --broker oanda
    python runtime/slippage_check.py --days 30
"""

import argparse
import logging
import sqlite3
import sys
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv

load_dotenv(ROOT / ".env")

logger = logging.getLogger("gb_brain.slippage_check")

DB_PATH = ROOT / "db" / "gb_brain.db"

# Thresholds that trigger a WARNING flag
WARN_AVG_SLIP_PTS = 5.0   # points
WARN_FILL_RATE    = 80.0  # percent


def _get_cutoff(days: int) -> str:
    return (datetime.utcnow() - timedelta(days=days)).isoformat()


def _load_fills(broker: str | None, cutoff: str) -> list[dict]:
    """
    Load fills from live_trades where source in ('demo', 'live') within the cutoff.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        # Verify table exists
        exists = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='live_trades'"
        ).fetchone()
        if not exists:
            logger.warning("live_trades table does not exist — no data to show")
            return []

        params: list = ["demo", "live", cutoff]
        query = """
            SELECT broker, symbol,
                   slippage_pts, slippage_pct,
                   signal_price, fill_price,
                   run_at
            FROM   live_trades
            WHERE  source IN (?, ?)
              AND  run_at >= ?
        """
        if broker:
            query += " AND broker = ?"
            params.append(broker)
        rows = conn.execute(query, params).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def _load_signals_count(broker: str | None, cutoff: str) -> dict[tuple, int]:
    """
    Returns {(broker, symbol): signal_count} from observed_signals.
    Falls back to empty dict if table is absent.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        exists = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='observed_signals'"
        ).fetchone()
        if not exists:
            return {}

        params: list = [cutoff]
        query = """
            SELECT broker, symbol, COUNT(*) AS cnt
            FROM   observed_signals
            WHERE  observed_at >= ?
        """
        if broker:
            query += " AND broker = ?"
            params.append(broker)
        query += " GROUP BY broker, symbol"
        rows = conn.execute(query, params).fetchall()
        return {(r["broker"], r["symbol"]): r["cnt"] for r in rows}
    finally:
        conn.close()


def _compute_stats(
    fills: list[dict],
    sig_counts: dict[tuple, int],
) -> list[dict]:
    """
    GROUP BY broker, symbol.
    Returns list of row dicts with: broker, symbol, fills, avg_slip_pts,
    avg_slip_pct, max_slip_pts, max_slip_pct, fill_rate, warn.
    """
    from collections import defaultdict

    groups: dict[tuple, list] = defaultdict(list)
    for f in fills:
        key = (f.get("broker", "?"), f.get("symbol", "?"))
        groups[key].append(f)

    rows = []
    for (broker, symbol), group in sorted(groups.items()):
        fill_count = len(group)

        slip_pts_list = [
            abs(float(f["slippage_pts"]))
            for f in group
            if f.get("slippage_pts") is not None
        ]
        slip_pct_list = [
            abs(float(f["slippage_pct"]))
            for f in group
            if f.get("slippage_pct") is not None
        ]

        avg_slip_pts = round(sum(slip_pts_list) / len(slip_pts_list), 4) if slip_pts_list else 0.0
        avg_slip_pct = round(sum(slip_pct_list) / len(slip_pct_list), 4) if slip_pct_list else 0.0
        max_slip_pts = round(max(slip_pts_list), 4) if slip_pts_list else 0.0
        max_slip_pct = round(max(slip_pct_list), 4) if slip_pct_list else 0.0

        # Fill rate: fills / signals * 100 (if signals known)
        sig_key    = (broker, symbol)
        sig_count  = sig_counts.get(sig_key)
        if sig_count and sig_count > 0:
            fill_rate = round(fill_count / sig_count * 100, 1)
        else:
            fill_rate = None  # unknown

        warn = (
            avg_slip_pts > WARN_AVG_SLIP_PTS
            or (fill_rate is not None and fill_rate < WARN_FILL_RATE)
        )

        rows.append(
            {
                "broker":       broker,
                "symbol":       symbol,
                "fills":        fill_count,
                "signals":      sig_count if sig_count else "N/A",
                "avg_slip_pts": avg_slip_pts,
                "avg_slip_pct": avg_slip_pct,
                "max_slip_pts": max_slip_pts,
                "max_slip_pct": max_slip_pct,
                "fill_rate":    fill_rate,
                "warn":         warn,
            }
        )
    return rows


def _print_table(rows: list[dict], days: int, broker: str | None):
    """Pretty-print the slippage check table."""
    print("\n" + "=" * 90)
    print(f"  GB-BRAIN Slippage Check  |  Last {days} days  |  broker={broker or 'ALL'}")
    print("=" * 90)

    if not rows:
        print("  No fill data found for the specified parameters.")
        print("=" * 90 + "\n")
        return

    hdr = (
        f"  {'Broker':<10} {'Symbol':<12} {'Fills':>6} {'Signals':>8} "
        f"{'Avg Slip Pts':>13} {'Max Slip Pts':>13} "
        f"{'Avg Slip%':>10} {'Fill Rate':>10}  Status"
    )
    print(hdr)
    print("  " + "-" * 86)

    warn_rows = []
    for r in rows:
        fill_rate_str = f"{r['fill_rate']:.1f}%" if r["fill_rate"] is not None else " N/A"
        status = "WARNING" if r["warn"] else "OK"
        line = (
            f"  {r['broker']:<10} {r['symbol']:<12} {r['fills']:>6} {str(r['signals']):>8} "
            f"{r['avg_slip_pts']:>13.4f} {r['max_slip_pts']:>13.4f} "
            f"{r['avg_slip_pct']:>9.4f}% {fill_rate_str:>10}  {status}"
        )
        print(line)
        if r["warn"]:
            warn_rows.append(r)

    print("=" * 90)

    if warn_rows:
        print(f"\n  *** WARNING THRESHOLDS: avg_slip_pts > {WARN_AVG_SLIP_PTS} or fill_rate < {WARN_FILL_RATE}% ***")
        for r in warn_rows:
            reasons = []
            if r["avg_slip_pts"] > WARN_AVG_SLIP_PTS:
                reasons.append(f"avg_slip_pts={r['avg_slip_pts']:.4f} > {WARN_AVG_SLIP_PTS}")
            if r["fill_rate"] is not None and r["fill_rate"] < WARN_FILL_RATE:
                reasons.append(f"fill_rate={r['fill_rate']:.1f}% < {WARN_FILL_RATE}%")
            print(f"  ! {r['broker']} {r['symbol']}: {' | '.join(reasons)}")

    print()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="GB-BRAIN Slippage Check — quick slippage summary from SQLite",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--broker", help="Filter by broker name (e.g. oanda, blofin)")
    p.add_argument("--days",   type=int, default=7, help="Lookback window in days (default 7)")
    p.add_argument(
        "--log-level",
        default="WARNING",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging verbosity (default WARNING — keeps output clean)",
    )
    return p


def main():
    args = _build_parser().parse_args()
    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    cutoff     = _get_cutoff(args.days)
    fills      = _load_fills(args.broker, cutoff)
    sig_counts = _load_signals_count(args.broker, cutoff)
    rows       = _compute_stats(fills, sig_counts)

    _print_table(rows, args.days, args.broker)


if __name__ == "__main__":
    main()
