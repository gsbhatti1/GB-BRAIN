"""
GB-BRAIN - Grid Bot for BloFin
================================
Signal-driven grid trading for crypto futures.

How it works:
  1. GEM strategy generates a direction signal (LONG or SHORT)
  2. Grid bot opens multiple entries at different price levels
  3. Each grid has its own take-profit target
  4. When signal reverses or stop-loss hit → close all grids
  5. Risk manager controls everything

Grid modes:
  ARITHMETIC: Equal $ spacing between grids (good for ranging)
  GEOMETRIC:  Equal % spacing between grids (good for trending)

Usage:
    python execute/grid_bot.py --symbol ETH --leverage 3 --grids 10 --paper
    python execute/grid_bot.py --symbol SOL --leverage 5 --grids 15 --paper
    python execute/grid_bot.py --config   # Show current config
"""

import sys
import time
import json
import logging
import argparse
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, field

import pandas as pd
import ta

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from config.settings import BLOFIN_KEY, BLOFIN_SECRET, BLOFIN_PASS
from execute.risk_manager import RiskManager
from execute.telegram_alerts import send_alert, send_trade_alert, send_error
from db.brain_db import connect

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("gb_brain.grid")


# ══════════════════════════════════════════════
# Grid Configuration
# ══════════════════════════════════════════════

@dataclass
class GridConfig:
    symbol: str = "ETH"
    leverage: int = 3
    num_grids: int = 10
    grid_spacing_pct: float = 0.005     # 0.5% between grids
    take_profit_pct: float = 0.01       # 1% TP per grid
    stop_loss_pct: float = 0.03         # 3% SL for entire position
    max_position_pct: float = 0.50      # Use 50% of balance
    timeframe: str = "15m"              # Signal timeframe
    signal_check_interval: int = 60     # Seconds between checks
    use_demo: bool = True
    grid_mode: str = "geometric"        # arithmetic or geometric

    # Strategy parameters (from GEM)
    ema_fast: int = 9
    ema_slow: int = 21
    rsi_period: int = 14
    rsi_overbought: int = 70
    rsi_oversold: int = 30
    bb_period: int = 20
    bb_std: float = 2.0


# ══════════════════════════════════════════════
# Grid State Tracking
# ══════════════════════════════════════════════

@dataclass
class GridLevel:
    level: int
    entry_price: float
    size: float
    tp_price: float
    status: str = "pending"  # pending, filled, tp_hit, cancelled
    order_id: str = ""
    filled_at: float = 0.0


@dataclass
class GridState:
    direction: str = ""         # "long" or "short" or ""
    grids: list = field(default_factory=list)
    total_invested: float = 0.0
    avg_entry: float = 0.0
    unrealized_pnl: float = 0.0
    is_active: bool = False


# ══════════════════════════════════════════════
# Signal Engine (same as bot_runner but tuned for grid)
# ══════════════════════════════════════════════

