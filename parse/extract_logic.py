"""
GB-BRAIN — Strategy Logic Extractor
=====================================
Reads harvested .py/.pine files and extracts structured trading logic.

Two modes:
  1. REGEX mode (fast, free) — pattern matching for common indicators
  2. AI mode (accurate, uses API) — Claude/Ollama reads and extracts logic

Usage:
    python parse/extract_logic.py                   # Regex mode (default)
    python parse/extract_logic.py --mode ai          # AI extraction
    python parse/extract_logic.py --limit 50         # Process 50 strategies
"""

import os
import sys
import re
import json
import hashlib
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from config.settings import STAGING_DIR
from db.brain_db import connect

# ── Indicator patterns for regex extraction ──
# These match both Pine Script (ta.ema, ta.rsi) and Python (EMAIndicator, RSI)
INDICATOR_PATTERNS = {
    "EMA":        r"(?:\b(?:EMA|ema)\b|ta\.ema|EMAIndicator|ema_indicator).*?(\d+)",
    "SMA":        r"(?:\b(?:SMA|sma)\b|ta\.sma|SMAIndicator|\.rolling\().*?(\d+)",
    "RSI":        r"(?:\b(?:RSI|rsi)\b|ta\.rsi|RSIIndicator).*?(\d+)",
    "MACD":       r"(?:\bMACD\b|ta\.macd|MACD\()",
    "BB":         r"(?:\bBollinger\b|\bBB\b|ta\.bb|BollingerBands)",
    "ATR":        r"(?:\bATR\b|ta\.atr|AverageTrueRange).*?(\d+)",
    "VWAP":       r"(?:\bVWAP\b|ta\.vwap|vwap)",
    "Stochastic": r"(?:\bStochastic\b|\bstoch\b|ta\.stoch|StochasticOscillator)",
    "Supertrend": r"(?:\bSupertrend\b|\bsupertrend\b)",
    "Ichimoku":   r"(?:\bIchimoku\b|\bichimoku\b)",
    "ADX":        r"(?:\bADX\b|ta\.adx|ADXIndicator)",
    "CCI":        r"(?:\bCCI\b|ta\.cci|CCIIndicator)",
    "OBV":        r"(?:\bOBV\b|ta\.obv|OnBalanceVolume)",
    "MFI":        r"(?:\bMFI\b|ta\.mfi|MFIIndicator)",
}

# Entry/exit patterns — match Pine Script and Python
ENTRY_PATTERNS = [
    r"(?:if|when|signal).*(?:cross(?:over|above)|>).*(?:buy|long|entry)",
    r"(?:buy|long|entry).*(?:if|when).*(?:cross|>|above)",
    r"strategy\.entry.*['\"](?:Long|Buy|long|buy)['\"]",
    r"self\.buy\(",
    r"(?:go_long|enter_long|open_long)",
    r"ta\.crossover.*(?:if|and|or).*(?:long|buy|entry)",
]

EXIT_PATTERNS = [
    r"(?:if|when|signal).*(?:cross(?:under|below)|<).*(?:sell|short|exit)",
    r"(?:sell|short|exit).*(?:if|when).*(?:cross|<|below)",
    r"strategy\.close",
    r"strategy\.exit",
    r"self\.(?:sell|position\.close)\(",
    r"(?:go_short|enter_short|close_long|exit_long)",
    r"ta\.crossunder",
]


def compute_logic_hash(content):
    """Hash the meaningful parts of strategy code for dedup."""
    # Remove comments, whitespace, source headers
    cleaned = re.sub(r"#.*$", "", content, flags=re.MULTILINE)
    cleaned = re.sub(r"\s+", " ", cleaned).strip().lower()
    return hashlib.sha256(cleaned.encode("utf-8")).hexdigest()[:32]


