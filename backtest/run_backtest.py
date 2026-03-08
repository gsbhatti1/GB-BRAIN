"""
GB-BRAIN — Backtest Engine
============================
Runs backtests for extracted strategies against cached market data.
Saves results to SQLite. Supports multiple strategy types.

Usage:
    python backtest/run_backtest.py                  # Run all pending
    python backtest/run_backtest.py --limit 100      # Run 100
    python backtest/run_backtest.py --symbol ETHUSDT  # One ticker
"""

import os
import sys
import json
import warnings
import argparse
from pathlib import Path
from datetime import datetime

import pandas as pd
import ta
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from config.settings import (
    ALL_TICKERS, TIMEFRAMES, DATA_CACHE_DIR,
    BACKTEST_CASH, BACKTEST_COMMISSION, MIN_TRADES,
)
from db.brain_db import connect, insert_backtest


# ══════════════════════════════════════════════
# Strategy Classes — each handles a type
# ══════════════════════════════════════════════

class TrendMomentumStrat(Strategy):
    """EMA crossover + RSI filter. The most common combo."""
    ema_fast = 9
    ema_slow = 21
    rsi_period = 14
    rsi_buy = 50
    rsi_sell = 50

    def init(self):
        close = pd.Series(self.data.Close)
        self.ema_f = self.I(lambda: ta.trend.EMAIndicator(close, self.ema_fast).ema_indicator().values)
        self.ema_s = self.I(lambda: ta.trend.EMAIndicator(close, self.ema_slow).ema_indicator().values)
        self.rsi = self.I(lambda: ta.momentum.RSIIndicator(close, self.rsi_period).rsi().values)

    def next(self):
        if crossover(self.ema_f, self.ema_s) and self.rsi[-1] > self.rsi_buy:
            self.buy()
        elif crossover(self.ema_s, self.ema_f) and self.position:
            self.position.close()
        elif self.rsi[-1] > 80 and self.position:
            self.position.close()


class MACDCrossStrat(Strategy):
    """MACD line crosses signal line."""
    fast = 12
    slow = 26
    signal = 9

    def init(self):
        close = pd.Series(self.data.Close)
        m = ta.trend.MACD(close, self.fast, self.slow, self.signal)
        self.macd = self.I(lambda: m.macd().values)
        self.macd_signal = self.I(lambda: m.macd_signal().values)

    def next(self):
        if crossover(self.macd, self.macd_signal):
            self.buy()
        elif crossover(self.macd_signal, self.macd) and self.position:
            self.position.close()


class MACrossStrat(Strategy):
    """Simple moving average crossover."""
    fast = 10
    slow = 20

    def init(self):
        close = pd.Series(self.data.Close)
        self.fma = self.I(lambda: close.rolling(self.fast).mean().values)
        self.sma = self.I(lambda: close.rolling(self.slow).mean().values)

    def next(self):
        if crossover(self.fma, self.sma):
            self.buy()
        elif crossover(self.sma, self.fma) and self.position:
            self.position.close()


class RSIReversalStrat(Strategy):
    """RSI oversold buy / overbought sell."""
    rsi_period = 14
    oversold = 30
    overbought = 70

    def init(self):
        close = pd.Series(self.data.Close)
        self.rsi = self.I(lambda: ta.momentum.RSIIndicator(close, self.rsi_period).rsi().values)

    def next(self):
        if self.rsi[-1] < self.oversold:
            self.buy()
        elif self.rsi[-1] > self.overbought and self.position:
            self.position.close()


class MeanReversionStrat(Strategy):
    """Bollinger Bands mean reversion."""
    period = 20
    std = 2

    def init(self):
        close = pd.Series(self.data.Close)
        bb = ta.volatility.BollingerBands(close, self.period, self.std)
        self.upper = self.I(lambda: bb.bollinger_hband().values)
        self.lower = self.I(lambda: bb.bollinger_lband().values)
        self.mid = self.I(lambda: bb.bollinger_mavg().values)

    def next(self):
        if self.data.Close[-1] < self.lower[-1]:
            self.buy()
        elif self.data.Close[-1] > self.upper[-1] and self.position:
            self.position.close()


class TrendFollowingStrat(Strategy):
    """Supertrend-style: EMA trend + ATR-based stops."""
    ema_period = 50
    atr_period = 14
    atr_mult = 2.0

    def init(self):
        close = pd.Series(self.data.Close)
        high = pd.Series(self.data.High)
        low = pd.Series(self.data.Low)
        self.ema = self.I(lambda: ta.trend.EMAIndicator(close, self.ema_period).ema_indicator().values)
        self.atr = self.I(lambda: ta.volatility.AverageTrueRange(high, low, close, self.atr_period).average_true_range().values)

    def next(self):
        if self.data.Close[-1] > self.ema[-1] and not self.position:
            self.buy(sl=self.data.Close[-1] - self.atr[-1] * self.atr_mult)
        elif self.data.Close[-1] < self.ema[-1] and self.position:
            self.position.close()


