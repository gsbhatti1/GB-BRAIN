"""
GB-BRAIN - Bot Runner
======================
Takes a GEM strategy from the database and runs it live/paper.
Fetches candles, computes indicators, generates signals, executes trades.

Usage:
    python execute/bot_runner.py --strategy "Bollinger-Bands-Standard-Deviation-Breakout" --broker oanda --symbol SPX --paper
    python execute/bot_runner.py --strategy "keithorange_FreqTrade" --broker blofin --symbol SOL --paper
    python execute/bot_runner.py --list   # Show available GEM strategies
"""

import sys
import time
import json
import logging
import argparse
from pathlib import Path
from datetime import datetime

import pandas as pd
import ta

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from config.settings import BACKTEST_COMMISSION
from execute.risk_manager import RiskManager
from execute.telegram_alerts import send_alert, send_trade_alert, send_error
from db.brain_db import connect

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("gb_brain.bot")


class SignalEngine:
    """Generates buy/sell signals from candle data using strategy parameters."""

    def __init__(self, params):
        self.p = params
        self.ma_fast = int(params.get("ma_fast", 9))
        self.ma_slow = int(params.get("ma_slow", 21))
        self.rsi_period = int(params.get("rsi_period", 14))
        self.rsi_ob = int(params.get("rsi_overbought", 70))
        self.rsi_os = int(params.get("rsi_oversold", 30))
        self.bb_period = int(params.get("bb_period", 20))
        self.bb_std = float(params.get("bb_std", 2.0))

    def compute(self, df):
        """Add indicators to dataframe."""
        close = df["close"]
        df["ema_fast"] = ta.trend.EMAIndicator(close, self.ma_fast).ema_indicator()
        df["ema_slow"] = ta.trend.EMAIndicator(close, self.ma_slow).ema_indicator()
        df["rsi"] = ta.momentum.RSIIndicator(close, self.rsi_period).rsi()
        bb = ta.volatility.BollingerBands(close, self.bb_period, self.bb_std)
        df["bb_upper"] = bb.bollinger_hband()
        df["bb_lower"] = bb.bollinger_lband()
        df["bb_mid"] = bb.bollinger_mavg()
        m = ta.trend.MACD(close)
        df["macd"] = m.macd()
        df["macd_signal"] = m.macd_signal()
        return df

    def signal(self, df):
        """Generate signal from latest data. Returns 'buy', 'sell', or None."""
        if len(df) < max(self.ma_slow, self.bb_period) + 5:
            return None

        row = df.iloc[-1]
        prev = df.iloc[-2]

        # EMA crossover
        ema_cross_up = prev["ema_fast"] <= prev["ema_slow"] and row["ema_fast"] > row["ema_slow"]
        ema_cross_dn = prev["ema_fast"] >= prev["ema_slow"] and row["ema_fast"] < row["ema_slow"]
        ema_bull = row["ema_fast"] > row["ema_slow"]

        # RSI conditions
        rsi_buy = row["rsi"] < self.rsi_os or (row["rsi"] > self.rsi_os and row["rsi"] < 60)
        rsi_sell = row["rsi"] > self.rsi_ob

        # BB conditions
        bb_buy = row["close"] < row["bb_lower"]
        bb_sell = row["close"] > row["bb_upper"]

        # MACD
        macd_bull = row["macd"] > row["macd_signal"]

        # Combined signal
        buy_signals = sum([ema_cross_up, bb_buy, rsi_buy and ema_bull, macd_bull and ema_cross_up])
        sell_signals = sum([ema_cross_dn, bb_sell, rsi_sell, not macd_bull and ema_cross_dn])

        if buy_signals >= 2:
            return "buy"
        if sell_signals >= 2:
            return "sell"
        return None


