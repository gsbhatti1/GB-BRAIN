"""
GB-BRAIN — Live Observer
==========================
Polls live market data, runs signal engines, logs signals to SQLite.
Does NOT place trades — only observes and records.
Designed to run as a background process.

Modes:
  paper   → Log signals only, no order placement
  demo    → Log signals + route to paper executor
  live    → Log signals + route to live broker (Phase 9 only)

Usage:
    python runtime/live_observer.py --mode paper --lane GB-INDICES
    python runtime/live_observer.py --mode paper --lane GB-CRYPTO-BOT
    python runtime/live_observer.py --mode paper --lane MANUAL-SIGNALS

Conventions:
    - SQLite is truth — all signals persisted in observed_signals table
    - Capital is priority — observer never places orders
    - .env for secrets — API credentials loaded from environment
    - Deterministic — same candle data + preset = same signal
"""

from __future__ import annotations

import argparse
import logging
import os
import signal
import sqlite3
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import pandas as pd

from runtime.runtime_policy import RuntimePolicy, Lane

# ---------------------------------------------------------------------------
# ROOT path (project root = two levels up from this file)
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Logger
# ---------------------------------------------------------------------------
logger = logging.getLogger("gb_brain.observer")

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
POLL_INTERVAL_SECONDS = 60
HEARTBEAT_INTERVAL_SECONDS = 300   # 5 minutes

# NY session window (UTC): 13:30–21:00
NY_SESSION_START_UTC = (13, 30)
NY_SESSION_END_UTC   = (21, 0)

# Crypto symbols — fetched via python-binance
CRYPTO_SYMBOLS = {"BTC", "ETH", "SOL"}

# Index symbols — fetched via yfinance; maps GB-BRAIN name → yfinance ticker
INDEX_SYMBOL_MAP: dict[str, str] = {
    "US30":   "YM=F",
    "NAS100": "NQ=F",
    "SPX500": "ES=F",
    "SPY":    "SPY",
    "QQQ":    "QQQ",
    "DIA":    "DIA",
}

# BinanceUS spot symbol mapping: GB-BRAIN symbol → Binance pair
CRYPTO_SYMBOL_MAP: dict[str, str] = {
    "BTC": "BTCUSDT",
    "ETH": "ETHUSDT",
    "SOL": "SOLUSDT",
}

# observed_signals CREATE TABLE SQL
_CREATE_OBSERVED_SIGNALS = """
CREATE TABLE IF NOT EXISTS observed_signals (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    lane_name     TEXT,
    symbol        TEXT,
    strategy      TEXT,
    timeframe     TEXT,
    direction     INTEGER,
    entry_price   REAL,
    stop_loss     REAL,
    tp1           REAL,
    tp3           REAL,
    score         REAL,
    reason        TEXT,
    session       TEXT,
    observed_at   TEXT DEFAULT (datetime('now')),
    mode          TEXT DEFAULT 'paper'
);
"""


# ---------------------------------------------------------------------------
# LiveObserver
# ---------------------------------------------------------------------------