def extract_regex(content, filename):
    """Extract strategy logic using regex patterns. Fast but approximate."""
    result = {
        "indicators": [],
        "parameters": {},
        "entry_logic": "",
        "exit_logic": "",
        "strategy_type": "unknown",
    }

    # Find indicators
    for name, pattern in INDICATOR_PATTERNS.items():
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches or re.search(pattern, content, re.IGNORECASE):
            result["indicators"].append(name)
            # Extract parameters if captured
            if matches and matches[0]:
                try:
                    result["parameters"][f"{name.lower()}_period"] = int(matches[0])
                except (ValueError, IndexError):
                    pass

    # Find entry conditions
    entry_lines = []
    for pattern in ENTRY_PATTERNS:
        for match in re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE):
            line = match.group(0).strip()[:200]
            if line not in entry_lines:
                entry_lines.append(line)
    result["entry_logic"] = " | ".join(entry_lines[:3]) if entry_lines else "not extracted"

    # Find exit conditions
    exit_lines = []
    for pattern in EXIT_PATTERNS:
        for match in re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE):
            line = match.group(0).strip()[:200]
            if line not in exit_lines:
                exit_lines.append(line)
    result["exit_logic"] = " | ".join(exit_lines[:3]) if exit_lines else "not extracted"

    # Classify strategy type
    indicators = set(result["indicators"])
    if {"EMA", "SMA"} & indicators and "RSI" in indicators:
        result["strategy_type"] = "trend_momentum"
    elif "MACD" in indicators:
        result["strategy_type"] = "macd_crossover"
    elif "BB" in indicators:
        result["strategy_type"] = "mean_reversion"
    elif {"EMA", "SMA"} & indicators:
        result["strategy_type"] = "ma_crossover"
    elif "RSI" in indicators:
        result["strategy_type"] = "rsi_reversal"
    elif "Supertrend" in indicators:
        result["strategy_type"] = "trend_following"
    elif "Stochastic" in indicators:
        result["strategy_type"] = "stoch_reversal"
    elif len(indicators) > 0:
        result["strategy_type"] = "multi_indicator"
    else:
        result["strategy_type"] = "unknown"

    return result


def process_strategies(mode="regex", limit=None):
    """Process all pending strategies in the database."""
    conn = connect()

    # Get pending strategies
    if limit:
        rows = conn.execute(
            "SELECT id, name, source_file FROM strategies WHERE status = 'pending' LIMIT ?",
            (limit,)
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT id, name, source_file FROM strategies WHERE status = 'pending'"
        ).fetchall()

    if not rows:
        print("[INFO] No pending strategies to process.")
        conn.close()
        return

    print("=" * 60)
    print(f"GB-BRAIN — Strategy Extractor ({mode} mode)")
    print(f"Processing {len(rows)} strategies")
    print("=" * 60)

    stats = {"processed": 0, "extracted": 0, "failed": 0}

    for i, row in enumerate(rows):
        sid = row["id"]
        name = row["name"]
        source = row["source_file"]

        if not source or not Path(source).exists():
            stats["failed"] += 1
            continue

        try:
            content = Path(source).read_text(encoding="utf-8", errors="ignore")
        except Exception:
            stats["failed"] += 1
            continue

        # Extract logic
        if mode == "regex":
            result = extract_regex(content, name)
        elif mode == "ai":
            # TODO: Phase 2 — AI extraction using Claude API or Ollama
            print(f"  [TODO] AI extraction not yet implemented. Using regex fallback.")
            result = extract_regex(content, name)
        else:
            result = extract_regex(content, name)

        # Compute logic hash for dedup
        logic_hash = compute_logic_hash(content)

        # Update database
        conn.execute(
            """UPDATE strategies SET
                indicators = ?,
                entry_logic = ?,
                exit_logic = ?,
                parameters = ?,
                logic_hash = ?,
                status = 'extracted',
                updated_at = datetime('now')
               WHERE id = ?""",
            (
                json.dumps(result["indicators"]),
                result["entry_logic"],
                result["exit_logic"],
                json.dumps(result["parameters"]),
                logic_hash,
                sid,
            ),
        )
        conn.commit()
        stats["extracted"] += 1
        stats["processed"] += 1

        if (i + 1) % 100 == 0:
            print(f"  [{i+1}/{len(rows)}] Extracted: {stats['extracted']} | Failed: {stats['failed']}")

    conn.close()

    print(f"\n{'=' * 60}")
    print("EXTRACTION COMPLETE")
    print(f"  Processed:  {stats['processed']}")
    print(f"  Extracted:  {stats['extracted']}")
    print(f"  Failed:     {stats['failed']}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GB-BRAIN Strategy Logic Extractor")
    parser.add_argument("--mode", "-m", default="regex", choices=["regex", "ai"],
                        help="Extraction mode (default: regex)")
    parser.add_argument("--limit", "-l", type=int, default=None,
                        help="Max strategies to process")
    args = parser.parse_args()

    process_strategies(mode=args.mode, limit=args.limit)
