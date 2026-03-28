"""
GB-BRAIN — Replay Mode
========================
Replays cached OHLCV data bar-by-bar, feeding it to Cipher/Parallax/Combined engines.
Simulates exactly what live_observer would see on each candle.
No live exchange needed. No API keys needed.

The replay proves: signal generation → paper_executor path works end-to-end on PC.

Usage:
    python simulate/replay_mode.py --ticker US30 --tf 5m
    python simulate/replay_mode.py --ticker BTC --tf 15m --strategy combined
    python simulate/replay_mode.py --ticker SPX --tf 5m --start 2025-01-01 --end 2025-03-01
    python simulate/replay_mode.py --ticker NAS100 --tf 5m --speed 0   # instant

Conventions:
    - SQLite is truth — all signals and paper trades persisted if --save-to-db
    - Capital is priority — PaperExecutor gate enforced
    - STOP → Backup → Patch → Run → Verify
    - .env for secrets — no API keys needed for replay
"""

from __future__ import annotations

import argparse
import logging
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import pandas as pd

# ---------------------------------------------------------------------------
# ROOT — project root two levels up from simulate/
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# ---------------------------------------------------------------------------
# Logger
# ---------------------------------------------------------------------------
logger = logging.getLogger("gb_brain.replay")

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
MIN_WINDOW = 50          # bars before signal generation begins
DATA_CACHE_DIR = ROOT / "backtest" / "data_cache"

# Canonical symbol → CSV stem mapping (mirrors run_custom_backtest.py conventions)
_CSV_STEM_MAP: dict[str, str] = {
    "US30":   "US30",
    "NAS100": "NAS100",
    "SPX":    "SPX",
    "SPX500": "SPX",
    "BTC":    "BTC",
    "ETH":    "ETH",
    "SOL":    "SOL",
}


# ---------------------------------------------------------------------------
# ReplayMode
# ---------------------------------------------------------------------------