class LiveObserver:
    """
    Background process that polls market data, evaluates signal engines,
    and persists signals to SQLite without placing any orders.

    Parameters
    ----------
    mode      : str  One of "paper", "demo", "live". Default "paper".
    lane_name : str  Name of the lane group to observe (e.g. "GB-INDICES").
    dry_run   : bool If True, skips DB writes and broker routing.
    """

    def __init__(
        self,
        mode: str = "paper",
        lane_name: str = "GB-INDICES",
        dry_run: bool = False,
    ) -> None:
        self.mode = mode.lower()
        self.lane_name = lane_name
        self.dry_run = dry_run
        self._running = False
        self._last_heartbeat: float = 0.0
        self._policy = RuntimePolicy()
        self._db_path = ROOT / "db" / "gb_brain.db"
        self._log_path = ROOT / "logs" / "observer.log"

        # Ensure directories exist
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        self._log_path.parent.mkdir(parents=True, exist_ok=True)

        # Register UNIX signal handlers for graceful shutdown
        signal.signal(signal.SIGINT,  self._handle_shutdown)
        signal.signal(signal.SIGTERM, self._handle_shutdown)

        # Ensure observed_signals table exists
        if not self.dry_run:
            self._ensure_table()

        logger.info(
            "LiveObserver init | mode=%s lane=%s dry_run=%s db=%s",
            self.mode, self.lane_name, self.dry_run, self._db_path,
        )

    # ------------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------------

    def run(self) -> None:
        """
        Main polling loop.  Runs until SIGINT / SIGTERM or internal error.

        Cycle:
          1. Heartbeat ping every 5 minutes
          2. For each enabled lane in lane_name:
             a. Fetch candles
             b. Run signal engines
             c. Log any signals to SQLite
          3. Sleep POLL_INTERVAL_SECONDS
        """
        self._running = True
        lanes = [
            l for l in self._policy.enabled_lanes()
            if l.lane_name == self.lane_name
        ]
        if not lanes:
            logger.warning("No enabled lanes found for '%s' — observer idle.", self.lane_name)

        logger.info(
            "Observer started | %d active lanes | poll=%ds",
            len(lanes), POLL_INTERVAL_SECONDS,
        )

        while self._running:
            cycle_start = time.monotonic()
            self._heartbeat()

            for lane in lanes:
                try:
                    self._process_lane(lane)
                except Exception as exc:  # noqa: BLE001
                    logger.exception(
                        "Unhandled error processing lane %s: %s", lane.key, exc
                    )

            elapsed = time.monotonic() - cycle_start
            sleep_for = max(0.0, POLL_INTERVAL_SECONDS - elapsed)
            logger.debug("Cycle complete in %.1fs — sleeping %.1fs.", elapsed, sleep_for)
            if self._running:
                time.sleep(sleep_for)

        logger.info("Observer stopped cleanly.")

    # ------------------------------------------------------------------
    # Per-lane processing
    # ------------------------------------------------------------------

    def _process_lane(self, lane: Lane) -> None:
        """Fetch candles and evaluate engines for a single lane."""
        if not self._should_run_now(lane):
            logger.debug("Lane %s outside session window — skipping.", lane.key)
            return

        symbol   = lane.symbol
        strategy = lane.strategy

        # Determine timeframe from strategy name
        timeframe = "5Min" if strategy == "parallax" else "15Min"

        df = self._fetch_candles(symbol, timeframe)
        if df is None or df.empty:
            logger.warning("No candle data for %s [%s] — skipping.", symbol, timeframe)
            return

        signals = self._run_engines(symbol, df, strategy)
        if not signals:
            logger.debug("No signal from %s on %s [%s].", strategy, symbol, timeframe)
            return

        for sig in signals:
            self._log_signal(sig, symbol, strategy, timeframe, lane)

    # ------------------------------------------------------------------
    # Data fetching
    # ------------------------------------------------------------------

    def _fetch_candles(
        self,
        symbol: str,
        timeframe: str,
        n_bars: int = 100,
    ) -> Optional[pd.DataFrame]:
        """
        Retrieve recent OHLCV candles for a symbol.

        Uses yfinance for index symbols and python-binance for crypto.

        Parameters
        ----------
        symbol    : str  GB-BRAIN symbol (e.g. "NAS100", "BTC")
        timeframe : str  Bar timeframe (e.g. "5Min", "15Min")
        n_bars    : int  Number of bars to retrieve. Default 100.

        Returns
        -------
        pd.DataFrame with columns: open, high, low, close, volume
        Index: DatetimeIndex (UTC)
        """
        if symbol.upper() in CRYPTO_SYMBOLS:
            return self._fetch_crypto_candles(symbol, timeframe, n_bars)
        else:
            return self._fetch_index_candles(symbol, timeframe, n_bars)

    def _fetch_index_candles(
        self,
        symbol: str,
        timeframe: str,
        n_bars: int,
    ) -> Optional[pd.DataFrame]:
        """Fetch index candles via yfinance."""
        try:
            import yfinance as yf  # type: ignore

            ticker = INDEX_SYMBOL_MAP.get(symbol.upper(), symbol.upper())
            # yfinance interval strings
            tf_map = {
                "1Min": "1m", "5Min": "5m", "15Min": "15m",
                "1H": "1h", "1Hour": "1h", "1D": "1d",
            }
            interval = tf_map.get(timeframe, "5m")
            # Fetch enough history: n_bars * interval in days
            period_days = max(2, (n_bars * int(timeframe.rstrip("Min").rstrip("H")) // 390) + 1)
            period = f"{period_days}d"

            df = yf.download(
                ticker,
                period=period,
                interval=interval,
                progress=False,
                auto_adjust=True,
            )
            if df is None or df.empty:
                logger.warning("yfinance returned empty for %s [%s].", ticker, interval)
                return None

            df.columns = [c.lower() for c in df.columns]
            df = df[["open", "high", "low", "close", "volume"]].dropna()
            return df.tail(n_bars)

        except ImportError:
            logger.error("yfinance not installed — cannot fetch index candles.")
            return None
        except Exception as exc:  # noqa: BLE001
            logger.exception("Error fetching index candles for %s: %s", symbol, exc)
            return None

    def _fetch_crypto_candles(
        self,
        symbol: str,
        timeframe: str,
        n_bars: int,
    ) -> Optional[pd.DataFrame]:
        """Fetch crypto candles via python-binance (Binance.US or global)."""
        try:
            from binance.client import Client  # type: ignore

            pair = CRYPTO_SYMBOL_MAP.get(symbol.upper(), f"{symbol.upper()}USDT")
            tf_map = {
                "1Min": Client.KLINE_INTERVAL_1MINUTE,
                "5Min": Client.KLINE_INTERVAL_5MINUTE,
                "15Min": Client.KLINE_INTERVAL_15MINUTE,
                "1H": Client.KLINE_INTERVAL_1HOUR,
                "1Hour": Client.KLINE_INTERVAL_1HOUR,
                "1D": Client.KLINE_INTERVAL_1DAY,
            }
            interval = tf_map.get(timeframe, Client.KLINE_INTERVAL_5MINUTE)

            api_key    = os.getenv("BINANCE_API_KEY", "")
            api_secret = os.getenv("BINANCE_API_SECRET", "")
            client = Client(api_key, api_secret)

            raw = client.get_klines(symbol=pair, interval=interval, limit=n_bars)
            if not raw:
                logger.warning("Binance returned empty for %s [%s].", pair, interval)
                return None

            df = pd.DataFrame(raw, columns=[
                "open_time", "open", "high", "low", "close", "volume",
                "close_time", "quote_vol", "trades", "taker_base_vol",
                "taker_quote_vol", "ignore",
            ])
            df["open_time"] = pd.to_datetime(df["open_time"], unit="ms", utc=True)
            df.set_index("open_time", inplace=True)
            for col in ("open", "high", "low", "close", "volume"):
                df[col] = df[col].astype(float)
            return df[["open", "high", "low", "close", "volume"]]

        except ImportError:
            logger.error("python-binance not installed — cannot fetch crypto candles.")
            return None
        except Exception as exc:  # noqa: BLE001
            logger.exception("Error fetching crypto candles for %s: %s", symbol, exc)
            return None

    # ------------------------------------------------------------------
    # Signal engines
    # ------------------------------------------------------------------

    def _run_engines(
        self,
        symbol: str,
        df: pd.DataFrame,
        preset: str,
    ) -> list[dict]:
        """
        Run CipherEngine and/or ParallaxEngine on the supplied candle data.

        Returns a list of signal dicts (may be empty if no signal fired).

        Parameters
        ----------
        symbol : str
        df     : pd.DataFrame  OHLCV candles
        preset : str  "parallax", "cipher", or "manual"
        """
        signals: list[dict] = []
        try:
            from strategies.custom import CipherEngine, ParallaxEngine  # type: ignore
        except ImportError:
            logger.error(
                "strategies.custom not importable — engines unavailable. "
                "Ensure strategies/ package is on PYTHONPATH."
            )
            return signals

        if preset in ("parallax", "combined"):
            try:
                engine = ParallaxEngine(symbol=symbol)
                result = engine.evaluate(df)
                if result and result.get("direction") != 0:
                    result["strategy"] = "parallax"
                    signals.append(result)
            except Exception as exc:  # noqa: BLE001
                logger.exception("ParallaxEngine error on %s: %s", symbol, exc)

        if preset in ("cipher", "combined"):
            try:
                engine = CipherEngine(symbol=symbol)
                result = engine.evaluate(df)
                if result and result.get("direction") != 0:
                    result["strategy"] = "cipher"
                    signals.append(result)
            except Exception as exc:  # noqa: BLE001
                logger.exception("CipherEngine error on %s: %s", symbol, exc)

        return signals

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def _log_signal(
        self,
        signal: dict,
        symbol: str,
        strategy_name: str,
        timeframe: str,
        lane: Lane,
    ) -> None:
        """
        Insert a signal into the observed_signals SQLite table.

        Parameters
        ----------
        signal        : dict  Signal dict from engine (direction, entry_price, etc.)
        symbol        : str
        strategy_name : str
        timeframe     : str
        lane          : Lane
        """
        if self.dry_run:
            logger.info(
                "[DRY-RUN] Signal | %s %s %s dir=%s entry=%.4f score=%.3f",
                lane.lane_name, symbol, strategy_name,
                signal.get("direction"),
                signal.get("entry_price", 0),
                signal.get("score", 0),
            )
            return

        session_label = "NY" if lane.session_filter else "always"

        row = (
            lane.lane_name,
            symbol,
            strategy_name,
            timeframe,
            int(signal.get("direction", 0)),
            float(signal.get("entry_price", 0.0)),
            float(signal.get("stop_loss", 0.0)),
            float(signal.get("tp1", 0.0)),
            float(signal.get("tp3", 0.0)),
            float(signal.get("score", 0.0)),
            str(signal.get("reason", "")),
            session_label,
            self.mode,
        )

        sql = """
            INSERT INTO observed_signals
                (lane_name, symbol, strategy, timeframe,
                 direction, entry_price, stop_loss, tp1, tp3,
                 score, reason, session, mode)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        try:
            with sqlite3.connect(self._db_path) as conn:
                conn.execute(sql, row)
                conn.commit()
            logger.info(
                "Signal logged | %s %s %s dir=%s entry=%.4f score=%.3f",
                lane.lane_name, symbol, strategy_name,
                signal.get("direction"),
                signal.get("entry_price", 0),
                signal.get("score", 0),
            )
        except sqlite3.Error as exc:
            logger.error("SQLite error logging signal: %s", exc)

    def _ensure_table(self) -> None:
        """Create observed_signals table if it does not exist."""
        try:
            with sqlite3.connect(self._db_path) as conn:
                conn.execute(_CREATE_OBSERVED_SIGNALS)
                conn.commit()
            logger.debug("observed_signals table ensured.")
        except sqlite3.Error as exc:
            logger.error("SQLite error creating observed_signals: %s", exc)

    # ------------------------------------------------------------------
    # Session window
    # ------------------------------------------------------------------

    def _should_run_now(self, lane: Lane) -> bool:
        """
        Check whether the current UTC time falls within the lane's session.

        Returns True if:
          - lane.session_filter is empty (always-on)
          - "NY" is in session_filter and current UTC time is within
            NY market hours (13:30–21:00 UTC, Mon–Fri)
        """
        if not lane.session_filter:
            return True   # Always-on lane (crypto)

        now_utc = datetime.now(tz=timezone.utc)
        weekday = now_utc.weekday()   # 0=Mon … 4=Fri

        if weekday >= 5:
            logger.debug("_should_run_now: weekend — NY session closed.")
            return False

        if "NY" in lane.session_filter:
            h, m = now_utc.hour, now_utc.minute
            start_minutes = NY_SESSION_START_UTC[0] * 60 + NY_SESSION_START_UTC[1]
            end_minutes   = NY_SESSION_END_UTC[0]   * 60 + NY_SESSION_END_UTC[1]
            current_mins  = h * 60 + m
            in_session = start_minutes <= current_mins < end_minutes
            logger.debug(
                "_should_run_now: NY session check %02d:%02d UTC → %s",
                h, m, in_session,
            )
            return in_session

        return True

    # ------------------------------------------------------------------
    # Heartbeat
    # ------------------------------------------------------------------

    def _heartbeat(self) -> None:
        """Log an 'alive' ping every HEARTBEAT_INTERVAL_SECONDS seconds."""
        now = time.monotonic()
        if now - self._last_heartbeat >= HEARTBEAT_INTERVAL_SECONDS:
            ts = datetime.now(tz=timezone.utc).isoformat()
            msg = f"[HEARTBEAT] {ts} | mode={self.mode} lane={self.lane_name} | alive"
            logger.info(msg)
            try:
                with open(self._log_path, "a", encoding="utf-8") as fh:
                    fh.write(msg + "\n")
            except OSError as exc:
                logger.warning("Could not write heartbeat to log file: %s", exc)
            self._last_heartbeat = now

    # ------------------------------------------------------------------
    # Shutdown
    # ------------------------------------------------------------------

    def _handle_shutdown(self, signum: int, frame) -> None:
        """Handle SIGINT / SIGTERM — stop the polling loop gracefully."""
        sig_name = signal.Signals(signum).name
        logger.info("Received %s — shutting down observer…", sig_name)
        self._running = False


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="GB-BRAIN Live Observer — polls market data, logs signals to SQLite.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--mode",
        choices=["paper", "demo", "live"],
        default="paper",
        help="Operating mode. 'paper' logs only; 'demo' routes to paper executor; "
             "'live' routes to live broker (Phase 9).",
    )
    parser.add_argument(
        "--lane",
        default="GB-INDICES",
        help="Lane group to observe (e.g. GB-INDICES, GB-CRYPTO-BOT, MANUAL-SIGNALS).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="Print signals without writing to SQLite or routing to executor.",
    )
    return parser.parse_args(argv)


def _setup_logging(level: int = logging.INFO) -> None:
    log_dir = ROOT / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(log_dir / "observer.log", encoding="utf-8"),
        ],
    )


if __name__ == "__main__":
    _setup_logging()
    args = _parse_args()
    observer = LiveObserver(
        mode=args.mode,
        lane_name=args.lane,
        dry_run=args.dry_run,
    )
    observer.run()
