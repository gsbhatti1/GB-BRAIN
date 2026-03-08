"""
GB-BRAIN — Data Fetcher
========================
Downloads OHLCV data from Yahoo Finance (indices) and Binance (crypto).
Saves to backtest/data_cache/ as CSV. Skips if cached.
"""

import os
import sys
import time
from pathlib import Path
from datetime import datetime, timedelta

import pandas as pd

# Add project root to path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from config.settings import (
    CRYPTO_TICKERS, INDEX_TICKERS, TIMEFRAMES,
    DATA_CACHE_DIR, BINANCE_KEY, BINANCE_SECRET,
    YF_INTERVALS, BINANCE_INTERVALS,
)


def fetch_yahoo(ticker, timeframe, cache_dir):
    """Fetch OHLCV from Yahoo Finance. Returns DataFrame or None."""
    import yfinance as yf

    cache_file = cache_dir / f"{ticker.replace('^', '')}_{timeframe}.csv"
    if cache_file.exists():
        age_hours = (time.time() - cache_file.stat().st_mtime) / 3600
        if age_hours < 12:
            print(f"  [CACHED] {ticker} {timeframe} ({age_hours:.1f}h old)")
            return pd.read_csv(cache_file, index_col=0, parse_dates=True)

    if timeframe not in YF_INTERVALS:
        print(f"  [SKIP] {ticker} {timeframe} — unsupported Yahoo interval")
        return None

    yf_cfg = YF_INTERVALS[timeframe]
    try:
        df = yf.download(
            ticker,
            interval=yf_cfg["interval"],
            period=yf_cfg["period"],
            progress=False,
            auto_adjust=True,
        )
        if df.empty:
            print(f"  [EMPTY] {ticker} {timeframe}")
            return None

        # Flatten multi-level columns if present
        if hasattr(df.columns, 'levels') and df.columns.nlevels > 1:
            df.columns = df.columns.get_level_values(0)

        df.columns = [c.lower() for c in df.columns]
        df = df[["open", "high", "low", "close", "volume"]].dropna()
        df.to_csv(cache_file)
        print(f"  [OK] {ticker} {timeframe} → {len(df)} bars")
        return df
    except Exception as e:
        print(f"  [FAIL] {ticker} {timeframe}: {e}")
        return None


def fetch_binance(ticker, timeframe, cache_dir):
    """Fetch OHLCV from Binance. Returns DataFrame or None."""
    from binance.client import Client

    cache_file = cache_dir / f"{ticker}_{timeframe}.csv"
    if cache_file.exists():
        age_hours = (time.time() - cache_file.stat().st_mtime) / 3600
        if age_hours < 12:
            print(f"  [CACHED] {ticker} {timeframe} ({age_hours:.1f}h old)")
            return pd.read_csv(cache_file, index_col=0, parse_dates=True)

    if timeframe not in BINANCE_INTERVALS:
        print(f"  [SKIP] {ticker} {timeframe} — unsupported Binance interval")
        return None

    lookback_days = {"1m": 7, "5m": 59, "15m": 59, "30m": 59, "1h": 365}
    days = lookback_days.get(timeframe, 59)
    start_str = (datetime.now() - timedelta(days=days)).strftime("%d %b %Y")

    try:
        client = Client(BINANCE_KEY, BINANCE_SECRET)
        klines = client.get_historical_klines(
            ticker, BINANCE_INTERVALS[timeframe], start_str
        )
        if not klines:
            print(f"  [EMPTY] {ticker} {timeframe}")
            return None

        cols = [
            "timestamp", "open", "high", "low", "close", "volume",
            "ct", "qv", "t", "tbb", "tbq", "ignore",
        ]
        df = pd.DataFrame(klines, columns=cols)
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df.set_index("timestamp", inplace=True)
        for c in ["open", "high", "low", "close", "volume"]:
            df[c] = df[c].astype(float)
        df = df[["open", "high", "low", "close", "volume"]]
        df.to_csv(cache_file)
        print(f"  [OK] {ticker} {timeframe} → {len(df)} bars")
        return df
    except Exception as e:
        print(f"  [FAIL] {ticker} {timeframe}: {e}")
        return None


def fetch_all():
    """Fetch data for all configured tickers and timeframes."""
    cache_dir = Path(DATA_CACHE_DIR)
    cache_dir.mkdir(parents=True, exist_ok=True)

    total = len(ALL_TICKERS) * len(TIMEFRAMES)
    done = 0

    print("=" * 50)
    print("GB-BRAIN — Data Fetcher")
    print(f"Tickers: {len(ALL_TICKERS)} | Timeframes: {len(TIMEFRAMES)} | Total: {total}")
    print("=" * 50)

    # Crypto via Binance
    print("\n── Crypto (Binance) ──")
    for ticker in CRYPTO_TICKERS:
        for tf in TIMEFRAMES:
            fetch_binance(ticker, tf, cache_dir)
            done += 1
            time.sleep(0.3)

    # Indices via Yahoo
    print("\n── Indices (Yahoo Finance) ──")
    for ticker in INDEX_TICKERS:
        for tf in TIMEFRAMES:
            fetch_yahoo(ticker, tf, cache_dir)
            done += 1
            time.sleep(0.5)

    # Summary
    cached_files = list(cache_dir.glob("*.csv"))
    print(f"\n{'=' * 50}")
    print(f"Done! {len(cached_files)} files in cache.")
    print(f"{'=' * 50}")


ALL_TICKERS = CRYPTO_TICKERS + INDEX_TICKERS

if __name__ == "__main__":
    fetch_all()