def fetch_live_candles(broker, symbol, timeframe="1h", limit=100):
    """Fetch recent candles from broker or data source."""
    if broker == "blofin":
        from execute.blofin_bridge import BloFinBridge
        bridge = BloFinBridge(use_demo=True)
        inst = bridge._resolve(symbol)
        # BloFin candle endpoint
        tf_map = {"5m": "5m", "15m": "15m", "1h": "1H", "4h": "4H"}
        result = bridge._get("/api/v1/market/candles", {
            "instId": inst,
            "bar": tf_map.get(timeframe, "1H"),
            "limit": str(limit),
        })
        data = result.get("data", [])
        if not data:
            return None
        df = pd.DataFrame(data, columns=["timestamp", "open", "high", "low", "close", "volume", "volCcy"])
        df["timestamp"] = pd.to_datetime(df["timestamp"].astype(int), unit="ms")
        df.set_index("timestamp", inplace=True)
        for c in ["open", "high", "low", "close", "volume"]:
            df[c] = df[c].astype(float)
        return df.sort_index()

    elif broker == "binance":
        from binance.client import Client
        from config.settings import BINANCE_KEY, BINANCE_SECRET
        client = Client(BINANCE_KEY, BINANCE_SECRET)
        klines = client.get_historical_klines(symbol, timeframe, f"{limit * 2} hours ago UTC")
        if not klines:
            return None
        cols = ["timestamp", "open", "high", "low", "close", "volume",
                "ct", "qv", "t", "tbb", "tbq", "ignore"]
        df = pd.DataFrame(klines, columns=cols)
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df.set_index("timestamp", inplace=True)
        for c in ["open", "high", "low", "close", "volume"]:
            df[c] = df[c].astype(float)
        return df[["open", "high", "low", "close", "volume"]].tail(limit)

    elif broker == "oanda":
        # For OANDA we use Yahoo as data source
        import yfinance as yf
        yf_map = {"NAS100": "^NDX", "US30": "^DJI", "SPX": "^GSPC", "SPX500": "^GSPC"}
        ticker = yf_map.get(symbol, symbol)
        tf_map = {"5m": "5m", "15m": "15m", "1h": "1h"}
        df = yf.download(ticker, period="7d", interval=tf_map.get(timeframe, "1h"),
                         progress=False, auto_adjust=True)
        if df.empty:
            return None
        if hasattr(df.columns, 'levels') and df.columns.nlevels > 1:
            df.columns = df.columns.get_level_values(0)
        df.columns = [c.lower() for c in df.columns]
        return df[["open", "high", "low", "close", "volume"]].tail(limit)

    return None


def run_bot(strategy_name, broker, symbol, timeframe="1h",
            paper=True, leverage=1, loop_interval=60):
    """Main bot loop."""
    conn = connect()

    # Load strategy from DB
    strat = conn.execute(
        "SELECT * FROM strategies WHERE name LIKE ? AND status = 'gem' LIMIT 1",
        (f"%{strategy_name}%",),
    ).fetchone()

    if not strat:
        # Try broader search
        strat = conn.execute(
            "SELECT * FROM strategies WHERE name LIKE ? LIMIT 1",
            (f"%{strategy_name}%",),
        ).fetchone()

    if not strat:
        print(f"[ERROR] Strategy not found: {strategy_name}")
        conn.close()
        return

    params = json.loads(strat["parameters"]) if strat["parameters"] else {}
    print(f"Strategy: {strat['name']}")
    print(f"Parameters: {params}")
    print(f"Broker: {broker} | Symbol: {symbol} | TF: {timeframe}")
    print(f"Paper: {paper} | Leverage: {leverage}")
    conn.close()

    # Setup
    engine = SignalEngine(params)
    risk = RiskManager()

    # Get initial balance
    try:
        if broker == "oanda":
            from execute.oanda_bridge import get_account_balance
            info = get_account_balance()
            balance = info["nav"]
        elif broker == "blofin":
            from execute.blofin_bridge import BloFinBridge
            bridge = BloFinBridge(use_demo=paper)
            info = bridge.get_balance()
            balance = info["equity"]
        else:
            balance = 10000  # Default for testing
    except Exception as e:
        print(f"[WARN] Could not get balance: {e}. Using $10,000 default.")
        balance = 10000

    risk.initialize(balance)
    send_alert(
        f"Bot started: {strat['name'][:40]}\n"
        f"  Broker: {broker} | {symbol} {timeframe}\n"
        f"  Balance: ${balance:.2f} | Paper: {paper}"
    )

    position = None  # None, "long", "short"
    entry_price = 0

    print(f"\nBot running. Checking every {loop_interval}s. Press Ctrl+C to stop.\n")

    try:
        while True:
            # Fetch candles
            df = fetch_live_candles(broker, symbol, timeframe)
            if df is None or len(df) < 50:
                logger.warning("Not enough candle data")
                time.sleep(loop_interval)
                continue

            # Compute indicators and get signal
            df = engine.compute(df)
            signal = engine.signal(df)
            price = float(df.iloc[-1]["close"])

            # Risk check
            can_trade, reason = risk.can_trade()

            ts = datetime.now().strftime("%H:%M:%S")

            if signal == "buy" and position is None and can_trade:
                units = risk.position_size(balance, price, leverage)
                if units > 0:
                    print(f"[{ts}] BUY {symbol} @ {price:.2f} | {units} units")
                    if not paper:
                        try:
                            if broker == "oanda":
                                from execute.oanda_bridge import place_order
                                place_order(symbol, int(units))
                            elif broker == "blofin":
                                bridge.place_order(symbol, "buy", units, leverage)
                        except Exception as e:
                            send_error("bot_buy", e)
                            time.sleep(loop_interval)
                            continue
                    position = "long"
                    entry_price = price
                    send_trade_alert("fill", symbol, "buy", units, price)

            elif signal == "sell" and position == "long":
                pnl = (price - entry_price) / entry_price * 100
                print(f"[{ts}] SELL {symbol} @ {price:.2f} | PnL: {pnl:+.2f}%")
                if not paper:
                    try:
                        if broker == "oanda":
                            from execute.oanda_bridge import close_position
                            close_position(symbol)
                        elif broker == "blofin":
                            bridge.close_position(symbol, "sell")
                    except Exception as e:
                        send_error("bot_sell", e)
                pnl_abs = (price - entry_price) * risk.position_size(balance, entry_price, leverage)
                risk.record_trade(pnl_abs, "sell")
                send_trade_alert("fill", symbol, "sell", 0, price, pnl_abs)
                position = None
                entry_price = 0

            elif not can_trade:
                logger.info(f"[{ts}] Risk block: {reason}")
            else:
                logger.debug(f"[{ts}] No signal | RSI:{df.iloc[-1]['rsi']:.1f} Price:{price:.2f}")

            time.sleep(loop_interval)

    except KeyboardInterrupt:
        print("\nBot stopped by user.")
        send_alert(f"Bot stopped: {strat['name'][:40]}\n{risk.report()}")