class ReplayMode:
    """
    Replays a cached OHLCV CSV bar-by-bar through the selected strategy engine.

    Parameters
    ----------
    ticker     : str   GB-BRAIN symbol (e.g. "US30", "BTC").
    timeframe  : str   Bar timeframe (e.g. "5m", "15m").
    strategy   : str   One of "cipher", "parallax", "combined". Default "combined".
    start      : str   Optional ISO-8601 start date for filtering (e.g. "2025-01-01").
    end        : str   Optional ISO-8601 end date for filtering.
    speed      : float Seconds to sleep between bars.  0 = instant.
    verbose    : bool  Print bar-by-bar progress. Default True.
    save_to_db : bool  Persist paper trades to SQLite when replay finishes.
    """

    def __init__(
        self,
        ticker: str,
        timeframe: str,
        strategy: str = "combined",
        start: Optional[str] = None,
        end: Optional[str] = None,
        speed: float = 0.0,
        verbose: bool = True,
        save_to_db: bool = False,
    ) -> None:
        self.ticker     = ticker.upper()
        self.timeframe  = timeframe
        self.strategy   = strategy.lower()
        self.start      = start
        self.end        = end
        self.speed      = max(0.0, speed)
        self.verbose    = verbose
        self.save_to_db = save_to_db

        # Lazily-imported executor (avoids circular import issues at module load)
        from simulate.paper_executor import PaperExecutor
        self._executor = PaperExecutor(starting_balance=10_000.0)

        # State
        self._signals_today: int = 0
        self._trades_today:  int = 0
        self._total_signals: int = 0

        logger.info(
            "ReplayMode init | ticker=%s tf=%s strategy=%s start=%s end=%s speed=%.2f",
            self.ticker, self.timeframe, self.strategy, self.start, self.end, self.speed,
        )

    # ------------------------------------------------------------------
    # Entry point
    # ------------------------------------------------------------------

    def run(self) -> dict:
        """
        Load cached CSV, filter date range, iterate bar-by-bar through engines.

        Returns
        -------
        dict  — final stats from PaperExecutor.get_stats()
        """
        df = self._load_data()
        if df is None or df.empty:
            logger.error("ReplayMode.run: no data loaded — aborting.")
            return {}

        df = self._apply_date_filter(df)
        if df.empty:
            logger.error("ReplayMode.run: data empty after date filter — aborting.")
            return {}

        total_bars = len(df)
        print(
            f"\n{'='*70}\n"
            f"  GB-BRAIN Replay | {self.ticker} [{self.timeframe}] | "
            f"strategy={self.strategy} | bars={total_bars}\n"
            f"  Range: {df.index[0]}  →  {df.index[-1]}\n"
            f"{'='*70}\n"
        )

        signals_log: list[dict] = []
        current_date: Optional[str] = None

        for i in range(total_bars):
            bar = df.iloc[i]
            bar_date = str(df.index[i])[:10]   # YYYY-MM-DD

            # Day boundary
            if bar_date != current_date:
                if current_date is not None:
                    # Reset daily counters
                    self._signals_today = 0
                    self._trades_today  = 0
                current_date = bar_date

            # ── Tick executor first (check open positions) ─────────────
            closed_this_bar = self._executor.tick(
                bar_high=float(bar.get("high", bar.get("High", 0))),
                bar_low=float(bar.get("low",  bar.get("Low",  0))),
                bar_close=float(bar.get("close", bar.get("Close", 0))),
                bar_time=str(df.index[i]),
            )
            self._trades_today += len(closed_this_bar)

            # ── Minimum window guard ──────────────────────────────────
            if i < MIN_WINDOW:
                if self.verbose and i % 10 == 0:
                    print(f"  [warmup] bar {i+1}/{MIN_WINDOW} warming up…")
                _sleep(self.speed)
                continue

            # ── Run engine on growing window [0..i] ───────────────────
            window_df = df.iloc[: i + 1]
            signals   = self._run_engines(window_df)

            if signals:
                for sig in signals:
                    # Deduplicate: skip if same direction + entry already open
                    if self._is_duplicate(sig):
                        logger.debug("Skipping duplicate signal at bar %d.", i)
                        continue

                    self._process_signal(sig, df, i)
                    signals_log.append(sig)
                    self._total_signals += 1
                    self._signals_today += 1

            # ── Bar progress ──────────────────────────────────────────
            if self.verbose:
                self._print_bar_summary(i, bar, self._signals_today, self._trades_today)

            _sleep(self.speed)

        # ── Force-close remaining open positions ──────────────────────
        if df is not None and not df.empty:
            last_close = float(df.iloc[-1].get("close", df.iloc[-1].get("Close", 0)))
            n_force_closed = self._executor.force_close_all(
                bar_close=last_close,
                bar_time=str(df.index[-1]),
            )
            if n_force_closed:
                logger.info("Replay ended: force-closed %d open position(s).", n_force_closed)

        # ── Persist to DB if requested ────────────────────────────────
        if self.save_to_db:
            n_saved = self._executor.save_to_db()
            logger.info("save_to_db: %d trade(s) written to SQLite.", n_saved)

        # ── Final report ──────────────────────────────────────────────
        self._final_report()

        return self._executor.get_stats()

    # ------------------------------------------------------------------
    # Signal processing
    # ------------------------------------------------------------------

    def _process_signal(self, signal: dict, df: pd.DataFrame, i: int) -> None:
        """
        Log a signal and route it to PaperExecutor.submit().

        Parameters
        ----------
        signal : dict   Signal dict from engine (direction, entry_price, …).
        df     : pd.DataFrame  Full data frame (for context / logging).
        i      : int    Current bar index.
        """
        direction_str = "LONG" if signal.get("direction", 0) == 1 else "SHORT"
        strat         = signal.get("strategy", self.strategy)
        entry         = signal.get("entry_price", 0.0)
        sl            = signal.get("stop_loss",  0.0)
        tp1           = signal.get("tp1",        0.0)
        tp3           = signal.get("tp3",        0.0)
        score         = signal.get("score",      0.0)
        reason        = signal.get("reason",     "")

        logger.info(
            "SIGNAL bar=%d | %s %s %s | entry=%.4f sl=%.4f tp1=%.4f tp3=%.4f "
            "score=%.3f reason=%s",
            i, self.ticker, strat, direction_str,
            entry, sl, tp1, tp3, score, reason,
        )

        print(
            f"  ▶ SIGNAL [{i:05d}] {self.ticker} {strat.upper():10s} "
            f"{direction_str:5s} | entry={entry:.4f} sl={sl:.4f} "
            f"tp1={tp1:.4f} score={score:.3f}"
        )

        trade = self._executor.submit(
            signal=signal,
            symbol=self.ticker,
            strategy=strat,
            timeframe=self.timeframe,
        )

        if trade:
            print(
                f"    → Paper trade opened: {trade.id[:8]}… "
                f"size={trade.size:.4f} | risk=1%"
            )
        else:
            print("    → Paper trade REJECTED (max_open / risk gate / invalid price).")

    # ------------------------------------------------------------------
    # Data loading
    # ------------------------------------------------------------------

    def _load_data(self) -> Optional[pd.DataFrame]:
        """
        Load OHLCV CSV from backtest/data_cache/.

        Tries several filename patterns used by run_custom_backtest.py:
          {TICKER}_{TIMEFRAME}.csv
          {TICKER}_{TIMEFRAME}_cache.csv
          {TICKER}.csv

        Returns pd.DataFrame with DatetimeIndex and lowercase columns,
        or None if no file found.
        """
        stem = _CSV_STEM_MAP.get(self.ticker, self.ticker)
        tf_clean = self.timeframe.replace("m", "m").replace("M", "m")

        candidates = [
            DATA_CACHE_DIR / f"{stem}_{tf_clean}.csv",
            DATA_CACHE_DIR / f"{stem}_{tf_clean}_cache.csv",
            DATA_CACHE_DIR / f"{stem}_{self.timeframe}.csv",
            DATA_CACHE_DIR / f"{stem}.csv",
            # Also look for lowercase ticker
            DATA_CACHE_DIR / f"{stem.lower()}_{tf_clean}.csv",
            DATA_CACHE_DIR / f"{stem.lower()}.csv",
        ]

        for path in candidates:
            if path.exists():
                logger.info("_load_data: loading %s", path)
                try:
                    df = pd.read_csv(path, index_col=0, parse_dates=True)
                    df.columns = [c.lower() for c in df.columns]
                    # Ensure required columns exist
                    for col in ("open", "high", "low", "close"):
                        if col not in df.columns:
                            logger.error("_load_data: missing column '%s' in %s.", col, path)
                            return None
                    df.dropna(subset=["open", "high", "low", "close"], inplace=True)
                    logger.info(
                        "_load_data: loaded %d bars from %s (range: %s → %s).",
                        len(df), path.name, df.index[0], df.index[-1],
                    )
                    return df
                except Exception as exc:  # noqa: BLE001
                    logger.error("_load_data: error reading %s — %s", path, exc)
                    return None

        logger.error(
            "_load_data: no CSV found for %s [%s] in %s. Tried: %s",
            self.ticker, self.timeframe, DATA_CACHE_DIR,
            [str(p) for p in candidates],
        )
        print(
            f"\n  [ERROR] No cached data found for {self.ticker} [{self.timeframe}].\n"
            f"  Expected location: {DATA_CACHE_DIR}\n"
            f"  Run the backtest data download first, or provide a CSV at one of:\n"
        )
        for p in candidates:
            print(f"    {p}")
        return None

    # ------------------------------------------------------------------
    # Engine runner
    # ------------------------------------------------------------------

    def _run_engines(self, df: pd.DataFrame) -> list[dict]:
        """
        Run the selected strategy engine(s) on the provided OHLCV window.

        Parameters
        ----------
        df : pd.DataFrame  Growing window (bars 0 through current bar i).

        Returns
        -------
        List of signal dicts (may be empty).
        """
        signals: list[dict] = []

        try:
            from strategies.custom import CipherEngine, ParallaxEngine  # type: ignore
        except ImportError:
            logger.warning("_run_engines: strategies.custom not importable — engines unavailable.")
            return signals

        if self.strategy in ("parallax", "combined"):
            try:
                engine = ParallaxEngine(symbol=self.ticker)
                result = engine.evaluate(df)
                if result and result.get("direction", 0) != 0:
                    result.setdefault("strategy", "parallax")
                    signals.append(result)
            except Exception as exc:  # noqa: BLE001
                logger.debug("ParallaxEngine error: %s", exc)

        if self.strategy in ("cipher", "combined"):
            try:
                engine = CipherEngine(symbol=self.ticker)
                result = engine.evaluate(df)
                if result and result.get("direction", 0) != 0:
                    result.setdefault("strategy", "cipher")
                    signals.append(result)
            except Exception as exc:  # noqa: BLE001
                logger.debug("CipherEngine error: %s", exc)

        return signals

    # ------------------------------------------------------------------
    # Date filter
    # ------------------------------------------------------------------

    def _apply_date_filter(self, df: pd.DataFrame) -> pd.DataFrame:
        """Filter df by self.start and self.end (inclusive, YYYY-MM-DD)."""
        if self.start:
            try:
                df = df[df.index >= pd.Timestamp(self.start, tz=df.index.tz)]
            except Exception as exc:  # noqa: BLE001
                logger.warning("_apply_date_filter: invalid start '%s' — %s", self.start, exc)
        if self.end:
            try:
                df = df[df.index <= pd.Timestamp(self.end, tz=df.index.tz)]
            except Exception as exc:  # noqa: BLE001
                logger.warning("_apply_date_filter: invalid end '%s' — %s", self.end, exc)
        return df

    # ------------------------------------------------------------------
    # Duplicate guard
    # ------------------------------------------------------------------

    def _is_duplicate(self, signal: dict) -> bool:
        """
        Return True if an open trade already exists for the same symbol+direction.
        Prevents stacking identical signals from consecutive bars.
        """
        direction = signal.get("direction", 0)
        for t in self._executor.get_open_trades():
            if t.symbol == self.ticker and t.direction == direction:
                return True
        return False

    # ------------------------------------------------------------------
    # Console output helpers
    # ------------------------------------------------------------------

    def _print_bar_summary(
        self,
        i: int,
        bar: pd.Series,
        signals_today: int,
        trades_today: int,
    ) -> None:
        """Print a compact one-liner progress update for bar i."""
        close  = float(bar.get("close",  bar.get("Close",  0)))
        high   = float(bar.get("high",   bar.get("High",   0)))
        low    = float(bar.get("low",    bar.get("Low",    0)))
        n_open = len(self._executor.get_open_trades())
        equity = self._executor.equity

        if i % 25 == 0:
            # Print header every 25 bars
            print(
                f"  {'Bar':>6}  {'Close':>10}  {'High':>10}  {'Low':>10}  "
                f"{'Sigs':>5}  {'Closed':>6}  {'Open':>5}  {'Equity':>12}"
            )
            print("  " + "-" * 76)

        print(
            f"  {i:>6}  {close:>10.4f}  {high:>10.4f}  {low:>10.4f}  "
            f"{signals_today:>5}  {trades_today:>6}  {n_open:>5}  {equity:>12,.2f}"
        )

    def _final_report(self) -> None:
        """Print a summary of the full replay with total signals and P&L."""
        stats = self._executor.get_stats()
        print("\n" + "=" * 70)
        print(f"  GB-BRAIN Replay COMPLETE — {self.ticker} [{self.timeframe}]")
        print("=" * 70)
        print(f"  Total signals generated : {self._total_signals}")
        print(f"  Closed trades           : {stats['trade_count']}")
        print(f"  Win rate                : {stats['win_rate']:.1f}%")
        print(f"  PnL (pts)               : {stats['pnl_total']:+.4f}")
        print(f"  PnL ($)                 : {stats['pnl_dollar']:+,.2f}")
        print(f"  Profit factor           : {stats['profit_factor']:.3f}")
        print(f"  Avg R:R                 : {stats['avg_rr']:.3f}")
        print(f"  Max drawdown            : {stats['max_drawdown'] * 100:.2f}%")
        print(f"  Final equity            : {stats['equity']:,.2f}")
        print("=" * 70 + "\n")
        self._executor.print_summary()


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

