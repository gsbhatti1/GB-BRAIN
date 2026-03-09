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
import json
import logging
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from config.settings import DB_PATH, DATA_CACHE_DIR, BACKTEST_CASH
from db.brain_db import connect
from strategies.custom.ticker_presets import get_preset, list_tickers, PRESETS
from strategies.custom.cipher_engine import CipherEngine, CipherSignal
from strategies.custom.parallax_engine import ParallaxEngine, ParallaxSignal
from strategies.custom.combined_engine import CombinedEngine, CombinedSignal

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger("gb_brain.custom_bt")


# ══════════════════════════════════════════════
# DATA LOADING
# ══════════════════════════════════════════════

def load_data(ticker: str, timeframe: str, preset: dict) -> pd.DataFrame:
    """Load OHLCV data from cache or download."""
    yahoo_sym = preset.get("yahoo_symbol")
    binance_sym = preset.get("binance_symbol")

    # Try cached data first
    cache_patterns = [
        DATA_CACHE_DIR / f"{ticker}_{timeframe}.parquet",
        DATA_CACHE_DIR / f"{yahoo_sym}_{timeframe}.parquet" if yahoo_sym else None,
        DATA_CACHE_DIR / f"{binance_sym}_{timeframe}.parquet" if binance_sym else None,
    ]

    for path in cache_patterns:
        if path and path.exists():
            logger.info(f"Loading cached: {path}")
            df = pd.read_parquet(path)
            df = _normalize_df(df)
            df = _align_timezone(df, ticker)
            return df

    # Try CSV
    for path in cache_patterns:
        if path:
            csv_path = path.with_suffix(".csv")
            if csv_path.exists():
                logger.info(f"Loading CSV: {csv_path}")
                df = pd.read_csv(csv_path, parse_dates=True, index_col=0)
                df = _normalize_df(df)
                df = _align_timezone(df, ticker)
                return df

    # Download via yfinance
    try:
        import yfinance as yf

        sym = yahoo_sym or binance_sym or ticker
        logger.info(f"Downloading {sym} {timeframe} from Yahoo Finance...")
        period_map = {"1m": "7d", "5m": "60d", "15m": "60d", "30m": "60d", "1h": "730d"}
        period = period_map.get(timeframe, "60d")

        data = yf.download(
            sym,
            period=period,
            interval=timeframe,
            progress=False,
            auto_adjust=False,
        )

        if data.empty:
            logger.error(f"No data for {sym} {timeframe}")
            return pd.DataFrame()

        save_path = DATA_CACHE_DIR / f"{ticker}_{timeframe}.parquet"
        data.to_parquet(save_path)
        logger.info(f"Cached to {save_path}")

        data = _normalize_df(data)
        data = _align_timezone(data, ticker)
        return data

    except Exception as e:
        logger.error(f"Failed to load data: {e}")
        return pd.DataFrame()


