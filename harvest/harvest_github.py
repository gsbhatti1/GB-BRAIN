"""
GB-BRAIN — Strategy Harvester
==============================
Scans GitHub for trading strategy repos.
Downloads .py and .pine files to strategies/staging/.
Deduplicates using SQLite harvest_log table.

Usage:
    python harvest/harvest_github.py
    python harvest/harvest_github.py --category crypto
    python harvest/harvest_github.py --dry-run
"""

import os
import sys
import json
import time
import hashlib
import argparse
from pathlib import Path

import requests

# Add project root to path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from config.settings import (
    GITHUB_TOKEN, STAGING_DIR,
    HARVEST_MAX_DEPTH, HARVEST_RATE_SLEEP, HARVEST_FILE_SLEEP,
)
from db.brain_db import connect, insert_harvest_log, is_harvested, insert_strategy

# ── GitHub API ───────────────────────────────
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
}

# Keywords that indicate a file contains strategy logic
STRATEGY_KEYWORDS = [
    "strategy", "signal", "entry", "exit", "backtest",
    "win_rate", "winrate", "long", "short", "ema",
    "rsi", "macd", "bollinger", "crossover", "stop_loss",
    "take_profit", "position", "order", "buy", "sell",
]

CRYPTO_KEYWORDS = [
    "btc", "eth", "sol", "crypto", "usdt", "binance",
    "bybit", "blofin", "bitcoin", "ethereum", "solana",
    "futures", "perpetual",
]

INDEX_KEYWORDS = [
    "us30", "nas100", "spx500", "spx", "spy", "es", "nq",
    "dow jones", "s&p500", "nasdaq", "index", "cfd",
]


def handle_rate_limit(response):
    """Sleep if GitHub rate limit is low."""
    remaining = int(response.headers.get("X-RateLimit-Remaining", "99"))
    reset_time = int(response.headers.get("X-RateLimit-Reset", "0"))
    if remaining < 5 and reset_time > 0:
        wait = max(reset_time - time.time(), 0) + 2
        print(f"  [RATE LIMIT] {remaining} left — sleeping {wait:.0f}s")
        time.sleep(wait)


def search_repos(query, page=1):
    """Search GitHub repos by query."""
    url = "https://api.github.com/search/repositories"
    params = {
        "q": query,
        "sort": "stars",
        "order": "desc",
        "per_page": 30,
        "page": page,
    }
    try:
        r = requests.get(url, headers=HEADERS, params=params, timeout=15)
        if r.status_code == 200:
            handle_rate_limit(r)
            return r.json().get("items", [])
        if r.status_code == 403:
            handle_rate_limit(r)
            return []
    except requests.RequestException as e:
        print(f"  [ERROR] search: {e}")
    return []


def get_repo_files(owner, repo, path="", depth=0):
    """Recursively get .py and .pine files from a repo."""
    if depth > HARVEST_MAX_DEPTH:
        return []
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
    except requests.RequestException:
        return []
    if r.status_code != 200:
        return []

    files = []
    for item in r.json():
        if item["type"] == "file":
            name = item["name"].lower()
            if name.endswith(".py") or name.endswith(".pine"):
                files.append(item)
        elif item["type"] == "dir" and depth < 2:
            subdir = item["name"].lower()
            relevant = ["strat", "signal", "trade", "bot", "algo", "backtest", "script", "src"]
            if any(k in subdir for k in relevant):
                files.extend(get_repo_files(owner, repo, item["path"], depth + 1))
    return files


def is_relevant(content, ext):
    """Check if file content looks like a trading strategy."""
    if ext == ".pine":
        return True
    low = content.lower()
    hits = sum(1 for k in STRATEGY_KEYWORDS if k in low)
    has_market = any(k in low for k in CRYPTO_KEYWORDS + INDEX_KEYWORDS)
    return hits >= 4 or (has_market and hits >= 2)


def classify_category(content):
    """Guess if a strategy is for crypto or indices."""
    low = content.lower()
    crypto_hits = sum(1 for k in CRYPTO_KEYWORDS if k in low)
    index_hits = sum(1 for k in INDEX_KEYWORDS if k in low)
    if crypto_hits > index_hits:
        return "crypto"
    if index_hits > crypto_hits:
        return "indices"
    return "unknown"


def clean_name(owner, repo, filename):
    """Create a clean, readable filename."""
    # Remove common prefixes/suffixes and special chars
    base = Path(filename).stem
    # Limit length
    clean = f"{owner}_{repo}_{base}"[:120]
    # Replace problematic chars
    for ch in ["/", "\\", " ", "'", '"', "(", ")", "[", "]"]:
        clean = clean.replace(ch, "_")
    return clean


