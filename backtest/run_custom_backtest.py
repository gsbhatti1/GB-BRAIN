"""
GB-BRAIN — Custom Strategy Backtester
========================================
Tests Cipher, Parallax, and Combined engines across all tickers and timeframes.
Simulates trade management (SL, TP, BE, trailing) and writes results to SQLite.

Usage:
    python backtest/run_custom_backtest.py                           # All tickers, all TFs
    python backtest/run_custom_backtest.py --ticker US30 --tf 5m     # One combo
    python backtest/run_custom_backtest.py --ticker SOL --strategy combined
    python backtest/run_custom_backtest.py --list                    # Show available tickers

STOP → Backup → Patch → Run → Verify
"""

import sys
import logging
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from config.settings import DATA_CACHE_DIR, BACKTEST_CASH
from db.brain_db import connect
from strategies.custom.ticker_presets import get_preset, list_tickers, PRESETS
from strategies.custom.cipher_engine import CipherEngine
from strategies.custom.parallax_engine import ParallaxEngine
from strategies.custom.combined_engine import CombinedEngine

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger("gb_brain.custom_bt")


# ══════════════════════════════════════════════
# DATA LOADING
# ══════════════════════════════════════════════

OHLCV_COLUMNS = ["open", "high", "low", "close", "volume"]
REQUIRED_PRICE_COLUMNS = ["open", "high", "low", "close"]


def _flatten_columns(columns) -> list[str]:
    """Flatten standard or MultiIndex columns into lowercase names."""
    flat = []
    for col in columns:
        if isinstance(col, tuple):
            name = str(col[0]).strip().lower()
        else:
            name = str(col).strip().lower()
        flat.append(name)
    return flat


def _looks_like_ohlcv(df: pd.DataFrame) -> bool:
    """Quick shape check for cached OHLCV frames."""
    cols = set(_flatten_columns(df.columns))
    return all(col in cols for col in REQUIRED_PRICE_COLUMNS)


