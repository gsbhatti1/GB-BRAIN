"""
GB-BRAIN — Demo Runner (Phase 6)
==================================
Runs real demo/practice accounts:
  BloFin demo for crypto (ETH, BTC, SOL)
  OANDA practice for indices (NAS100, US30, SPX500)

Wraps live_observer + paper_executor but routes orders to real demo brokers.
Tracks fills, slippage, and execution quality.

Usage:
    python runtime/demo_runner.py --broker blofin --symbol ETH --tf 5m
    python runtime/demo_runner.py --broker oanda --symbol US30 --tf 5m
    python runtime/demo_runner.py --list-demo-accounts
"""

import argparse
import json
import logging
import sqlite3
import sys
import time
from datetime import datetime, date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv
load_dotenv(ROOT / ".env")

logger = logging.getLogger("gb_brain.demo")

# ---------------------------------------------------------------------------
# Broker routing constants
# ---------------------------------------------------------------------------
BLOFIN_SYMBOLS = {"ETH", "BTC", "SOL"}
OANDA_SYMBOLS  = {"NAS100", "US30", "SPX500"}
VALID_BROKERS  = {"blofin", "oanda"}
VALID_TFS      = {"1m", "3m", "5m", "15m", "30m", "1h", "4h"}

DB_PATH = ROOT / "db" / "gb_brain.db"


# ---------------------------------------------------------------------------
# Lazy imports — all with correct GB-BRAIN module paths
# ---------------------------------------------------------------------------

def _import_blofin_bridge():
    try:
        import execute.blofin_bridge as _bb
        # blofin_bridge is module-level functions — wrap in adapter
        class BloFinBridge:
            def get_latest_candle(self, symbol, timeframe):
                # blofin_bridge has get_price or similar
                try:
                    price = _bb.get_ticker_price(symbol) if hasattr(_bb, 'get_ticker_price') else None
                except Exception:
                    price = None
                if price is None:
                    return None
                return {"open": price, "high": price, "low": price,
                        "close": price, "volume": 0}
            def place_order(self, symbol=None, side="BUY", size=1.0, order_type="market", **kw):
                try:
                    return _bb.place_order(symbol, size if side == "BUY" else -abs(size))
                except Exception as exc:
                    logger.error("BloFin order error: %s", exc)
                    return None
        return BloFinBridge
    except ImportError as exc:
        logger.warning("BloFinBridge not found: %s", exc)
        return None


def _import_oanda_bridge():
    try:
        import execute.oanda_bridge as _ob
        # oanda_bridge is module-level functions — wrap in adapter
        class OandaBridge:
            def get_latest_candle(self, symbol, timeframe):
                try:
                    price = _ob.get_price(symbol)
                except Exception:
                    price = None
                if price is None:
                    return None
                return {"open": price, "high": price, "low": price,
                        "close": price, "volume": 0}
            def place_order(self, instrument=None, units=1, order_type="MARKET",
                            symbol=None, side="BUY", size=1.0, **kw):
                sym = instrument or symbol or ""
                u   = units if units != 1 else (size if side == "BUY" else -abs(size))
                try:
                    return _ob.place_order(sym, u)
                except Exception as exc:
                    logger.error("OANDA order error: %s", exc)
                    return None
        return OandaBridge
    except ImportError as exc:
        logger.warning("OandaBridge not found: %s", exc)
        return None


def _import_engine():
    try:
        from strategies.custom.combined_engine import CombinedEngine
        return CombinedEngine
    except ImportError as exc:
        logger.warning("CombinedEngine not found: %s", exc)
        return None


def _import_risk_manager():
    try:
        from execute.risk_manager import RiskManager
        return RiskManager
    except ImportError as exc:
        logger.warning("RiskManager not found: %s", exc)
        return None


def _import_runtime_policy():
    try:
        from runtime.runtime_policy import RuntimePolicy
        return RuntimePolicy
    except ImportError as exc:
        logger.warning("RuntimePolicy not found: %s", exc)
        return None