def _sleep(seconds: float) -> None:
    """Sleep only if seconds > 0."""
    if seconds > 0:
        time.sleep(seconds)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="GB-BRAIN Replay Mode — bar-by-bar engine replay on cached OHLCV data.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--ticker",
        default="SPX",
        help="GB-BRAIN symbol to replay (e.g. US30, BTC, SPX, NAS100).",
    )
    parser.add_argument(
        "--tf",
        default="5m",
        dest="timeframe",
        help="Bar timeframe to replay (e.g. 5m, 15m, 1h).",
    )
    parser.add_argument(
        "--strategy",
        choices=["cipher", "parallax", "combined"],
        default="combined",
        help="Strategy engine(s) to run.",
    )
    parser.add_argument(
        "--start",
        default=None,
        help="Start date filter (YYYY-MM-DD). Optional.",
    )
    parser.add_argument(
        "--end",
        default=None,
        help="End date filter (YYYY-MM-DD). Optional.",
    )
    parser.add_argument(
        "--speed",
        type=float,
        default=0.0,
        help="Seconds per bar. 0 = instant, 0.1 = 100ms/bar.",
    )
    parser.add_argument(
        "--save-to-db",
        action="store_true",
        default=False,
        help="Write paper trades to SQLite live_trades table after replay.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        default=False,
        help="Suppress bar-by-bar progress output.",
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
            logging.FileHandler(log_dir / "replay.log", encoding="utf-8"),
        ],
    )


if __name__ == "__main__":
    _setup_logging()
    _args = _parse_args()

    replay = ReplayMode(
        ticker=_args.ticker,
        timeframe=_args.timeframe,
        strategy=_args.strategy,
        start=_args.start,
        end=_args.end,
        speed=_args.speed,
        verbose=not _args.quiet,
        save_to_db=_args.save_to_db,
    )
    replay.run()