class GridSignalEngine:
    """Generates direction signals for grid entries."""

    def __init__(self, cfg: GridConfig):
        self.cfg = cfg

    def compute_indicators(self, df):
        close = df["close"]
        df["ema_fast"] = ta.trend.EMAIndicator(close, self.cfg.ema_fast).ema_indicator()
        df["ema_slow"] = ta.trend.EMAIndicator(close, self.cfg.ema_slow).ema_indicator()
        df["rsi"] = ta.momentum.RSIIndicator(close, self.cfg.rsi_period).rsi()
        bb = ta.volatility.BollingerBands(close, self.cfg.bb_period, self.cfg.bb_std)
        df["bb_upper"] = bb.bollinger_hband()
        df["bb_lower"] = bb.bollinger_lband()
        df["bb_mid"] = bb.bollinger_mavg()
        m = ta.trend.MACD(close)
        df["macd"] = m.macd()
        df["macd_signal"] = m.macd_signal()
        atr = ta.volatility.AverageTrueRange(df["high"], df["low"], close, 14)
        df["atr"] = atr.average_true_range()
        return df

    def get_signal(self, df):
        """Returns 'long', 'short', or None."""
        if len(df) < max(self.cfg.ema_slow, self.cfg.bb_period) + 5:
            return None

        row = df.iloc[-1]
        prev = df.iloc[-2]

        # Trend
        ema_bull = row["ema_fast"] > row["ema_slow"]
        ema_cross_up = prev["ema_fast"] <= prev["ema_slow"] and row["ema_fast"] > row["ema_slow"]
        ema_cross_dn = prev["ema_fast"] >= prev["ema_slow"] and row["ema_fast"] < row["ema_slow"]

        # RSI
        rsi_buy = row["rsi"] < self.cfg.rsi_oversold
        rsi_sell = row["rsi"] > self.cfg.rsi_overbought
        rsi_neutral = self.cfg.rsi_oversold < row["rsi"] < self.cfg.rsi_overbought

        # BB
        bb_buy = row["close"] < row["bb_lower"]
        bb_sell = row["close"] > row["bb_upper"]

        # MACD
        macd_bull = row["macd"] > row["macd_signal"]

        # Score signals
        long_score = sum([ema_cross_up, ema_bull and rsi_buy, bb_buy, macd_bull and ema_bull])
        short_score = sum([ema_cross_dn, not ema_bull and rsi_sell, bb_sell, not macd_bull and not ema_bull])

        if long_score >= 2:
            return "long"
        if short_score >= 2:
            return "short"
        return None

    def get_atr(self, df):
        """Get current ATR for dynamic grid spacing."""
        if "atr" in df.columns and len(df) > 0:
            return float(df.iloc[-1]["atr"])
        return 0.0


# ══════════════════════════════════════════════
# Grid Bot Core
# ══════════════════════════════════════════════

