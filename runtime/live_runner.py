"""
GB-BRAIN — Live Runner (Phase 9)
==================================
Stage 1 micro live trading.
  - 0.5% risk per trade
  - 1 symbol only
  - 1 open position max
  - source='live' in live_trades (distinguishes from demo fills)

Built on the working demo_runner rewrite. Only differences:
  1. Uses CapitalAllocator to size positions (not hardcoded 1.0)
  2. source='live' tag in DB
  3. Checks CapitalAllocator.can_add_position() before every order
  4. Reads account balance from broker before each trade
  5. Requires kill_switch.json stage >= 1 to run

Usage:
    python runtime/live_runner.py --broker oanda --symbol US30 --tf 5m
    python runtime/live_runner.py --broker blofin --symbol ETH --tf 5m
    python runtime/live_runner.py --advance-stage  # advance from PAPER → MICRO
    python runtime/live_runner.py --status         # show allocator status
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

logger = logging.getLogger("gb_brain.live")

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
BLOFIN_SYMBOLS = {"ETH", "BTC", "SOL"}
OANDA_SYMBOLS  = {"NAS100", "US30", "SPX500"}
VALID_BROKERS  = {"blofin", "oanda"}
VALID_TFS      = {"1m", "3m", "5m", "15m", "30m", "1h", "4h"}

DB_PATH = ROOT / "db" / "gb_brain.db"


# ---------------------------------------------------------------------------
# Lazy imports — identical correct paths from working demo_runner
# ---------------------------------------------------------------------------

def _import_blofin_bridge():
    try:
        import execute.blofin_bridge as _bb
        class BloFinBridge:
            def get_latest_candle(self, symbol, timeframe):
                try:
                    price = _bb.get_ticker_price(symbol) if hasattr(_bb, 'get_ticker_price') else None
                except Exception:
                    price = None
                if price is None:
                    return None
                return {"open": price, "high": price, "low": price,
                        "close": price, "volume": 0}
            def get_account_balance(self):
                try:
                    return _bb.get_account_balance() if hasattr(_bb, 'get_account_balance') else None
                except Exception:
                    return None
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
            def get_account_balance(self):
                try:
                    return _ob.get_account_balance() if hasattr(_ob, 'get_account_balance') else None
                except Exception:
                    return None
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


def _import_capital_allocator():
    try:
        from runtime.capital_allocator import CapitalAllocator
        return CapitalAllocator
    except ImportError as exc:
        logger.warning("CapitalAllocator not found: %s", exc)
        return None


# ---------------------------------------------------------------------------
# LiveRunner
# ---------------------------------------------------------------------------
class LiveRunner:
    """
    Phase 9 live trading runner — Stage 1 MICRO only.

    Key differences from DemoRunner:
      - CapitalAllocator sizes every position (0.5% risk)
      - can_add_position() checked before every order
      - source='live' in live_trades
      - Reads account balance from broker before each trade
      - Refuses to run if kill_switch stage < 1

    Safety rules:
      - Max 1 open position (Stage 1 limit)
      - Max 1 symbol (Stage 1 limit)
      - Daily loss limit enforced by RiskManager
      - Kill switch checked every tick
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
        self._allocator   = None

        self._init_components()
        self._check_stage()
        self._ensure_schema()

        logger.info(
            "LiveRunner initialised — broker=%s symbol=%s tf=%s strategy=%s",
            self.broker, self.symbol, self.timeframe, self.strategy,
        )

    # ------------------------------------------------------------------
    # Initialisation
    # ------------------------------------------------------------------
    def _init_components(self):
        # Kill switch
        KS = _import_kill_switch()
        if KS:
            self._ks = KS()

        # Capital allocator — reads stage from kill_switch.json
        CA = _import_capital_allocator()
        if CA:
            self._allocator = CA()

        # Runtime policy
        RP = _import_runtime_policy()
        if RP:
            self._policy = RP()

        # Risk manager
        RM = _import_risk_manager()
        if RM:
            self._risk_mgr = RM()

        # Signal engine — CombinedEngine takes a preset dict
        CE = _import_engine()
        if CE:
            gems_path = ROOT / "config" / "gb_strategy_gems.json"
            try:
                gems   = json.loads(gems_path.read_text(encoding="utf-8"))
                preset = gems.get("combined", {}).get(self.symbol, {}).get("params", {})
            except Exception:
                preset = {}
            self._engine = CE(preset=preset) if preset else None
            if self._engine is None:
                logger.warning(
                    "No preset found for combined/%s — signal engine disabled", self.symbol
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

    def _check_stage(self):
        """Refuse to run if stage < 1 (PAPER mode — no real capital)."""
        if self._allocator is None:
            raise RuntimeError(
                "CapitalAllocator unavailable — cannot run live. "
                "Check runtime/capital_allocator.py exists."
            )
        status = self._allocator.get_status()
        stage  = status.get("stage", 0)
        if stage < 1:
            raise RuntimeError(
                f"Capital allocator is at Stage {stage} (PAPER) — "
                "advance to Stage 1 (MICRO) before running live.\n"
                "Run: python3 -m runtime.live_runner --advance-stage"
            )
        logger.info(
            "Stage check passed — stage=%d (%s) risk_pct=%.1f%%",
            stage, status.get("stage_name"), status.get("risk_pct"),
        )

    def _ensure_schema(self):
        """Ensure live_trades has all columns live_runner needs."""
        conn = sqlite3.connect(DB_PATH)
        try:
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
        logger.info(
            "Starting LIVE loop — %s %s %s", self.broker, self.symbol, self.timeframe
        )
        self._send_telegram(
            f"[LIVE START] {self.broker.upper()} {self.symbol} {self.timeframe} — "
            f"Stage 1 MICRO live runner started"
        )

        try:
            while True:
                try:
                    self._tick()
                except Exception as exc:
                    logger.exception("Tick error: %s", exc)
                    self._send_telegram(f"[LIVE ERROR] {self.symbol} tick error: {exc}")
                time.sleep(self.POLL_INTERVAL)

        except KeyboardInterrupt:
            logger.info("Live runner stopped by user.")
        finally:
            self._daily_summary()

    def _tick(self):
        # 1. Kill switch gate
        if self._ks and not self._ks.is_armed():
            state = self._ks.status().get("state", "UNKNOWN")
            logger.warning("Kill switch is %s — skipping tick", state)
            return

        # 2. Capital allocator gate — open positions count from DB
        open_count = self._count_open_positions()
        if self._allocator and not self._allocator.can_add_position(
            self.symbol, open_count
        ):
            logger.debug(
                "Allocator blocking new position — symbol=%s open=%d",
                self.symbol, open_count,
            )
            return

        # 3. Runtime policy gate
        if self._policy:
            lane   = self._policy.get_lane(self._lane_name, self.symbol, self.strategy)
            lane_ok = self._policy.can_trade(lane, 0)
            if not lane_ok:
                logger.debug(
                    "Lane %s/%s/%s disabled by policy — skipping",
                    self._lane_name, self.symbol, self.strategy,
                )
                return

        # 4. Fetch candle
        candle = self._fetch_candle()
        if candle is None:
            return

        # 5. Generate signal
        signal = self._generate_signal(candle)
        if signal is None or signal.get("action") == "HOLD":
            return

        # 6. Risk check
        if self._risk_mgr:
            allowed, reason = self._risk_mgr.can_trade()
            if not allowed:
                logger.info("Risk manager blocked trade: %s", reason)
                return

        # 7. Size the position using CapitalAllocator
        units = self._compute_units(signal)
        if units <= 0:
            logger.info("Computed units=0 — skipping order (balance or risk_pts issue)")
            return
        signal["units"] = units

        # 8. Place live order
        order_result = self._place_live_order(signal)
        if order_result is None:
            return

        # 9. Log fill with source='live'
        self._log_fill(order_result, signal)

        # 10. Check daily loss after fill
        if self._risk_mgr and self._risk_mgr.state.is_halted:
            logger.warning("Daily loss limit hit — halting live runner")
            self._send_telegram(f"[LIVE HALT] {self.symbol} daily loss limit reached")
            raise KeyboardInterrupt

    def _count_open_positions(self) -> int:
        """Count live positions open today from live_trades."""
        conn = sqlite3.connect(DB_PATH)
        try:
            today = date.today().isoformat()
            row = conn.execute(
                """
                SELECT COUNT(*) FROM live_trades
                WHERE source = 'live'
                  AND broker = ?
                  AND symbol = ?
                  AND run_at >= ?
                  AND status NOT IN ('closed', 'filled', 'cancelled')
                """,
                (self.broker, self.symbol, today),
            ).fetchone()
            return row[0] if row else 0
        except Exception:
            return 0
        finally:
            conn.close()

    def _compute_units(self, signal: dict) -> float:
        """
        Use CapitalAllocator to size the position.
        Returns 0.0 if sizing fails or balance unavailable.
        """
        if self._allocator is None:
            return 1.0  # fallback — should not reach here after _check_stage

        # Get account balance from broker
        balance = None
        if self._bridge and hasattr(self._bridge, "get_account_balance"):
            try:
                balance = self._bridge.get_account_balance()
                if isinstance(balance, dict):
                    # OANDA returns a dict; extract NAV
                    balance = float(
                        balance.get("NAV")
                        or balance.get("balance")
                        or balance.get("nav")
                        or 0
                    )
                else:
                    balance = float(balance) if balance else None
            except Exception as exc:
                logger.warning("Could not fetch account balance: %s", exc)
                balance = None

        if not balance or balance <= 0:
            logger.warning("Account balance unavailable — cannot size position")
            return 0.0

        entry_price = signal.get("entry_price", 0)
        stop_loss   = signal.get("stop_loss",   0)
        risk_pts    = abs(entry_price - stop_loss) if entry_price and stop_loss else 0

        if risk_pts <= 0:
            # Fallback: use 0.5% of entry as risk distance
            risk_pts = entry_price * 0.005 if entry_price else 0

        if risk_pts <= 0:
            logger.warning("Cannot compute risk_pts — entry=%.5f sl=%.5f", entry_price, stop_loss)
            return 0.0

        units = self._allocator.get_position_size(
            symbol=self.symbol,
            balance=balance,
            risk_pts=risk_pts,
            entry_price=entry_price,
        )

        logger.info(
            "Position sized — %s balance=%.2f risk_pts=%.4f entry=%.5f → %.6f units",
            self.symbol, balance, risk_pts, entry_price, units,
        )
        return units

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
    def _place_live_order(self, signal: dict):
        if self._bridge is None:
            logger.warning("No bridge configured — cannot place live order")
            return None

        side  = signal.get("side", signal.get("action", "BUY")).upper()
        units = signal.get("units", 1.0)
        price = signal.get("entry_price", signal.get("price"))

        logger.info(
            "[LIVE ORDER] %s %s %s @ %s (broker=%s)",
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
            logger.error("Live order placement failed: %s", exc)
            self._send_telegram(f"[LIVE ORDER FAIL] {self.symbol} {side} error: {exc}")
            return None

    # ------------------------------------------------------------------
    # Fill logging — source='live'
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
        units    = signal.get("units", 1.0)
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
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'live', ?, ?)
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
            "[LIVE FILL] %s %s @ %.5f (signal=%.5f slip=%.4f%% units=%.6f)",
            side, self.symbol,
            fill_price or 0, signal_price or 0, slippage_pct or 0, units,
        )
        self._send_telegram(
            f"[LIVE FILL] {self.broker.upper()} {side} {units:.6f} {self.symbol}\n"
            f"Signal: {signal_price}  Fill: {fill_price}  Slip: {slippage_pct:.4f}%"
        )

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
                WHERE  source = 'live'
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
            summary = f"[LIVE SUMMARY] {self.symbol} — no fills today"
            logger.info(summary)
            self._send_telegram(summary)
            return

        avg_slip = sum(r[5] for r in rows if r[5] is not None) / total_fills
        max_slip = max((r[5] or 0) for r in rows)
        buys  = sum(1 for r in rows if r[0] == "BUY")
        sells = total_fills - buys

        summary = (
            f"[LIVE DAILY SUMMARY] {self.broker.upper()} {self.symbol}\n"
            f"  Date      : {today}\n"
            f"  Fills     : {total_fills}  (BUY={buys} SELL={sells})\n"
            f"  Avg Slip  : {avg_slip:.4f}%\n"
            f"  Max Slip  : {max_slip:.4f}%\n"
        )
        logger.info(summary)
        print(summary)
        self._send_telegram(summary)

    def _send_telegram(self, message: str):
        if self._send_alert:
            try:
                self._send_alert(message)
            except Exception as exc:
                logger.warning("Telegram send failed: %s", exc)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="GB-BRAIN Live Runner (Phase 9) — Stage 1 MICRO live trading",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--broker",  choices=list(VALID_BROKERS), help="Broker to use")
    p.add_argument("--symbol",  help="Trading symbol, e.g. ETH, US30")
    p.add_argument("--tf",      default="5m", choices=list(VALID_TFS), help="Candle timeframe")
    p.add_argument("--strategy", default="combined", help="Strategy name (default: combined)")
    p.add_argument(
        "--advance-stage",
        action="store_true",
        help="Advance CapitalAllocator from PAPER (0) to MICRO (1) then exit",
    )
    p.add_argument(
        "--status",
        action="store_true",
        help="Print CapitalAllocator status and exit",
    )
    p.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
    )
    return p


def main():
    args = _build_parser().parse_args()

    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # --status: just print allocator state
    if args.status:
        CA = _import_capital_allocator()
        if CA:
            CA().print_status()
        else:
            print("CapitalAllocator not available")
        return

    # --advance-stage: promote PAPER → MICRO
    if args.advance_stage:
        CA = _import_capital_allocator()
        if not CA:
            print("ERROR: CapitalAllocator not available")
            sys.exit(1)
        allocator = CA()
        status    = allocator.get_status()
        if status["stage"] >= 1:
            print(f"Already at Stage {status['stage']} ({status['stage_name']}) — no change needed")
            allocator.print_status()
            return
        new_stage = allocator.advance_stage(reason="Phase 9 live rollout — manual advance")
        print(f"Advanced to Stage {int(new_stage)}: {new_stage.name}")
        allocator.print_status()
        return

    if not args.broker or not args.symbol:
        _build_parser().error("--broker and --symbol are required to run the live loop")

    runner = LiveRunner(
        broker=args.broker,
        symbol=args.symbol,
        timeframe=args.tf,
        strategy=args.strategy,
    )
    runner.run()


if __name__ == "__main__":
    main()