class MultiIndicatorStrat(Strategy):
    """Combined: EMA + RSI + MACD for high-confidence entries."""
    ema_fast = 9
    ema_slow = 21
    rsi_period = 14

    def init(self):
        close = pd.Series(self.data.Close)
        self.ema_f = self.I(lambda: ta.trend.EMAIndicator(close, self.ema_fast).ema_indicator().values)
        self.ema_s = self.I(lambda: ta.trend.EMAIndicator(close, self.ema_slow).ema_indicator().values)
        self.rsi = self.I(lambda: ta.momentum.RSIIndicator(close, self.rsi_period).rsi().values)
        m = ta.trend.MACD(close)
        self.macd = self.I(lambda: m.macd().values)
        self.macd_sig = self.I(lambda: m.macd_signal().values)

    def next(self):
        ema_bull = self.ema_f[-1] > self.ema_s[-1]
        rsi_ok = 40 < self.rsi[-1] < 70
        macd_bull = self.macd[-1] > self.macd_sig[-1]

        if ema_bull and rsi_ok and macd_bull and not self.position:
            self.buy()
        elif (not ema_bull or self.rsi[-1] > 80) and self.position:
            self.position.close()


# ── Strategy type mapping ────────────────────
STRATEGY_MAP = {
    "trend_momentum":  TrendMomentumStrat,
    "macd_crossover":  MACDCrossStrat,
    "ma_crossover":    MACrossStrat,
    "rsi_reversal":    RSIReversalStrat,
    "mean_reversion":  MeanReversionStrat,
    "trend_following": TrendFollowingStrat,
    "multi_indicator": MultiIndicatorStrat,
    "stoch_reversal":  RSIReversalStrat,  # Fallback
    "unknown":         MACrossStrat,       # Fallback
}


def load_data(symbol, timeframe):
    """Load cached OHLCV data."""
    # Try different filename patterns
    clean_symbol = symbol.replace("^", "")
    for fname in [f"{symbol}_{timeframe}.csv", f"{clean_symbol}_{timeframe}.csv"]:
        path = DATA_CACHE_DIR / fname
        if path.exists():
            df = pd.read_csv(path, index_col=0, parse_dates=True)
            df.columns = [c.capitalize() for c in df.columns]
            df = df.dropna()
            return df
    return None


def apply_parameters(strat_class, params):
    """Create a strategy class with custom parameters applied."""
    if not params:
        return strat_class

    overrides = {}
    p = params if isinstance(params, dict) else json.loads(params)

    # Map extracted parameters to strategy class attributes
    for key, val in p.items():
        key_lower = key.lower()
        if "ema_fast" in key_lower or "fast" in key_lower:
            if hasattr(strat_class, "ema_fast"):
                overrides["ema_fast"] = int(val)
            elif hasattr(strat_class, "fast"):
                overrides["fast"] = int(val)
        elif "ema_slow" in key_lower or "slow" in key_lower:
            if hasattr(strat_class, "ema_slow"):
                overrides["ema_slow"] = int(val)
            elif hasattr(strat_class, "slow"):
                overrides["slow"] = int(val)
        elif "rsi" in key_lower and "period" in key_lower:
            if hasattr(strat_class, "rsi_period"):
                overrides["rsi_period"] = int(val)
        elif "period" in key_lower:
            if hasattr(strat_class, "period"):
                overrides["period"] = int(val)

    if not overrides:
        return strat_class

    # Create subclass with overridden defaults
    new_class = type(
        f"{strat_class.__name__}_custom",
        (strat_class,),
        overrides,
    )
    return new_class


