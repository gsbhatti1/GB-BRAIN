r"""
GB-BRAIN — Import Existing Strategies
=======================================
Imports your 4,500+ strategies from Future-Trading into GB-BRAIN.
Reads from 2_translated/ and 2_translated_merged/ folders.
Registers each file in SQLite + copies to strategies/staging/.

Usage:
    python scripts/import_existing.py --source "C:\Users\gsbha\qwen-dev\Future-Trading"
    python scripts/import_existing.py --source "C:\Users\gsbha\qwen-dev\Future-Trading" --dry-run
"""

import os
import sys
import json
import hashlib
import shutil
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from config.settings import STAGING_DIR
from db.brain_db import connect, insert_strategy, insert_harvest_log, init_db


# Keywords for relevance checking
CRYPTO_KEYWORDS = [
    "btc", "eth", "sol", "crypto", "usdt", "binance",
    "bybit", "blofin", "bitcoin", "ethereum", "solana",
    "futures", "perpetual",
]

INDEX_KEYWORDS = [
    "us30", "nas100", "spx500", "spx", "spy", "es", "nq",
    "dow jones", "s&p500", "nasdaq", "index", "cfd",
]


def classify_category(content, filename):
    """Guess crypto vs indices from content and filename."""
    text = (content + " " + filename).lower()
    crypto_hits = sum(1 for k in CRYPTO_KEYWORDS if k in text)
    index_hits = sum(1 for k in INDEX_KEYWORDS if k in text)
    if crypto_hits > index_hits:
        return "crypto"
    if index_hits > crypto_hits:
        return "indices"
    return "crypto"  # default to crypto since most harvested are


def clean_strategy_name(filename):
    """Create a clean name from filename."""
    name = Path(filename).stem
    # Remove common duplicate suffixes
    for suffix in ["_1_1_1", "_1_1", "_1"]:
        if name.endswith(suffix):
            name = name[:-len(suffix)]
            break
    # Limit length
    return name[:120]


def import_strategies(source_dir, dry_run=False):
    """Import strategies from Future-Trading folders."""
    source = Path(source_dir)

    if not source.exists():
        print(f"[ERROR] Source directory not found: {source}")
        print(f"  Make sure the path is correct.")
        return

    # Find strategy files in these folders
    search_dirs = []
    for folder in ["2_translated", "2_translated_merged"]:
        d = source / folder
        if d.exists():
            search_dirs.append(d)
            print(f"[FOUND] {d} — {len(list(d.glob('*.md')))} .md files")

    # Also check for Python files
    for folder in ["engine", "strategies"]:
        d = source / folder
        if d.exists():
            py_count = len(list(d.rglob("*.py")))
            if py_count > 0:
                search_dirs.append(d)
                print(f"[FOUND] {d} — {py_count} .py files")

    # Also check pine scripts
    pine_dir = source / "6_pine_scripts"
    if pine_dir.exists():
        search_dirs.append(pine_dir)
        pine_count = len(list(pine_dir.rglob("*.pine")))
        print(f"[FOUND] {pine_dir} — {pine_count} .pine files")

    if not search_dirs:
        print("[ERROR] No strategy folders found in source directory.")
        return

    # Ensure DB exists
    from config.settings import DB_PATH
    if not DB_PATH.exists():
        print("[INFO] Initializing database...")
        init_db()

    conn = connect()
    STAGING_DIR.mkdir(parents=True, exist_ok=True)

    stats = {"found": 0, "imported": 0, "skipped_dup": 0, "skipped_small": 0}
    seen_names = set()

    print(f"\n{'=' * 60}")
    print(f"GB-BRAIN — Strategy Import")
    print(f"Source: {source}")
    print(f"Dry run: {dry_run}")
    print(f"{'=' * 60}\n")

    for search_dir in search_dirs:
        # Find all .md, .py, .pine files
        patterns = ["*.md", "*.py", "*.pine"]
        files = []
        for pat in patterns:
            if search_dir.name in ["engine"]:
                # For engine folder, only get specific strategy files
                files.extend(search_dir.glob(pat))
            else:
                files.extend(search_dir.glob(pat))

        print(f"\nProcessing: {search_dir.name}/ ({len(files)} files)")

        for filepath in sorted(files):
            stats["found"] += 1

            # Skip tiny files
            if filepath.stat().st_size < 200:
                stats["skipped_small"] += 1
                continue

            # Clean name and check for duplicates
            name = clean_strategy_name(filepath.name)
            if name in seen_names:
                stats["skipped_dup"] += 1
                continue
            seen_names.add(name)

            if dry_run:
                if stats["found"] <= 20:
                    print(f"  [DRY] {name[:60]}")
                continue

            # Read content
            try:
                content = filepath.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue

            # Compute hash for dedup
            content_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]

            # Copy to staging
            ext = filepath.suffix
            dest = STAGING_DIR / f"{name}{ext}"
            if not dest.exists():
                shutil.copy2(filepath, dest)

            # Classify
            category = classify_category(content, name)

            # Register in SQLite
            sid = insert_strategy(
                conn,
                name=name,
                source_file=str(dest),
                source_repo=f"local:{search_dir.name}",
                category=category,
                logic_hash=content_hash,
            )

            # Log harvest
            insert_harvest_log(
                conn,
                repo_full_name=f"local/{search_dir.name}",
                file_path=str(filepath),
                file_hash=content_hash,
            )

            stats["imported"] += 1

            if stats["imported"] % 500 == 0:
                print(f"  Imported: {stats['imported']:,}...")

    conn.close()

    print(f"\n{'=' * 60}")
    print("IMPORT COMPLETE")
    print(f"  Files found:      {stats['found']:,}")
    print(f"  Imported:         {stats['imported']:,}")
    print(f"  Skipped (dup):    {stats['skipped_dup']:,}")
    print(f"  Skipped (small):  {stats['skipped_small']:,}")
    print(f"{'=' * 60}")

    if not dry_run:
        # Show DB stats
        conn = connect()
        from db.brain_db import get_stats
        s = get_stats(conn)
        conn.close()
        print(f"\nDatabase stats:")
        print(f"  Total strategies: {s['total_strategies']:,}")
        print(f"  Pending:          {s['pending']:,}")
        print(f"  Harvested files:  {s['total_harvested']:,}")

    if dry_run:
        print(f"\n  (Dry run — nothing was saved. Remove --dry-run to import for real.)")