def list_gems():
    """List available GEM strategies."""
    conn = connect()
    rows = conn.execute("""
        SELECT s.name, br.symbol, br.timeframe, br.win_rate, br.total_return,
               br.profit_factor, br.total_trades
        FROM backtest_results br JOIN strategies s ON s.id = br.strategy_id
        WHERE br.status = 'GEM' ORDER BY br.composite_score DESC LIMIT 50
    """).fetchall()
    conn.close()

    print(f"\n{'=' * 90}")
    print(f"TOP {len(rows)} GEM STRATEGIES")
    print(f"{'=' * 90}")
    print(f"{'Strategy':<45} {'Symbol':<10} {'TF':<4} {'Win%':>5} {'Ret%':>7} {'PF':>5}")
    print("-" * 90)
    for r in rows:
        print(f"{r['name'][:45]:<45} {r['symbol']:<10} {r['timeframe']:<4} "
              f"{r['win_rate']:>5.1f} {r['total_return']:>+7.1f} {r['profit_factor']:>5.1f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GB-BRAIN Bot Runner")
    parser.add_argument("--strategy", "-s", type=str, help="Strategy name (partial match)")
    parser.add_argument("--broker", "-b", default="oanda", choices=["oanda", "blofin", "binance"])
    parser.add_argument("--symbol", type=str, default="SPX", help="Trading symbol")
    parser.add_argument("--timeframe", "-t", default="1h", help="Candle timeframe")
    parser.add_argument("--leverage", "-l", type=int, default=1)
    parser.add_argument("--interval", type=int, default=60, help="Loop interval seconds")
    parser.add_argument("--paper", action="store_true", default=True, help="Paper trading (default)")
    parser.add_argument("--live", action="store_true", help="LIVE trading (real money)")
    parser.add_argument("--list", action="store_true", help="List available GEM strategies")
    args = parser.parse_args()

    if args.list:
        list_gems()
    elif args.strategy:
        paper = not args.live
        run_bot(args.strategy, args.broker, args.symbol, args.timeframe,
                paper=paper, leverage=args.leverage, loop_interval=args.interval)
    else:
        print("Use --list to see GEMs, or --strategy NAME to run a bot.")
        print("Example:")
        print('  python execute/bot_runner.py --list')
        print('  python execute/bot_runner.py --strategy "Bollinger" --broker oanda --symbol SPX --paper')