def _normalize_df(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize OHLCV columns, including yfinance MultiIndex columns."""
    if df is None or df.empty:
        return pd.DataFrame()

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [str(col[0]).lower().strip() for col in df.columns]
    else:
        normalized = []
        for c in df.columns:
            if isinstance(c, tuple):
                normalized.append(str(c[0]).lower().strip())
            else:
                normalized.append(str(c).lower().strip())
        df.columns = normalized

    df = df.loc[:, ~pd.Index(df.columns).duplicated()]

    required = ["open", "high", "low", "close"]
    for col in required:
        if col not in df.columns:
            raise ValueError(f"Missing column: {col}")

    if "volume" not in df.columns:
        df["volume"] = 1.0

    keep = [c for c in ["open", "high", "low", "close", "volume"] if c in df.columns]
    df = df[keep].copy()
    return df


def _align_timezone(df: pd.DataFrame, ticker: str) -> pd.DataFrame:
    """Convert index into the timezone expected by the strategy logic."""
    if df is None or df.empty:
        return pd.DataFrame()

    idx = pd.to_datetime(df.index, errors="coerce")

    if getattr(idx, "tz", None) is None:
        idx = idx.tz_localize("UTC")

    if ticker in {"US30", "NAS100", "SPX500"}:
        idx = idx.tz_convert("America/New_York").tz_localize(None)
    else:
        idx = idx.tz_convert("UTC").tz_localize(None)

    out = df.copy()
    out.index = idx
    out = out[~out.index.isna()].sort_index()
    return out
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
    capital = BACKTEST_CASH
    peak_capital = capital

    for sig in signals:
        bar = sig.bar if hasattr(sig, 'bar') else sig["bar"]
        direction = sig.direction if hasattr(sig, 'direction') else sig["direction"]
        entry_price = sig.entry_price if hasattr(sig, 'entry_price') else sig["entry_price"]
        sl = sig.stop_loss if hasattr(sig, 'stop_loss') else sig["stop_loss"]
        tp1 = sig.tp1 if hasattr(sig, 'tp1') else sig["tp1"]
        tp3 = sig.tp3 if hasattr(sig, 'tp3') else sig["tp3"]

        if bar >= n - 1:
            continue

        # Simulate forward from entry bar
        risk = abs(entry_price - sl)
        if risk <= 0:
            continue

        be_hit = False
        tp1_hit = False
        trailing = False
        trail_peak = entry_price if direction == 1 else entry_price
        trail_trough = entry_price if direction == -1 else entry_price
        exit_price = None
        exit_bar = None
        exit_reason = ""

        one_r = entry_price + risk * direction  # 1R level

        for j in range(bar + 1, min(bar + 200, n)):  # Max 200 bars per trade
            if direction == 1:  # LONG
                # Check SL
                current_sl = entry_price if be_hit else sl
                if l[j] <= current_sl:
                    exit_price = current_sl
                    exit_bar = j
                    exit_reason = "BE" if be_hit else "SL"
                    break

                # Check TP3 (max target)
                if h[j] >= tp3:
                    exit_price = tp3
                    exit_bar = j
                    exit_reason = "TP3"
                    break

                # Check TP1 → start trailing
                if not tp1_hit and h[j] >= tp1:
                    tp1_hit = True
                    trailing = True
                    trail_peak = h[j]

                # Break-even at 1R
                if not be_hit and h[j] >= one_r:
                    be_hit = True

                # Trailing stop
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

        # If no exit found, close at last bar
        if exit_price is None:
            exit_price = c[min(bar + 199, n - 1)]
            exit_bar = min(bar + 199, n - 1)
            exit_reason = "TIMEOUT"

        pnl_pts = (exit_price - entry_price) * direction
        rr = pnl_pts / risk if risk > 0 else 0

        score = 0
        if hasattr(sig, 'confluence_score'):
            score = sig.confluence_score
        elif hasattr(sig, 'score'):
            score = sig.score

        trades.append({
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
        })

    # ─── Compute metrics ───
    if not trades:
        return {"total_trades": 0, "win_rate": 0, "total_return": 0,
                "profit_factor": 0, "avg_rr": 0, "max_drawdown": 0}

    wins = [t for t in trades if t["pnl_pts"] > 0]
    losses = [t for t in trades if t["pnl_pts"] <= 0]

    total_win_pts = sum(t["pnl_pts"] for t in wins)
    total_loss_pts = abs(sum(t["pnl_pts"] for t in losses))

    pf = total_win_pts / max(total_loss_pts, 0.01)
    wr = len(wins) / len(trades) * 100

    # Equity curve for drawdown
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

    # ─── CIPHER ───
    if strategy in ("all", "cipher"):
        logger.info("Running Cipher engine...")
        cipher = CipherEngine(preset["cipher"])
        cipher_sigs = cipher.run(df)
        logger.info(f"  Cipher signals: {len(cipher_sigs)}")
        if cipher_sigs:
            cipher_results = simulate_trades(cipher_sigs, df, preset)
            results["cipher"] = cipher_results
            _print_results("CIPHER", cipher_results)

    # ─── PARALLAX ───
    if strategy in ("all", "parallax"):
        logger.info("Running Parallax engine...")
        parallax = ParallaxEngine(preset["parallax"])
        parallax_sigs = parallax.run(df)
        logger.info(f"  Parallax signals: {len(parallax_sigs)}")
        if parallax_sigs:
            parallax_results = simulate_trades(parallax_sigs, df, preset)
            results["parallax"] = parallax_results
            _print_results("PARALLAX", parallax_results)

    # ─── COMBINED ───
    if strategy in ("all", "combined"):
        logger.info("Running Combined engine...")
        combined = CombinedEngine(preset)
        combined_sigs = combined.run(df)
        logger.info(f"  Combined signals: {len(combined_sigs)}")
        if combined_sigs:
            combined_results = simulate_trades(combined_sigs, df, preset)
            results["combined"] = combined_results
            _print_results("COMBINED", combined_results)

            # Show top signals by score
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
    logger.info(f"  Exits: TP3={r['exit_reasons']['TP3']} TRAIL={r['exit_reasons']['TRAIL']} SL={r['exit_reasons']['SL']} BE={r['exit_reasons']['BE']}")
    if r['avg_score'] > 0:
        logger.info(f"  Avg Signal Score: {r['avg_score']:.1f}")


def save_to_db(ticker: str, timeframe: str, strategy_name: str, results: dict):
    """Save backtest results to SQLite."""
    conn = connect()
    cursor = conn.cursor()

    # Insert or get strategy
    cursor.execute(
        "INSERT OR IGNORE INTO strategies (name, category, source_file) VALUES (?, ?, ?)",
        (f"GB_{strategy_name}_{ticker}", "custom", f"strategies/custom/{strategy_name}_engine.py")
    )
    conn.commit()

    cursor.execute("SELECT id FROM strategies WHERE name = ?", (f"GB_{strategy_name}_{ticker}",))
    row = cursor.fetchone()
    if not row:
        return
    strategy_id = row[0]

    # Insert backtest result
    cursor.execute("""
        INSERT INTO backtest_results
        (strategy_id, symbol, timeframe, total_trades, wins, losses,
         win_rate, total_return, max_drawdown, profit_factor, avg_rr, composite_score, status, run_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        strategy_id, ticker, timeframe,
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
    ))
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

            except Exception as e:
                logger.error(f"Error testing {ticker} {tf}: {e}")
                import traceback
                traceback.print_exc()

    print("\n" + "═" * 60)
    print("DONE. SQLite is truth.")
    print("═" * 60)


if __name__ == "__main__":
    main()