def download_and_save(item, owner, repo, stars, conn, dry_run=False):
    """Download a file, check relevance, save to staging, log to DB."""
    ext = ".pine" if item["name"].lower().endswith(".pine") else ".py"
    file_path = item.get("path", item["name"])

    # Check if already harvested
    repo_full = f"{owner}/{repo}"
    if is_harvested(conn, repo_full, file_path):
        return "skip_dup"

    if dry_run:
        print(f"    [DRY] Would download: {file_path}")
        return "dry"

    # Download
    try:
        r = requests.get(item["download_url"], headers=HEADERS, timeout=15)
        if r.status_code != 200:
            return "fail"
        content = r.text
    except requests.RequestException:
        return "fail"

    # Check relevance
    if not is_relevant(content, ext):
        return "skip_irrelevant"

    # Save to staging
    clean = clean_name(owner, repo, item["name"])
    out_path = STAGING_DIR / (clean + ext)
    content_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]

    header = f"# SOURCE: https://github.com/{owner}/{repo}\n"
    header += f"# FILE:   {file_path}\n"
    header += f"# STARS:  {stars}\n\n"

    out_path.write_text(header + content, encoding="utf-8", errors="replace")

    # Log to DB
    insert_harvest_log(conn, repo_full_name=repo_full, file_path=file_path,
                       file_hash=content_hash)

    # Register strategy (pending extraction)
    category = classify_category(content)
    insert_strategy(conn, name=clean, source_file=str(out_path),
                    source_repo=f"https://github.com/{owner}/{repo}",
                    category=category)

    print(f"    [SAVED] {clean[:60]}... ({category})")
    return "saved"


def run_harvest(categories=None, dry_run=False, max_pages=2):
    """Main harvest loop."""
    # Check GitHub token
    if not GITHUB_TOKEN or GITHUB_TOKEN in ("test", "ghp_your_token_here", "your_token_here"):
        print("=" * 60)
        print("[ERROR] GitHub token not configured!")
        print("")
        print("  1. Go to: https://github.com/settings/tokens")
        print("  2. Generate a new token (classic) with 'public_repo' scope")
        print("  3. Open your .env file: notepad .env")
        print("  4. Set: GITHUB_TOKEN=ghp_your_actual_token")
        print("  5. Save and re-run this script")
        print("")
        print("  Without a token, GitHub API returns 0 results.")
        print("=" * 60)
        return

    # Verify token works
    try:
        test_r = requests.get("https://api.github.com/user", headers=HEADERS, timeout=10)
        if test_r.status_code == 401:
            print("[ERROR] GitHub token is INVALID. Generate a new one at:")
            print("  https://github.com/settings/tokens")
            return
        remaining = test_r.headers.get("X-RateLimit-Remaining", "?")
        print(f"[OK] GitHub token valid. Rate limit remaining: {remaining}")
    except Exception as e:
        print(f"[WARN] Could not verify GitHub token: {e}")

    # Load queries
    queries_file = Path(__file__).parent / "queries.json"
    all_queries = json.loads(queries_file.read_text(encoding="utf-8"))

    # Filter categories if specified
    if categories:
        queries = {}
        for cat in categories:
            if cat in all_queries:
                queries[cat] = all_queries[cat]
            else:
                print(f"[WARN] Unknown category: {cat}")
        if not queries:
            print("[ERROR] No valid categories found")
            return
    else:
        queries = all_queries

    # Flatten all queries
    flat_queries = []
    for cat, qlist in queries.items():
        for q in qlist:
            flat_queries.append((cat, q))

    conn = connect()
    stats = {"repos": 0, "saved": 0, "skipped": 0, "failed": 0}
    seen_repos = set()

    print("=" * 60)
    print("GB-BRAIN — Strategy Harvester")
    print(f"Categories: {list(queries.keys())}")
    print(f"Queries: {len(flat_queries)}")
    print(f"Dry run: {dry_run}")
    print("=" * 60)

    for qi, (cat, query) in enumerate(flat_queries):
        print(f"\n[{qi+1}/{len(flat_queries)}] ({cat}) {query[:70]}")

        for page in range(1, max_pages + 1):
            repos = search_repos(query, page)
            for repo in repos:
                key = repo["full_name"]
                if key in seen_repos:
                    continue
                seen_repos.add(key)
                stats["repos"] += 1

                owner = repo["owner"]["login"]
                rname = repo["name"]
                stars = repo["stargazers_count"]
                print(f"  [{stars}★] {key}")

                files = get_repo_files(owner, rname)
                for f in files:
                    result = download_and_save(f, owner, rname, stars, conn, dry_run)
                    if result == "saved":
                        stats["saved"] += 1
                    elif result.startswith("skip"):
                        stats["skipped"] += 1
                    elif result == "fail":
                        stats["failed"] += 1
                    time.sleep(HARVEST_FILE_SLEEP)

            time.sleep(HARVEST_RATE_SLEEP)

        print(f"  Progress: {stats['repos']} repos | {stats['saved']} saved | {stats['skipped']} skipped")

    conn.close()

    print(f"\n{'=' * 60}")
    print("HARVEST COMPLETE")
    print(f"  Repos scanned:  {stats['repos']}")
    print(f"  Files saved:    {stats['saved']}")
    print(f"  Skipped:        {stats['skipped']}")
    print(f"  Failed:         {stats['failed']}")
    print(f"\nFiles in: {STAGING_DIR}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GB-BRAIN Strategy Harvester")
    parser.add_argument("--category", "-c", nargs="+",
                        help="Categories to harvest (e.g. crypto indices elite)")
    parser.add_argument("--dry-run", "-d", action="store_true",
                        help="Show what would be downloaded without saving")
    parser.add_argument("--pages", "-p", type=int, default=2,
                        help="Max pages per query (default: 2)")
    args = parser.parse_args()

    run_harvest(categories=args.category, dry_run=args.dry_run, max_pages=args.pages)