def run_single_backtest(strategy_row, symbol, timeframe):
    """Run one backtest. Returns result dict or None."""
    df = load_data(symbol, timeframe)
    if df is None or len(df) < 100:
        return None

    # Determine strategy class
    # First check indicators JSON for type mapping
    indicators = []
    try:
        ind_json = strategy_row["indicators"]
        if ind_json:
            indicators = json.loads(ind_json)
    except (json.JSONDecodeError, TypeError):
        pass

    # Use extracted parameters
    params = None
    try:
        p_json = strategy_row["parameters"]
        if p_json:
            params = json.loads(p_json)
    except (json.JSONDecodeError, TypeError):
        pass

    # Pick strategy class based on indicator combo
    if "EMA" in indicators and "RSI" in indicators and "MACD" in indicators:
        strat_cls = MultiIndicatorStrat
    elif "EMA" in indicators and "RSI" in indicators:
        strat_cls = TrendMomentumStrat
    elif "MACD" in indicators:
        strat_cls = MACDCrossStrat
    elif "BB" in indicators:
        strat_cls = MeanReversionStrat
    elif "Supertrend" in indicators or "ATR" in indicators:
        strat_cls = TrendFollowingStrat
    elif "RSI" in indicators:
        strat_cls = RSIReversalStrat
    elif "EMA" in indicators or "SMA" in indicators:
        strat_cls = MACrossStrat
    else:
        strat_cls = MACrossStrat

    # Apply custom parameters
    strat_cls = apply_parameters(strat_cls, params)

    try:
        bt = Backtest(df, strat_cls, cash=BACKTEST_CASH, commission=BACKTEST_COMMISSION)
        stats = bt.run()

        if stats["# Trades"] < MIN_TRADES:
            return None

        win_rate = round(stats["Win Rate [%]"], 2)
        total_return = round(stats["Return [%]"], 2)
        max_dd = round(stats["Max. Drawdown [%]"], 2)

        # Calculate profit factor
        equity = stats.get("_equity_curve", None)
        profit_factor = 0.0
        if hasattr(stats, "_trades") and len(stats._trades) > 0:
            wins_sum = stats._trades[stats._trades["PnL"] > 0]["PnL"].sum()
            loss_sum = abs(stats._trades[stats._trades["PnL"] < 0]["PnL"].sum())
            profit_factor = round(wins_sum / loss_sum, 2) if loss_sum > 0 else 99.0

        return {
            "strategy_id": strategy_row["id"],
            "symbol": symbol,
            "timeframe": timeframe,
            "data_source": "binance" if "USDT" in symbol else "yahoo",
            "total_trades": stats["# Trades"],
            "wins": int(stats["# Trades"] * win_rate / 100),
            "losses": stats["# Trades"] - int(stats["# Trades"] * win_rate / 100),
            "win_rate": win_rate,
            "total_return": total_return,
            "max_drawdown": max_dd,
            "profit_factor": profit_factor,
            "sharpe_ratio": round(stats.get("Sharpe Ratio", 0) or 0, 2),
        }
    except Exception as e:
        return None


def run_all_backtests(symbols=None, timeframes=None, limit=None):
    """Run backtests for all extracted strategies."""
    conn = connect()

    # Get strategies that have been extracted but not yet fully tested
    if limit:
        rows = conn.execute(
            """SELECT * FROM strategies
               WHERE status IN ('extracted', 'pending')
               AND indicators IS NOT NULL
               LIMIT ?""",
            (limit,),
        ).fetchall()
    else:
        rows = conn.execute(
            """SELECT * FROM strategies
               WHERE status IN ('extracted', 'pending')
               AND indicators IS NOT NULL"""
        ).fetchall()

    if not rows:
        print("[INFO] No strategies to backtest.")
        conn.close()
        return

    tickers = symbols or ALL_TICKERS
    tfs = timeframes or TIMEFRAMES
    total = len(rows) * len(tickers) * len(tfs)

    print("=" * 60)
    print("GB-BRAIN — Backtest Engine")
    print(f"Strategies: {len(rows)} | Tickers: {len(tickers)} | TFs: {len(tfs)}")
    print(f"Total combinations: {total:,}")
    print("=" * 60)

    stats = {"run": 0, "hits": 0, "skipped": 0}

    for si, strat in enumerate(rows):
        for symbol in tickers:
            for tf in tfs:
                result = run_single_backtest(strat, symbol, tf)
                stats["run"] += 1

                if result:
                    insert_backtest(conn, **result)
                    stats["hits"] += 1
                else:
                    stats["skipped"] += 1

                if stats["run"] % 500 == 0:
                    pct = round(stats["run"] / total * 100, 1)
                    print(
                        f"  [{stats['run']:,}/{total:,}] ({pct}%) "
                        f"hits: {stats['hits']:,} | skip: {stats['skipped']:,}"
                    )

        # Mark strategy as tested
        conn.execute(
            "UPDATE strategies SET status = 'tested', updated_at = datetime('now') WHERE id = ?",
            (strat["id"],),
        )
        conn.commit()

    conn.close()

    print(f"\n{'=' * 60}")
    print("BACKTESTING COMPLETE")
    print(f"  Combinations run: {stats['run']:,}")
    print(f"  Valid results:    {stats['hits']:,}")
    print(f"  Skipped:          {stats['skipped']:,}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GB-BRAIN Backtest Engine")
    parser.add_argument("--limit", "-l", type=int, help="Max strategies to test")
    parser.add_argument("--symbol", "-s", type=str, help="Single symbol to test")
    parser.add_argument("--timeframe", "-t", type=str, help="Single timeframe")
    args = parser.parse_args()

    symbols = [args.symbol] if args.symbol else None
    tfs = [args.timeframe] if args.timeframe else None
    run_all_backtests(symbols=symbols, timeframes=tfs, limit=args.limit)