def _normalize_df(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize index and OHLCV columns into a clean numeric frame."""
    if df is None or df.empty:
        return pd.DataFrame(columns=OHLCV_COLUMNS)

    df = df.copy()
    df.columns = _flatten_columns(df.columns)

    # Parse timestamp index safely. Junk rows like 'Ticker' / 'Datetime' become NaT and get dropped.
    df.index = pd.to_datetime(pd.Index(df.index.astype(str)), utc=True, errors="coerce", format="mixed")
    df.index.name = "datetime"
    df = df[df.index.notna()]

    # Remove duplicate timestamps and keep chronological order.
    if not df.empty:
        df = df[~df.index.duplicated(keep="last")]
        df = df.sort_index()

    # Coerce OHLCV to numeric.
    for col in OHLCV_COLUMNS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Validate required price columns.
    missing = [col for col in REQUIRED_PRICE_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Missing column(s): {', '.join(missing)}")

    # Drop broken rows where any core OHLC value is non-numeric.
    df = df.dropna(subset=REQUIRED_PRICE_COLUMNS)

    if "volume" not in df.columns:
        df["volume"] = 1.0
    else:
        df["volume"] = df["volume"].fillna(0.0)

    if df.empty:
        raise ValueError("No valid OHLC rows after normalization")

    return df[OHLCV_COLUMNS]


def _read_cached_csv(csv_path: Path) -> pd.DataFrame:
    """Read cached CSV, supporting both flat caches and yfinance-exported CSVs."""
    read_errors = []

    # Flat read works for clean caches and also for yfinance CSV exports with junk header rows,
    # as long as normalization drops the non-datetime rows afterward.
    try:
        df = pd.read_csv(csv_path, index_col=0)
        return _normalize_df(df)
    except Exception as exc:
        read_errors.append(f"flat read failed: {exc}")

    # Fallback to yfinance-style multi-row header: Price/Ticker + Datetime index label.
    try:
        df = pd.read_csv(csv_path, header=[0, 1], index_col=0)
        if _looks_like_ohlcv(df):
            return _normalize_df(df)
        read_errors.append("multi-header read failed: columns did not look like OHLCV")
    except Exception as exc:
        read_errors.append(f"multi-header read failed: {exc}")

    raise ValueError(f"Could not parse cached CSV {csv_path.name}: {' | '.join(read_errors)}")


def _write_cached_csv(df: pd.DataFrame, csv_path: Path) -> None:
    """Write a clean, flat OHLCV cache so future reads are deterministic."""
    clean = _normalize_df(df)
    clean.to_csv(csv_path, index_label="datetime")


def load_data(ticker: str, timeframe: str, preset: dict) -> pd.DataFrame:
    """Load OHLCV data from cache or download."""
    yahoo_sym = preset.get("yahoo_symbol")
    binance_sym = preset.get("binance_symbol")

    # Build search names (ticker first, then yahoo, then binance)
    names = []
    for name in [ticker, yahoo_sym, binance_sym]:
        if name and name not in names:
            names.append(name)

    # Try CSV first (always works, no extra dependencies)
    for name in names:
        csv_path = DATA_CACHE_DIR / f"{name}_{timeframe}.csv"
        if csv_path.exists():
            logger.info(f"Loading CSV: {csv_path}")
            try:
                return _read_cached_csv(csv_path)
            except Exception as exc:
                logger.warning(f"Failed parsing CSV {csv_path.name}: {exc}")

    # Try parquet (needs pyarrow/fastparquet)
    for name in names:
        pq_path = DATA_CACHE_DIR / f"{name}_{timeframe}.parquet"
        if pq_path.exists():
            try:
                logger.info(f"Loading parquet: {pq_path}")
                df = pd.read_parquet(pq_path)
                return _normalize_df(df)
            except ImportError:
                logger.warning("Parquet file found but pyarrow not installed. pip install pyarrow")
            except Exception as exc:
                logger.warning(f"Failed parsing parquet {pq_path.name}: {exc}")

    # Download via yfinance
    try:
        import yfinance as yf

        sym = yahoo_sym or binance_sym or ticker
        logger.info(f"Downloading {sym} {timeframe} from Yahoo Finance...")
        period_map = {"1m": "7d", "5m": "60d", "15m": "60d", "30m": "60d", "1h": "730d"}
        period = period_map.get(timeframe, "60d")
        data = yf.download(sym, period=period, interval=timeframe, progress=False, auto_adjust=False)
        if data.empty:
            logger.error(f"No data for {sym} {timeframe}")
            return pd.DataFrame(columns=OHLCV_COLUMNS)

        clean = _normalize_df(data)

        # Cache as flat CSV to avoid future header-shape issues.
        save_path = DATA_CACHE_DIR / f"{ticker}_{timeframe}.csv"
        _write_cached_csv(clean, save_path)
        logger.info(f"Cached to {save_path}")
        return clean
    except Exception as exc:
        logger.error(f"Failed to load data: {exc}")
        return pd.DataFrame(columns=OHLCV_COLUMNS)


# ══════════════════════════════════════════════
# TRADE SIMULATOR
# ══════════════════════════════════════════════

def simulate_trades(signals: list, df: pd.DataFrame, preset: dict) -> Dict[str, Any]:
    """
    Simulate trades with SL, TP1/TP2/TP3, break-even, and trailing stop.
    Returns performance metrics.
    """
    c = df["close"].values.astype(float)
    h = df["high"].values.astype(float)
    l = df["low"].values.astype(float)
    n = len(c)

    trades = []

    for sig in signals:
        bar = sig.bar if hasattr(sig, "bar") else sig["bar"]
        direction = sig.direction if hasattr(sig, "direction") else sig["direction"]
        entry_price = sig.entry_price if hasattr(sig, "entry_price") else sig["entry_price"]
        sl = sig.stop_loss if hasattr(sig, "stop_loss") else sig["stop_loss"]
        tp1 = sig.tp1 if hasattr(sig, "tp1") else sig["tp1"]
        tp3 = sig.tp3 if hasattr(sig, "tp3") else sig["tp3"]

        if bar >= n - 1:
            continue

        # Simulate forward from entry bar
        risk = abs(entry_price - sl)
        if risk <= 0:
            continue

        be_hit = False
        tp1_hit = False
        trailing = False
        trail_peak = entry_price
        trail_trough = entry_price
        exit_price = None
        exit_bar = None
        exit_reason = ""

        one_r = entry_price + risk * direction  # 1R level

        for j in range(bar + 1, min(bar + 200, n)):  # Max 200 bars per trade
            if direction == 1:  # LONG
                current_sl = entry_price if be_hit else sl
                if l[j] <= current_sl:
                    exit_price = current_sl
                    exit_bar = j
                    exit_reason = "BE" if be_hit else "SL"
                    break

                if h[j] >= tp3:
                    exit_price = tp3
                    exit_bar = j
                    exit_reason = "TP3"
                    break

                if not tp1_hit and h[j] >= tp1:
                    tp1_hit = True
                    trailing = True
                    trail_peak = h[j]

                if not be_hit and h[j] >= one_r:
                    be_hit = True

                if trailing:
                    trail_peak = max(trail_peak, h[j])
                    trail_pct = preset.get("parallax", {}).get("trail_pct", 0.40)
                    trail_stop = trail_peak - (trail_peak - entry_price) * trail_pct
                    if c[j] < trail_stop:
                        exit_price = c[j]
                        exit_bar = j
                        exit_reason = "TRAIL"
                        break

            else:  # SHORT
                current_sl = entry_price if be_hit else sl
                if h[j] >= current_sl:
                    exit_price = current_sl
                    exit_bar = j
                    exit_reason = "BE" if be_hit else "SL"
                    break

                if l[j] <= tp3:
                    exit_price = tp3
                    exit_bar = j
                    exit_reason = "TP3"
                    break

                if not tp1_hit and l[j] <= tp1:
                    tp1_hit = True
                    trailing = True
                    trail_trough = l[j]

                if not be_hit and l[j] <= one_r:
                    be_hit = True

                if trailing:
                    trail_trough = min(trail_trough, l[j])
                    trail_pct = preset.get("parallax", {}).get("trail_pct", 0.40)
                    trail_stop = trail_trough + (entry_price - trail_trough) * trail_pct
                    if c[j] > trail_stop:
                        exit_price = c[j]
                        exit_bar = j
                        exit_reason = "TRAIL"
                        break

        if exit_price is None:
            exit_price = c[min(bar + 199, n - 1)]
            exit_bar = min(bar + 199, n - 1)
            exit_reason = "TIMEOUT"

        pnl_pts = (exit_price - entry_price) * direction
        rr = pnl_pts / risk if risk > 0 else 0

        score = 0
        if hasattr(sig, "confluence_score"):
            score = sig.confluence_score
        elif hasattr(sig, "score"):
            score = sig.score

        trades.append(
            {
                "entry_bar": bar,
                "exit_bar": exit_bar,
                "direction": direction,
                "entry_price": entry_price,
                "exit_price": exit_price,
                "sl": sl,
                "tp1": tp1,
                "tp3": tp3,
                "pnl_pts": pnl_pts,
                "rr": rr,
                "exit_reason": exit_reason,
                "score": score,
                "risk": risk,
            }
        )

    if not trades:
        return {
            "total_trades": 0,
            "win_rate": 0,
            "total_return": 0,
            "profit_factor": 0,
            "avg_rr": 0,
            "max_drawdown": 0,
        }

    wins = [t for t in trades if t["pnl_pts"] > 0]
    losses = [t for t in trades if t["pnl_pts"] <= 0]

    total_win_pts = sum(t["pnl_pts"] for t in wins)
    total_loss_pts = abs(sum(t["pnl_pts"] for t in losses))

    pf = total_win_pts / max(total_loss_pts, 0.01)
    wr = len(wins) / len(trades) * 100

    equity = [BACKTEST_CASH]
    for t in trades:
        equity.append(equity[-1] + t["pnl_pts"])
    peak = np.maximum.accumulate(equity)
    dd = (np.array(equity) - peak) / np.where(peak > 0, peak, 1) * 100
    max_dd = abs(np.min(dd))

    avg_rr = np.mean([t["rr"] for t in trades])
    total_return_pct = (equity[-1] - BACKTEST_CASH) / BACKTEST_CASH * 100

    return {
        "total_trades": len(trades),
        "wins": len(wins),
        "losses": len(losses),
        "win_rate": round(wr, 2),
        "total_return": round(total_return_pct, 2),
        "profit_factor": round(pf, 3),
        "avg_rr": round(avg_rr, 2),
        "max_drawdown": round(max_dd, 2),
        "total_pts": round(sum(t["pnl_pts"] for t in trades), 2),
        "win_pts": round(total_win_pts, 2),
        "loss_pts": round(total_loss_pts, 2),
        "avg_score": round(np.mean([t["score"] for t in trades]), 1),
        "trades": trades,
        "exit_reasons": {
            "TP3": len([t for t in trades if t["exit_reason"] == "TP3"]),
            "TRAIL": len([t for t in trades if t["exit_reason"] == "TRAIL"]),
            "SL": len([t for t in trades if t["exit_reason"] == "SL"]),
            "BE": len([t for t in trades if t["exit_reason"] == "BE"]),
            "TIMEOUT": len([t for t in trades if t["exit_reason"] == "TIMEOUT"]),
        },
    }


# ══════════════════════════════════════════════
# MAIN BACKTEST LOOP
# ══════════════════════════════════════════════

def run_backtest(ticker: str, timeframe: str, strategy: str = "all"):
    """Run backtest for a specific ticker/timeframe/strategy combo."""
    preset = get_preset(ticker)
    logger.info(f"═══ {preset['display_name']} | {timeframe} | Strategy: {strategy} ═══")

    df = load_data(ticker, timeframe, preset)
    if df.empty:
        logger.error(f"No data available for {ticker} {timeframe}")
        return {}

    logger.info(f"Data loaded: {len(df)} bars from {df.index[0]} to {df.index[-1]}")

    results = {}

    if strategy in ("all", "cipher"):
        logger.info("Running Cipher engine...")
        cipher = CipherEngine(preset["cipher"])
        cipher_sigs = cipher.run(df)
        logger.info(f"  Cipher signals: {len(cipher_sigs)}")
        if cipher_sigs:
            cipher_results = simulate_trades(cipher_sigs, df, preset)
            results["cipher"] = cipher_results
            _print_results("CIPHER", cipher_results)

    if strategy in ("all", "parallax"):
        logger.info("Running Parallax engine...")
        parallax = ParallaxEngine(preset["parallax"])
        parallax_sigs = parallax.run(df)
        logger.info(f"  Parallax signals: {len(parallax_sigs)}")
        if parallax_sigs:
            parallax_results = simulate_trades(parallax_sigs, df, preset)
            results["parallax"] = parallax_results
            _print_results("PARALLAX", parallax_results)

    if strategy in ("all", "combined"):
        logger.info("Running Combined engine...")
        combined = CombinedEngine(preset)
        combined_sigs = combined.run(df)
        logger.info(f"  Combined signals: {len(combined_sigs)}")
        if combined_sigs:
            combined_results = simulate_trades(combined_sigs, df, preset)
            results["combined"] = combined_results
            _print_results("COMBINED", combined_results)

            top = sorted(combined_sigs, key=lambda s: s.confluence_score, reverse=True)[:5]
            logger.info("  Top 5 signals by confluence score:")
            for s in top:
                logger.info(f"    Score {s.confluence_score:.0f} | {s.direction:+d} | {s.source} | {s.reason}")

    return results


def _print_results(name: str, r: dict):
    """Print results in a clean format."""
    logger.info(f"  ─── {name} Results ───")
    logger.info(f"  Trades: {r['total_trades']} | Win Rate: {r['win_rate']:.1f}% | PF: {r['profit_factor']:.2f}")
    logger.info(f"  Total Pts: {r['total_pts']:.1f} | Avg R:R: {r['avg_rr']:.2f} | Max DD: {r['max_drawdown']:.1f}%")
    logger.info(
        f"  Exits: TP3={r['exit_reasons']['TP3']} TRAIL={r['exit_reasons']['TRAIL']} SL={r['exit_reasons']['SL']} BE={r['exit_reasons']['BE']}"
    )
    if r.get("avg_score", 0) > 0:
        logger.info(f"  Avg Signal Score: {r['avg_score']:.1f}")


def save_to_db(ticker: str, timeframe: str, strategy_name: str, results: dict):
    """Save backtest results to SQLite."""
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT OR IGNORE INTO strategies (name, category, source_file) VALUES (?, ?, ?)",
        (f"GB_{strategy_name}_{ticker}", "custom", f"strategies/custom/{strategy_name}_engine.py"),
    )
    conn.commit()

    cursor.execute("SELECT id FROM strategies WHERE name = ?", (f"GB_{strategy_name}_{ticker}",))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return
    strategy_id = row[0]

    cursor.execute(
        """
        INSERT INTO backtest_results
        (strategy_id, symbol, timeframe, total_trades, wins, losses,
         win_rate, total_return, max_drawdown, profit_factor, avg_rr, composite_score, status, run_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            strategy_id,
            ticker,
            timeframe,
            results.get("total_trades", 0),
            results.get("wins", 0),
            results.get("losses", 0),
            results.get("win_rate", 0),
            results.get("total_return", 0),
            results.get("max_drawdown", 0),
            results.get("profit_factor", 0),
            results.get("avg_rr", 0),
            results.get("win_rate", 0) * 0.35 + results.get("profit_factor", 0) * 2,
            "GEM" if results.get("win_rate", 0) >= 55 and results.get("total_return", 0) > 0 else "PASS",
            datetime.now().isoformat(),
        ),
    )
    conn.commit()
    conn.close()
    logger.info(f"  Saved to SQLite: GB_{strategy_name}_{ticker}")