class GridBot:
    """Grid trading bot for BloFin futures."""

    def __init__(self, cfg: GridConfig):
        self.cfg = cfg
        self.state = GridState()
        self.risk = RiskManager()
        self.signal_engine = GridSignalEngine(cfg)
        self.bridge = None

    def _connect(self):
        """Connect to BloFin."""
        from execute.blofin_bridge import BloFinBridge
        self.bridge = BloFinBridge(use_demo=self.cfg.use_demo)
        ok, info = self.bridge.test_connection()
        if not ok:
            raise ConnectionError(f"BloFin connection failed: {info}")
        balance = info["equity"]
        self.risk.initialize(balance)
        logger.info(f"Connected to BloFin {'DEMO' if self.cfg.use_demo else 'LIVE'}")
        logger.info(f"Balance: ${balance:.2f} | Leverage: {self.cfg.leverage}x")
        return balance

    def _fetch_candles(self):
        """Fetch candles from BloFin."""
        symbol = f"{self.cfg.symbol}USDT"
        inst = self.bridge._resolve(symbol)
        tf_map = {"1m": "1m", "5m": "5m", "15m": "15m", "1h": "1H", "4h": "4H"}
        result = self.bridge._get("/api/v1/market/candles", {
            "instId": inst,
            "bar": tf_map.get(self.cfg.timeframe, "15m"),
            "limit": "100",
        })
        data = result.get("data", [])
        if not data:
            return None

        df = pd.DataFrame(data)
        df = df.iloc[:, :7]
        df.columns = ["timestamp", "open", "high", "low", "close", "volume", "volCcy"]
        df["timestamp"] = pd.to_datetime(df["timestamp"].astype(int), unit="ms")
        df.set_index("timestamp", inplace=True)
        for c in ["open", "high", "low", "close", "volume"]:
            df[c] = df[c].astype(float)
        return df.sort_index()

    def _calculate_grid_levels(self, price, direction, atr):
        """Calculate grid entry levels based on current price."""
        grids = []
        total_balance = self.risk.state.current_balance
        margin = total_balance * self.cfg.max_position_pct
        notional = margin * self.cfg.leverage

        # Calculate size per grid (heavier on better entries)
        weights = [(i + 1) for i in range(self.cfg.num_grids)]
        total_weight = sum(weights)

        for i in range(self.cfg.num_grids):
            # Grid spacing
            if self.cfg.grid_mode == "geometric":
                spacing = self.cfg.grid_spacing_pct * (i + 1)
            else:
                spacing = self.cfg.grid_spacing_pct * (i + 1)

            # Entry price
            if direction == "long":
                entry = price * (1 - spacing)
                tp = entry * (1 + self.cfg.take_profit_pct)
            else:
                entry = price * (1 + spacing)
                tp = entry * (1 - self.cfg.take_profit_pct)

            # Size (more on better entries)
            grid_notional = notional * weights[i] / total_weight
            size = round(grid_notional / entry, 4)

            grids.append(GridLevel(
                level=i + 1,
                entry_price=round(entry, 2),
                size=size,
                tp_price=round(tp, 2),
            ))

        return grids

    def _open_grid(self, direction, price, atr):
        """Open a new grid position."""
        grids = self._calculate_grid_levels(price, direction, atr)

        logger.info(f"\n{'=' * 50}")
        logger.info(f"OPENING {direction.upper()} GRID — {self.cfg.num_grids} levels")
        logger.info(f"Current price: ${price:.2f}")
        logger.info(f"{'=' * 50}")

        self.state.direction = direction
        self.state.grids = grids
        self.state.is_active = True

        # Place first grid at market (immediate entry)
        first = grids[0]
        side = "buy" if direction == "long" else "sell"

        if self.bridge:
            try:
                result = self.bridge.place_order(
                    f"{self.cfg.symbol}USDT", side, first.size, self.cfg.leverage
                )
                first.status = "filled"
                first.filled_at = time.time()
                first.order_id = str(result.get("data", [{}])[0].get("orderId", ""))
                self.state.total_invested += first.size * price
                self.state.avg_entry = price
                logger.info(f"  Grid 1: FILLED {side} {first.size} @ ${price:.2f}")
                send_trade_alert("fill", f"{self.cfg.symbol}-USDT", side, first.size, price)
            except Exception as e:
                logger.error(f"  Grid 1 FAILED: {e}")
                send_error("grid_open", e)
                return False

        # Log remaining grid levels
        for g in grids[1:]:
            logger.info(f"  Grid {g.level}: PENDING {side} {g.size} @ ${g.entry_price:.2f} → TP ${g.tp_price:.2f}")

        total_size = sum(g.size for g in grids)
        logger.info(f"\nTotal grid size: {total_size:.4f} {self.cfg.symbol}")
        logger.info(f"Avg grid spacing: {self.cfg.grid_spacing_pct*100:.1f}%")
        logger.info(f"TP per grid: {self.cfg.take_profit_pct*100:.1f}%")
        logger.info(f"SL: {self.cfg.stop_loss_pct*100:.1f}%")

        send_alert(
            f"GRID OPENED: {direction.upper()} {self.cfg.symbol}\n"
            f"  Grids: {self.cfg.num_grids} | Lev: {self.cfg.leverage}x\n"
            f"  Price: ${price:.2f}\n"
            f"  Total size: {total_size:.4f}"
        )
        return True

    def _check_grid_fills(self, current_price):
        """Check if any pending grids should be filled."""
        if not self.state.is_active:
            return

        direction = self.state.direction
        side = "buy" if direction == "long" else "sell"

        for g in self.state.grids:
            if g.status != "pending":
                continue

            # Check if price reached this grid level
            should_fill = False
            if direction == "long" and current_price <= g.entry_price:
                should_fill = True
            elif direction == "short" and current_price >= g.entry_price:
                should_fill = True

            if should_fill:
                if self.bridge:
                    try:
                        self.bridge.place_order(
                            f"{self.cfg.symbol}USDT", side, g.size, self.cfg.leverage
                        )
                        g.status = "filled"
                        g.filled_at = time.time()
                        self.state.total_invested += g.size * current_price
                        filled_count = sum(1 for x in self.state.grids if x.status == "filled")
                        total = sum(x.size * x.entry_price for x in self.state.grids if x.status == "filled")
                        total_size = sum(x.size for x in self.state.grids if x.status == "filled")
                        self.state.avg_entry = total / total_size if total_size > 0 else current_price

                        logger.info(f"  Grid {g.level}: FILLED {side} {g.size} @ ${current_price:.2f} (level {filled_count}/{self.cfg.num_grids})")
                        send_trade_alert("fill", f"{self.cfg.symbol}-USDT", side, g.size, current_price)
                    except Exception as e:
                        logger.error(f"  Grid {g.level} fill FAILED: {e}")

    def _check_take_profits(self, current_price):
        """Check if any filled grids hit their TP."""
        if not self.state.is_active:
            return

        direction = self.state.direction
        close_side = "sell" if direction == "long" else "buy"

        for g in self.state.grids:
            if g.status != "filled":
                continue

            hit_tp = False
            if direction == "long" and current_price >= g.tp_price:
                hit_tp = True
            elif direction == "short" and current_price <= g.tp_price:
                hit_tp = True

            if hit_tp:
                if self.bridge:
                    try:
                        self.bridge.place_order(
                            f"{self.cfg.symbol}USDT", close_side, g.size, self.cfg.leverage
                        )
                        pnl = abs(current_price - g.entry_price) * g.size
                        g.status = "tp_hit"
                        self.risk.record_trade(pnl, close_side)
                        logger.info(f"  Grid {g.level}: TP HIT @ ${current_price:.2f} | PnL: +${pnl:.2f}")
                        send_trade_alert("fill", f"{self.cfg.symbol}-USDT", close_side, g.size, current_price, pnl)
                    except Exception as e:
                        logger.error(f"  Grid {g.level} TP close FAILED: {e}")

    def _check_stop_loss(self, current_price):
        """Check if overall stop loss is hit."""
        if not self.state.is_active or self.state.avg_entry == 0:
            return False

        direction = self.state.direction
        if direction == "long":
            loss_pct = (self.state.avg_entry - current_price) / self.state.avg_entry
        else:
            loss_pct = (current_price - self.state.avg_entry) / self.state.avg_entry

        if loss_pct >= self.cfg.stop_loss_pct:
            logger.warning(f"STOP LOSS HIT: {loss_pct*100:.1f}% loss")
            self._close_all_grids(current_price, reason="stop_loss")
            return True
        return False

    def _close_all_grids(self, current_price, reason="signal"):
        """Close all open grid positions."""
        if not self.state.is_active:
            return

        close_side = "sell" if self.state.direction == "long" else "buy"
        total_pnl = 0

        for g in self.state.grids:
            if g.status == "filled":
                if self.bridge:
                    try:
                        self.bridge.place_order(
                            f"{self.cfg.symbol}USDT", close_side, g.size, self.cfg.leverage
                        )
                    except Exception as e:
                        logger.error(f"  Close grid {g.level} failed: {e}")

                if self.state.direction == "long":
                    pnl = (current_price - g.entry_price) * g.size
                else:
                    pnl = (g.entry_price - current_price) * g.size
                total_pnl += pnl
                g.status = "cancelled"

            elif g.status == "pending":
                g.status = "cancelled"

        self.risk.record_trade(total_pnl, close_side)
        self.state.is_active = False
        self.state.direction = ""

        logger.info(f"\nGRID CLOSED: reason={reason} | PnL: ${total_pnl:+.2f}")
        send_alert(
            f"GRID CLOSED: {self.cfg.symbol}\n"
            f"  Reason: {reason}\n"
            f"  PnL: ${total_pnl:+.2f}\n"
            f"  {self.risk.report()}"
        )

    def _grid_status(self):
        """Print current grid status."""
        if not self.state.is_active:
            return "No active grid"

        filled = sum(1 for g in self.state.grids if g.status == "filled")
        tp_hit = sum(1 for g in self.state.grids if g.status == "tp_hit")
        pending = sum(1 for g in self.state.grids if g.status == "pending")

        return (
            f"{self.state.direction.upper()} | "
            f"Filled: {filled} | TP: {tp_hit} | Pending: {pending} | "
            f"Avg: ${self.state.avg_entry:.2f}"
        )

    # ── Main Loop ────────────────────────────
    def run(self):
        """Main bot loop."""
        balance = self._connect()

        # Load best strategy params from DB
        self._load_gem_params()

        send_alert(
            f"GRID BOT STARTED: {self.cfg.symbol}-USDT\n"
            f"  Mode: {'DEMO' if self.cfg.use_demo else 'LIVE'}\n"
            f"  Balance: ${balance:.2f}\n"
            f"  Leverage: {self.cfg.leverage}x\n"
            f"  Grids: {self.cfg.num_grids}\n"
            f"  Spacing: {self.cfg.grid_spacing_pct*100:.1f}%\n"
            f"  TP: {self.cfg.take_profit_pct*100:.1f}% | SL: {self.cfg.stop_loss_pct*100:.1f}%"
        )

        logger.info(f"\nGrid bot running. Checking every {self.cfg.signal_check_interval}s.\n")

        try:
            while True:
                # Fetch candles
                df = self._fetch_candles()
                if df is None or len(df) < 50:
                    logger.warning("Not enough candle data")
                    time.sleep(self.cfg.signal_check_interval)
                    continue

                # Compute indicators
                df = self.signal_engine.compute_indicators(df)
                current_price = float(df.iloc[-1]["close"])
                atr = self.signal_engine.get_atr(df)
                signal = self.signal_engine.get_signal(df)

                ts = datetime.now().strftime("%H:%M:%S")

                # Risk check
                can_trade, reason = self.risk.can_trade()

                if self.state.is_active:
                    # Check grid fills, TPs, and SL
                    self._check_grid_fills(current_price)
                    self._check_take_profits(current_price)
                    sl_hit = self._check_stop_loss(current_price)

                    # Check for signal reversal
                    if not sl_hit and signal and signal != self.state.direction:
                        logger.info(f"[{ts}] Signal reversed to {signal} — closing grid")
                        self._close_all_grids(current_price, reason="signal_reversal")

                    # Check if all TPs hit
                    all_done = all(g.status in ("tp_hit", "cancelled") for g in self.state.grids)
                    if all_done and self.state.is_active:
                        logger.info(f"[{ts}] All grids completed")
                        self.state.is_active = False
                        self.state.direction = ""

                    logger.info(f"[{ts}] ${current_price:.2f} | {self._grid_status()}")

                else:
                    # No active grid — check for new signal
                    if signal and can_trade:
                        logger.info(f"[{ts}] Signal: {signal.upper()} @ ${current_price:.2f}")
                        self._open_grid(signal, current_price, atr)
                    elif not can_trade:
                        logger.info(f"[{ts}] ${current_price:.2f} | Risk: {reason}")
                    else:
                        rsi = df.iloc[-1]["rsi"]
                        logger.info(f"[{ts}] ${current_price:.2f} | RSI:{rsi:.1f} | Waiting for signal...")

                # Update balance
                if self.bridge:
                    try:
                        info = self.bridge.get_balance()
                        self.risk.update_balance(info["equity"])
                    except Exception:
                        pass

                time.sleep(self.cfg.signal_check_interval)

        except KeyboardInterrupt:
            logger.info("\nBot stopped by user.")
            if self.state.is_active:
                logger.info("Closing active grid...")
                price = self.bridge.get_price(f"{self.cfg.symbol}USDT") if self.bridge else 0
                self._close_all_grids(price, reason="manual_stop")
            send_alert(f"Grid bot stopped: {self.cfg.symbol}\n{self.risk.report()}")

    def _load_gem_params(self):
        """Load best GEM strategy parameters for this symbol from DB."""
        try:
            conn = connect()
            symbol_map = {"ETH": "ETHUSDT", "BTC": "BTCUSDT", "SOL": "SOLUSDT"}
            db_symbol = symbol_map.get(self.cfg.symbol, f"{self.cfg.symbol}USDT")

            row = conn.execute('''
                SELECT s.parameters FROM backtest_results br
                JOIN strategies s ON s.id = br.strategy_id
                WHERE br.symbol = ? AND br.status = 'GEM'
                ORDER BY br.composite_score DESC LIMIT 1
            ''', (db_symbol,)).fetchone()

            if row and row["parameters"]:
                params = json.loads(row["parameters"])
                self.cfg.ema_fast = int(params.get("ma_fast", self.cfg.ema_fast))
                self.cfg.ema_slow = int(params.get("ma_slow", self.cfg.ema_slow))
                self.cfg.rsi_period = int(params.get("rsi_period", self.cfg.rsi_period))
                self.cfg.rsi_overbought = int(params.get("rsi_overbought", self.cfg.rsi_overbought))
                self.cfg.rsi_oversold = int(params.get("rsi_oversold", self.cfg.rsi_oversold))
                self.cfg.bb_period = int(params.get("bb_period", self.cfg.bb_period))
                self.cfg.bb_std = float(params.get("bb_std", self.cfg.bb_std))
                logger.info(f"Loaded GEM params for {db_symbol}: {params}")
            else:
                logger.info(f"No GEM found for {db_symbol}, using defaults")

            conn.close()
        except Exception as e:
            logger.warning(f"Could not load GEM params: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GB-BRAIN Grid Bot for BloFin")
    parser.add_argument("--symbol", "-s", default="ETH", choices=["ETH", "BTC", "SOL"])
    parser.add_argument("--leverage", "-l", type=int, default=3, choices=[1, 2, 3, 5])
    parser.add_argument("--grids", "-g", type=int, default=10, help="Number of grid levels (5-30)")
    parser.add_argument("--spacing", type=float, default=0.5, help="Grid spacing in %% (0.3-2.0)")
    parser.add_argument("--tp", type=float, default=1.0, help="Take profit per grid in %% (0.5-5.0)")
    parser.add_argument("--sl", type=float, default=3.0, help="Stop loss in %% (1.0-10.0)")
    parser.add_argument("--timeframe", "-t", default="15m", choices=["1m", "5m", "15m", "1h"])
    parser.add_argument("--interval", type=int, default=60, help="Check interval in seconds")
    parser.add_argument("--paper", action="store_true", default=True)
    parser.add_argument("--live", action="store_true", help="LIVE trading (real money)")
    parser.add_argument("--config", action="store_true", help="Show config and exit")
    args = parser.parse_args()

    cfg = GridConfig(
        symbol=args.symbol,
        leverage=args.leverage,
        num_grids=max(5, min(30, args.grids)),
        grid_spacing_pct=max(0.003, min(0.02, args.spacing / 100)),
        take_profit_pct=max(0.005, min(0.05, args.tp / 100)),
        stop_loss_pct=max(0.01, min(0.10, args.sl / 100)),
        timeframe=args.timeframe,
        signal_check_interval=args.interval,
        use_demo=not args.live,
    )

    if args.config:
        print(f"\n{'=' * 50}")
        print(f"GB-BRAIN Grid Bot Configuration")
        print(f"{'=' * 50}")
        print(f"  Symbol:     {cfg.symbol}-USDT")
        print(f"  Leverage:   {cfg.leverage}x")
        print(f"  Grids:      {cfg.num_grids}")
        print(f"  Spacing:    {cfg.grid_spacing_pct*100:.1f}%")
        print(f"  TP/grid:    {cfg.take_profit_pct*100:.1f}%")
        print(f"  SL:         {cfg.stop_loss_pct*100:.1f}%")
        print(f"  Timeframe:  {cfg.timeframe}")
        print(f"  Mode:       {'DEMO' if cfg.use_demo else 'LIVE'}")
        print(f"  EMA:        {cfg.ema_fast}/{cfg.ema_slow}")
        print(f"  RSI:        {cfg.rsi_period} (OB:{cfg.rsi_overbought} OS:{cfg.rsi_oversold})")
        print(f"  BB:         {cfg.bb_period} std:{cfg.bb_std}")
        print(f"{'=' * 50}")
        sys.exit(0)

    bot = GridBot(cfg)
    bot.run()