# ── Also import existing backtest results ────
def import_existing_results(source_dir):
    """Import raw_results.csv from Future-Trading into SQLite."""
    source = Path(source_dir)
    csv_path = source / "4_backtest_results" / "raw_results.csv"

    if not csv_path.exists():
        print(f"[SKIP] No existing results file: {csv_path}")
        return

    import pandas as pd
    from db.brain_db import insert_backtest

    df = pd.read_csv(csv_path)
    print(f"\n[INFO] Found {len(df):,} existing backtest results")
    print(f"  (These used the OLD generic engine — importing for reference only)")

    conn = connect()
    imported = 0

    for _, row in df.iterrows():
        # Find strategy by name
        strat = conn.execute(
            "SELECT id FROM strategies WHERE name = ?",
            (row.get("strategy", ""),)
        ).fetchone()

        if not strat:
            continue

        try:
            insert_backtest(
                conn,
                strategy_id=strat["id"],
                symbol=row.get("ticker", ""),
                timeframe=row.get("timeframe", ""),
                data_source="legacy",
                total_trades=int(row.get("trades", 0)),
                win_rate=float(row.get("win_rate", 0)),
                total_return=float(row.get("return_pct", 0)),
                status="legacy",
            )
            imported += 1
        except Exception:
            pass

        if imported % 5000 == 0 and imported > 0:
            print(f"  Imported {imported:,} results...")

    conn.close()
    print(f"  Legacy results imported: {imported:,}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Import existing strategies into GB-BRAIN")
    parser.add_argument(
        "--source", "-s",
        required=True,
        help="Path to Future-Trading folder (e.g. C:\\Users\\gsbha\\qwen-dev\\Future-Trading)"
    )
    parser.add_argument("--dry-run", "-d", action="store_true",
                        help="Show what would be imported without doing it")
    parser.add_argument("--results", "-r", action="store_true",
                        help="Also import old backtest results (as legacy)")
    args = parser.parse_args()

    import_strategies(args.source, dry_run=args.dry_run)

    if args.results and not args.dry_run:
        import_existing_results(args.source)