# ══════════════════════════════════════════════
# CLI
# ══════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="GB-BRAIN Custom Strategy Backtester")
    parser.add_argument("--ticker", type=str, help="Ticker to test (US30, NAS100, SPX500, BTC, ETH, SOL)")
    parser.add_argument("--tf", type=str, help="Timeframe (5m, 15m, 30m, 1h)")
    parser.add_argument("--strategy", type=str, default="all", choices=["cipher", "parallax", "combined", "all"])
    parser.add_argument("--list", action="store_true", help="List available tickers")
    parser.add_argument("--save", action="store_true", help="Save results to SQLite")
    args = parser.parse_args()

    if args.list:
        print("\nAvailable Tickers:")
        for k, v in list_tickers().items():
            preset = PRESETS[k]
            print(f"  {k:8s} → {v:25s} | Best TFs: {', '.join(preset['best_timeframes'])}")
        return

    if args.ticker:
        tickers = [args.ticker.upper()]
    else:
        tickers = list(PRESETS.keys())

    for ticker in tickers:
        preset = get_preset(ticker)
        timeframes = [args.tf] if args.tf else preset["best_timeframes"]

        for tf in timeframes:
            try:
                results = run_backtest(ticker, tf, args.strategy)

                if args.save:
                    for strat_name, strat_results in results.items():
                        if strat_results.get("total_trades", 0) > 0:
                            save_to_db(ticker, tf, strat_name, strat_results)

            except Exception as exc:
                logger.error(f"Error testing {ticker} {tf}: {exc}")
                import traceback

                traceback.print_exc()

    print("\n" + "═" * 60)
    print("DONE. SQLite is truth.")
    print("═" * 60)


if __name__ == "__main__":
    main()