def _import_telegram():
    try:
        from execute.telegram_alerts import send_alert
        return send_alert
    except ImportError as exc:
        logger.warning("Telegram alert not found: %s", exc)
        return None


def _import_kill_switch():
    try:
        from runtime.kill_switch import KillSwitch
        return KillSwitch
    except ImportError as exc:
        logger.warning("KillSwitch not found: %s", exc)
        return None


# ---------------------------------------------------------------------------
# DemoRunner
# ---------------------------------------------------------------------------
class DemoRunner:
    """
    Orchestrates demo/practice trading for a single broker + symbol + timeframe.

    Routing:
      - blofin  → BloFinBridge (demo mode)
      - oanda   → OandaBridge  (practice environment)

    Every fill is persisted in live_trades with source='demo' so fill_tracker
    and slippage_check can analyse execution quality.
    """

    POLL_INTERVAL = 10  # seconds between candle polls

    def __init__(
        self,
        broker: str,
        symbol: str,
        timeframe: str = "5m",
        strategy: str = "combined",
    ):
        broker = broker.lower()
        if broker not in VALID_BROKERS:
            raise ValueError(f"broker must be one of {VALID_BROKERS}, got '{broker}'")
        if timeframe not in VALID_TFS:
            raise ValueError(f"timeframe must be one of {VALID_TFS}, got '{timeframe}'")

        self.broker    = broker
        self.symbol    = symbol.upper()
        self.timeframe = timeframe
        self.strategy  = strategy

        # Derive lane name from broker
        self._lane_name = "GB-INDICES" if broker == "oanda" else "GB-CRYPTO-BOT"

        self._engine      = None
        self._risk_mgr    = None
        self._policy      = None
        self._bridge      = None
        self._send_alert  = _import_telegram()
        self._ks          = None

        self._init_components()
        self._ensure_schema()

        logger.info(
            "DemoRunner initialised — broker=%s symbol=%s tf=%s strategy=%s",
            self.broker, self.symbol, self.timeframe, self.strategy,
        )

    # ------------------------------------------------------------------
    # Initialisation helpers
    # ------------------------------------------------------------------
    def _init_components(self):
        # Kill switch
        KS = _import_kill_switch()
        if KS:
            self._ks = KS()

        # Runtime policy
        RP = _import_runtime_policy()
        if RP:
            self._policy = RP()

        # Risk manager
        RM = _import_risk_manager()
        if RM:
            self._risk_mgr = RM()

        # Signal engine — CombinedEngine takes a preset dict
        # gb_strategy_gems.json v2.0: keyed by symbol -> list of GEM dicts
        CE = _import_engine()
        if CE:
            gems_path = ROOT / "config" / "gb_strategy_gems.json"
            preset = {}
            self._active_gem = None
            try:
                gems = json.loads(gems_path.read_text(encoding="utf-8"))
                sym_gems = gems.get(self.symbol, [])
                # Pick best deploy_ready GEM (first = highest composite_score)
                for g in sym_gems:
                    if g.get("deploy_ready", False):
                        preset = g.get("parameters", {})
                        self._active_gem = g.get("name", "unknown")
                        break
            except Exception as exc:
                logger.warning("Failed to load gems config: %s", exc)
            self._engine = CE(preset=preset) if preset else None
            if self._engine is None:
                logger.warning(
                    "No deploy-ready GEM found for %s — signal engine disabled", self.symbol
                )
            else:
                logger.info(
                    "Loaded GEM preset for %s: %s (params=%s)",
                    self.symbol, self._active_gem, list(preset.keys())
                )

        # Broker bridge
        if self.broker == "blofin":
            BF = _import_blofin_bridge()
            if BF:
                self._bridge = BF()
        else:
            OA = _import_oanda_bridge()
            if OA:
                self._bridge = OA()

    def _ensure_schema(self):
        """Ensure live_trades has all columns demo_runner needs."""
        conn = sqlite3.connect(DB_PATH)
        try:
            # Add any missing columns (ALTER TABLE is safe on existing columns)
            existing = {r[1] for r in conn.execute("PRAGMA table_info(live_trades);")}
            needed = [
                ("signal_price", "REAL"),
                ("fill_price",   "REAL"),
                ("slippage_pts", "REAL"),
                ("slippage_pct", "REAL"),
                ("source",       "TEXT"),
                ("run_at",       "TEXT"),
                ("order_id",     "TEXT"),
                ("units",        "REAL"),
                ("raw_signal",   "TEXT"),
                ("raw_result",   "TEXT"),
            ]
            for col, typ in needed:
                if col not in existing:
                    conn.execute(f"ALTER TABLE live_trades ADD COLUMN {col} {typ};")
                    logger.debug("Added column live_trades.%s", col)
            conn.commit()
        finally:
            conn.close()

    # ------------------------------------------------------------------
    # Main loop
    # ------------------------------------------------------------------
    def run(self):
        logger.info("Starting demo loop — %s %s %s", self.broker, self.symbol, self.timeframe)
        self._send_telegram(
            f"[DEMO START] {self.broker.upper()} {self.symbol} {self.timeframe} — demo runner started"
        )

        try:
            while True:
                try:
                    self._tick()
                except Exception as exc:
                    logger.exception("Tick error: %s", exc)
                    self._send_telegram(f"[DEMO ERROR] {self.symbol} tick error: {exc}")
                time.sleep(self.POLL_INTERVAL)

        except KeyboardInterrupt:
            logger.info("Demo runner stopped by user.")
        finally:
            self._daily_summary()

    def _tick(self):
        # 1. Kill switch gate
        if self._ks and not self._ks.is_armed():
            state = self._ks.status().get("state", "UNKNOWN")
            logger.warning("Kill switch is %s — skipping tick", state)
            return

        # 2. Runtime policy gate — can_trade(lane, trades_today)
        if self._policy:
            lane = self._policy.get_lane(self._lane_name, self.symbol, self.strategy)
            lane_ok = self._policy.can_trade(lane, 0)
            if not lane_ok:
                logger.debug(
                    "Lane %s/%s/%s disabled by policy — skipping",
                    self._lane_name, self.symbol, self.strategy,
                )
                return

        # 3. Fetch candle
        candle = self._fetch_candle()
        if candle is None:
            return

        # 4. Generate signal
        signal = self._generate_signal(candle)
        if signal is None or signal.get("action") == "HOLD":
            return

        # 5. Risk check — can_trade() returns (bool, reason_str)
        if self._risk_mgr:
            allowed, reason = self._risk_mgr.can_trade()
            if not allowed:
                logger.info("Risk manager blocked trade: %s", reason)
                return

        # 6. Place demo order
        order_result = self._place_demo_order(signal)
        if order_result is None:
            return

        # 7. Log fill
        self._log_fill(order_result, signal)

        # 8. Check daily loss after fill — use RiskManager state
        if self._risk_mgr and self._risk_mgr.state.is_halted:
            logger.warning("Daily loss limit hit — halting demo runner")
            self._send_telegram(f"[DEMO HALT] {self.symbol} daily loss limit reached")
            raise KeyboardInterrupt

    def _fetch_candle(self):
        if self._bridge is None:
            logger.debug("No bridge available — cannot fetch candle")
            return None
        try:
            return self._bridge.get_latest_candle(self.symbol, self.timeframe)
        except Exception as exc:
            logger.error("Candle fetch error: %s", exc)
            return None

    def _generate_signal(self, candle):
        if self._engine is None:
            return None
        try:
            import pandas as pd
            # CombinedEngine.run() takes a DataFrame
            if isinstance(candle, dict):
                df = pd.DataFrame([candle])
                for col in ("open", "high", "low", "close", "volume"):
                    if col in df.columns:
                        df[col] = pd.to_numeric(df[col], errors="coerce")
            else:
                df = candle
            results = self._engine.run(df)
            if not results:
                return {"action": "HOLD"}
            sig = results[-1]
            direction = getattr(sig, "direction", 0)
            return {
                "action":      "BUY" if direction == 1 else ("SELL" if direction == -1 else "HOLD"),
                "direction":   direction,
                "entry_price": getattr(sig, "entry_price", 0),
                "stop_loss":   getattr(sig, "stop_loss",   0),
                "tp1":         getattr(sig, "tp1",         0),
                "tp3":         getattr(sig, "tp3",         0),
                "score":       getattr(sig, "score",       0),
            }
        except Exception as exc:
            logger.error("Signal engine error: %s", exc)
            return None

    # ------------------------------------------------------------------
    # Order placement
    # ------------------------------------------------------------------
    def _place_demo_order(self, signal: dict):
        if self._bridge is None:
            logger.warning("No bridge configured — cannot place demo order")
            return None

        side  = signal.get("side", signal.get("action", "BUY")).upper()
        units = signal.get("units", signal.get("size", 1.0))
        price = signal.get("entry_price", signal.get("price"))

        logger.info(
            "[DEMO ORDER] %s %s %s @ %s (broker=%s)",
            side, units, self.symbol, price, self.broker,
        )

        try:
            if self.broker == "blofin":
                result = self._bridge.place_order(
                    symbol=self.symbol,
                    side=side,
                    size=units,
                    order_type="market",
                )
            else:  # oanda
                result = self._bridge.place_order(
                    instrument=self.symbol,
                    units=units if side == "BUY" else -abs(units),
                )
            return result
        except Exception as exc:
            logger.error("Demo order placement failed: %s", exc)
            self._send_telegram(f"[DEMO ORDER FAIL] {self.symbol} {side} error: {exc}")
            return None

    # ------------------------------------------------------------------
    # Fill logging
    # ------------------------------------------------------------------
    def _log_fill(self, order_result: dict, signal: dict):
        if order_result is None:
            return

        signal_price = signal.get("entry_price", signal.get("price"))
        fill_price   = (
            order_result.get("fill_price")
            or order_result.get("avgPx")
            or order_result.get("price")
        )
        side     = signal.get("side", signal.get("action", "BUY")).upper()
        units    = signal.get("units", signal.get("size", 1.0))
        order_id = (
            order_result.get("ordId")
            or order_result.get("id")
            or order_result.get("orderID")
        )
        status   = order_result.get("state") or order_result.get("status") or "filled"

        slippage_pts, slippage_pct = self._compute_slippage(signal_price, fill_price)

        conn = sqlite3.connect(DB_PATH)
        try:
            conn.execute(
                """
                INSERT INTO live_trades
                  (run_at, broker, symbol, timeframe, strategy, side,
                   signal_price, fill_price, units,
                   slippage_pts, slippage_pct,
                   order_id, status, source, raw_signal, raw_result)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'demo', ?, ?)
                """,
                (
                    datetime.utcnow().isoformat(),
                    self.broker,
                    self.symbol,
                    self.timeframe,
                    self.strategy,
                    side,
                    signal_price,
                    fill_price,
                    units,
                    slippage_pts,
                    slippage_pct,
                    str(order_id),
                    status,
                    json.dumps(signal),
                    json.dumps(order_result),
                ),
            )
            conn.commit()
        finally:
            conn.close()

        logger.info(
            "[FILL] %s %s @ %.5f (signal=%.5f slip=%.4f%%)",
            side, self.symbol,
            fill_price or 0, signal_price or 0, slippage_pct or 0,
        )
        self._send_telegram(
            f"[DEMO FILL] {self.broker.upper()} {side} {units} {self.symbol}\n"
            f"Signal: {signal_price}  Fill: {fill_price}  Slip: {slippage_pct:.4f}%"
        )

    # ------------------------------------------------------------------
    # Slippage
    # ------------------------------------------------------------------
    def _compute_slippage(self, signal_price, fill_price):
        if signal_price is None or fill_price is None:
            return 0.0, 0.0
        try:
            sp = float(signal_price)
            fp = float(fill_price)
            if sp == 0:
                return 0.0, 0.0
            pts = abs(fp - sp)
            pct = pts / sp * 100
            return round(pts, 6), round(pct, 6)
        except (TypeError, ValueError):
            return 0.0, 0.0

    # ------------------------------------------------------------------
    # Daily summary
    # ------------------------------------------------------------------
    def _daily_summary(self):
        today = date.today().isoformat()
        conn  = sqlite3.connect(DB_PATH)
        try:
            rows = conn.execute(
                """
                SELECT side, signal_price, fill_price, units, slippage_pts, slippage_pct
                FROM   live_trades
                WHERE  source = 'demo'
                  AND  broker = ?
                  AND  symbol = ?
                  AND  run_at >= ?
                """,
                (self.broker, self.symbol, today),
            ).fetchall()
        finally:
            conn.close()

        total_fills = len(rows)
        if total_fills == 0:
            summary = f"[DEMO SUMMARY] {self.symbol} — no fills today"
            logger.info(summary)
            self._send_telegram(summary)
            return

        avg_slip = sum(r[5] for r in rows if r[5] is not None) / total_fills
        max_slip = max((r[5] or 0) for r in rows)
        buys  = sum(1 for r in rows if r[0] == "BUY")
        sells = total_fills - buys

        summary = (
            f"[DEMO DAILY SUMMARY] {self.broker.upper()} {self.symbol}\n"
            f"  Date      : {today}\n"
            f"  Fills     : {total_fills}  (BUY={buys} SELL={sells})\n"
            f"  Avg Slip  : {avg_slip:.4f}%\n"
            f"  Max Slip  : {max_slip:.4f}%\n"
        )
        logger.info(summary)
        print(summary)
        self._send_telegram(summary)

    # ------------------------------------------------------------------
    # Telegram helper
    # ------------------------------------------------------------------
    def _send_telegram(self, message: str):
        if self._send_alert:
            try:
                self._send_alert(message)
            except Exception as exc:
                logger.warning("Telegram send failed: %s", exc)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def list_demo_accounts():
    print("=== Demo / Practice Accounts ===")
    print(f"  BloFin demo    — symbols: {sorted(BLOFIN_SYMBOLS)}")
    print(f"  OANDA practice — symbols: {sorted(OANDA_SYMBOLS)}")


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="GB-BRAIN Demo Runner — executes on real demo/practice broker accounts",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--broker",   choices=list(VALID_BROKERS), help="Broker to use")
    p.add_argument("--symbol",   help="Trading symbol, e.g. ETH, US30")
    p.add_argument("--tf",       default="5m", choices=list(VALID_TFS), help="Candle timeframe")
    p.add_argument("--strategy", default="combined", help="Strategy name (default: combined)")
    p.add_argument("--list-demo-accounts", action="store_true",
                   help="Print demo account info and exit")
    p.add_argument("--log-level", default="INFO",
                   choices=["DEBUG", "INFO", "WARNING", "ERROR"],
                   help="Logging level")
    return p


def main():
    parser = _build_parser()
    args   = parser.parse_args()

    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    if args.list_demo_accounts:
        list_demo_accounts()
        return

    if not args.broker or not args.symbol:
        parser.error("--broker and --symbol are required")

    runner = DemoRunner(
        broker=args.broker,
        symbol=args.symbol,
        timeframe=args.tf,
        strategy=args.strategy,
    )
    runner.run()


if __name__ == "__main__":
    main()
