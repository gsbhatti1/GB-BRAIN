"""
GB-BRAIN — Score & Sort
=========================
Reads backtest results from SQLite, computes composite scores,
classifies strategies (GEM / PASS / TRASH), and moves files.

Usage:
    python backtest/score_and_sort.py
    python backtest/score_and_sort.py --report    # Also generate Excel
"""

import sys
import json
import shutil
import argparse
from pathlib import Path
from datetime import datetime

import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import PatternFill, Font, Alignment

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from config.settings import (
    GEM_WIN_RATE, PASS_WIN_RATE, SCORE_WEIGHTS, MIN_TRADES,
    BEST_DIR, ARCHIVE_DIR, STAGING_DIR,
)
from db.brain_db import connect, update_strategy_status


def compute_composite_score(row):
    """Weighted composite score. Higher = better."""
    w = SCORE_WEIGHTS
    score = (
        (row.get("win_rate", 0) or 0) * w["win_rate"]
        + (row.get("total_return", 0) or 0) * w["total_return"]
        + (row.get("profit_factor", 0) or 0) * w["profit_factor"] * 10  # Scale PF
        + min((row.get("total_trades", 0) or 0), 200) / 200 * 100 * w["trade_count"]
    )
    return round(score, 2)


def classify(win_rate, total_return, profit_factor):
    """Classify a strategy based on metrics."""
    if win_rate >= GEM_WIN_RATE and total_return > 0 and profit_factor > 1.0:
        return "GEM"
    if win_rate < PASS_WIN_RATE or total_return < -20:
        return "TRASH"
    return "PASS"


def run_scoring(generate_report=False):
    """Score all backtest results and classify strategies."""
    conn = connect()

    # Get aggregated results per strategy (best result per strategy)
    df = pd.read_sql(
        """
        SELECT
            s.id as strategy_id,
            s.name as strategy_name,
            s.category,
            s.source_file,
            s.indicators,
            br.symbol,
            br.timeframe,
            br.total_trades,
            br.win_rate,
            br.total_return,
            br.max_drawdown,
            br.profit_factor,
            br.sharpe_ratio
        FROM backtest_results br
        JOIN strategies s ON s.id = br.strategy_id
        WHERE br.total_trades >= ?
        ORDER BY br.win_rate DESC
        """,
        conn,
        params=(MIN_TRADES,),
    )

    if df.empty:
        print("[INFO] No backtest results to score.")
        conn.close()
        return

    # Compute scores
    df["composite_score"] = df.apply(compute_composite_score, axis=1)
    df["status"] = df.apply(
        lambda r: classify(r["win_rate"], r["total_return"], r["profit_factor"]),
        axis=1,
    )
    df = df.sort_values("composite_score", ascending=False)

    # Update database
    print("Updating database with scores...")
    for _, row in df.iterrows():
        conn.execute(
            """UPDATE backtest_results SET composite_score = ?, status = ?
               WHERE strategy_id = ? AND symbol = ? AND timeframe = ?""",
            (row["composite_score"], row["status"],
             row["strategy_id"], row["symbol"], row["timeframe"]),
        )

    # Per-strategy best classification
    best_per_strat = df.groupby("strategy_id").agg({
        "composite_score": "max",
        "win_rate": "max",
        "total_return": "max",
        "status": lambda x: "GEM" if "GEM" in x.values else ("PASS" if "PASS" in x.values else "TRASH"),
    }).reset_index()

    for _, row in best_per_strat.iterrows():
        update_strategy_status(conn, row["strategy_id"], row["status"].lower())

    conn.commit()

    # Move files
    gems = best_per_strat[best_per_strat["status"] == "GEM"]
    trash = best_per_strat[best_per_strat["status"] == "TRASH"]

    gem_count = 0
    trash_count = 0

    for _, row in gems.iterrows():
        strat = conn.execute(
            "SELECT source_file, category FROM strategies WHERE id = ?",
            (row["strategy_id"],),
        ).fetchone()
        if strat and strat["source_file"]:
            src = Path(strat["source_file"])
            if src.exists():
                cat = strat["category"] or "crypto"
                dest_dir = BEST_DIR / cat
                dest_dir.mkdir(parents=True, exist_ok=True)
                dest = dest_dir / src.name
                shutil.copy2(src, dest)
                gem_count += 1

    for _, row in trash.iterrows():
        strat = conn.execute(
            "SELECT source_file FROM strategies WHERE id = ?",
            (row["strategy_id"],),
        ).fetchone()
        if strat and strat["source_file"]:
            src = Path(strat["source_file"])
            if src.exists():
                dest = ARCHIVE_DIR / src.name
                shutil.copy2(src, dest)
                trash_count += 1

    conn.close()

    # Summary
    status_counts = df["status"].value_counts()
    print(f"\n{'=' * 60}")
    print("SCORING COMPLETE")
    print(f"  Total results scored: {len(df):,}")
    print(f"  GEM:   {status_counts.get('GEM', 0):,}")
    print(f"  PASS:  {status_counts.get('PASS', 0):,}")
    print(f"  TRASH: {status_counts.get('TRASH', 0):,}")
    print(f"  Files moved to best/:    {gem_count}")
    print(f"  Files moved to archive/: {trash_count}")
    print(f"{'=' * 60}")

    # Generate Excel report
    if generate_report:
        report_path = generate_excel_report(df)
        print(f"\n  Excel report: {report_path}")

    return df


def generate_excel_report(df):
    """Generate a color-coded Excel ranking report."""
    report_dir = ROOT / "monitor" / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = report_dir / f"strategy_rankings_{ts}.xlsx"

    wb = Workbook()
    ws = wb.active
    ws.title = "Rankings"

    cols = [
        "strategy_name", "category", "symbol", "timeframe",
        "total_trades", "win_rate", "total_return", "max_drawdown",
        "profit_factor", "sharpe_ratio", "composite_score", "status",
    ]

    # Header
    header_fill = PatternFill(start_color="1F2937", end_color="1F2937", fill_type="solid")
    header_font = Font(color="FFFFFF", bold=True, size=10)
    for ci, col in enumerate(cols, 1):
        cell = ws.cell(row=1, column=ci, value=col.replace("_", " ").title())
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center")

    # Data rows
    gem_fill = PatternFill(start_color="D1FAE5", end_color="D1FAE5", fill_type="solid")
    pass_fill = PatternFill(start_color="FEF3C7", end_color="FEF3C7", fill_type="solid")
    trash_fill = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")

    for ri, (_, row) in enumerate(df.head(500).iterrows(), 2):
        status = row.get("status", "PASS")
        fill = gem_fill if status == "GEM" else trash_fill if status == "TRASH" else pass_fill

        for ci, col in enumerate(cols, 1):
            val = row.get(col, "")
            cell = ws.cell(row=ri, column=ci, value=val)
            cell.fill = fill

    # Auto-width
    for ci in range(1, len(cols) + 1):
        ws.column_dimensions[chr(64 + min(ci, 26))].width = 18

    wb.save(path)
    return path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GB-BRAIN Score & Sort")
    parser.add_argument("--report", "-r", action="store_true",
                        help="Generate Excel report")
    args = parser.parse_args()

    run_scoring(generate_report=args.report)
