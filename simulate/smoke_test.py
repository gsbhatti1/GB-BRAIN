"""
GB-BRAIN — Smoke Test
======================
Injects forced signals to prove the full path works:
  signal → paper_executor → SQLite → risk_manager → Telegram alert

Two modes:
  forced   → Creates synthetic perfect signals, bypasses engine
  engine   → Runs real engine on last N bars of cached data

Usage:
    python simulate/smoke_test.py                              # Forced mode, SPX
    python simulate/smoke_test.py --mode forced --symbol SPX
    python simulate/smoke_test.py --mode engine --symbol US30 --tf 5m
    python simulate/smoke_test.py --check-only               # Verify imports/DB only

Conventions:
    - SQLite is truth — DB tables verified, paper trades written
    - Capital is priority — RiskManager path tested
    - STOP → Backup → Patch → Run → Verify
    - .env for secrets — credentials checked, never logged
"""

from __future__ import annotations

import argparse
import logging
import os
import sqlite3
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# ROOT — project root two levels up from simulate/
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# ---------------------------------------------------------------------------
# Logger
# ---------------------------------------------------------------------------
logger = logging.getLogger("gb_brain.smoke")

# ---------------------------------------------------------------------------
# DB path
# ---------------------------------------------------------------------------
try:
    from config import settings as _settings  # type: ignore
    _DB_PATH: Path = Path(getattr(_settings, "DB_PATH", ROOT / "db" / "gb_brain.db"))
except Exception:  # noqa: BLE001
    _DB_PATH = ROOT / "db" / "gb_brain.db"

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
DATA_CACHE_DIR = ROOT / "backtest" / "data_cache"

# Tables that must exist for GB-BRAIN to function
_REQUIRED_TABLES = [
    "strategies",
    "backtest_results",
    "live_trades",
    "bots",
    "observed_signals",
]

# .env keys to check (not logged, only presence checked)
_ENV_KEYS = [
    "GITHUB_TOKEN",
    "BINANCE_API_KEY",
    "BINANCE_API_SECRET",
    "OANDA_ACCOUNT_ID",
    "OANDA_API_KEY",
    "BLOFIN_API_KEY",
    "BLOFIN_API_SECRET",
    "TELEGRAM_BOT_TOKEN",
    "TELEGRAM_CHAT_ID",
    "ALPACA_API_KEY",
    "ALPACA_API_SECRET",
    "ALPACA_BASE_URL",
]

# Synthetic price parameters per symbol (entry, sl_dist, tp1_mult, tp3_mult)
_SYMBOL_PARAMS: dict[str, dict] = {
    "SPX":    {"entry": 5_250.00, "sl_dist": 15.0,   "direction":  1},
    "NAS100": {"entry": 18_500.00,"sl_dist": 50.0,   "direction":  1},
    "US30":   {"entry": 40_000.00,"sl_dist": 80.0,   "direction":  1},
    "BTC":    {"entry": 65_000.00,"sl_dist": 500.0,  "direction":  1},
    "ETH":    {"entry": 3_400.00, "sl_dist": 40.0,   "direction":  1},
    "SOL":    {"entry": 150.00,   "sl_dist": 3.0,    "direction":  1},
}


# ---------------------------------------------------------------------------
# Result container
# ---------------------------------------------------------------------------

@dataclass
class _TestResult:
    name: str
    status: str = "PENDING"    # PASS / FAIL / SKIP / WARN
    notes:  str = ""


# ---------------------------------------------------------------------------
# SmokeTest
# ---------------------------------------------------------------------------

class SmokeTest:
    """
    Runs a battery of checks to verify the GB-BRAIN pipeline is healthy.

    Parameters
    ----------
    mode         : str  "forced" (synthetic signals) or "engine" (real engine on cache).
    symbol       : str  Instrument to test against. Default "SPX".
    timeframe    : str  Bar timeframe for engine mode. Default "5m".
    num_signals  : int  Number of synthetic signals in forced mode. Default 5.
    skip_telegram: bool Skip Telegram alert test even if configured.
    """

    def __init__(
        self,
        mode: str = "forced",
        symbol: str = "SPX",
        timeframe: str = "5m",
        num_signals: int = 5,
        skip_telegram: bool = False,
    ) -> None:
        self.mode          = mode.lower()
        self.symbol        = symbol.upper()
        self.timeframe     = timeframe
        self.num_signals   = num_signals
        self.skip_telegram = skip_telegram

        self._results: list[_TestResult] = []

    # ------------------------------------------------------------------
    # Entry point
    # ------------------------------------------------------------------

    def run(self, check_only: bool = False) -> bool:
        """
        Execute the full smoke test suite.

        Parameters
        ----------
        check_only : bool
            If True, only run _check_imports, _check_db, _check_env — skip
            signal generation, executor, and Telegram tests.

        Returns
        -------
        bool — True if all non-SKIP results are PASS.
        """
        print("\n" + "=" * 65)
        print("  GB-BRAIN Smoke Test")
        print(f"  Mode: {self.mode.upper()}  |  Symbol: {self.symbol}  |  TF: {self.timeframe}")
        print("=" * 65 + "\n")

        # ── Phase 1: System checks ─────────────────────────────────────
        self._check_imports()
        self._check_db()
        self._check_env()

        if check_only:
            self._print_results()
            return self._all_passed()

        # ── Phase 2: Signal generation ────────────────────────────────
        if self.mode == "forced":
            signals = self._forced_signals(self.num_signals)
        else:
            signals = self._engine_signals(self.symbol, self.timeframe)

        if not signals:
            self._results.append(_TestResult(
                name="signal_generation",
                status="FAIL",
                notes=f"No signals produced in '{self.mode}' mode.",
            ))
        else:
            self._results.append(_TestResult(
                name="signal_generation",
                status="PASS",
                notes=f"{len(signals)} signal(s) generated.",
            ))

        # ── Phase 3: Paper executor path ──────────────────────────────
        submitted_trades = self._run_through_executor(signals)

        # ── Phase 4: Risk manager test ────────────────────────────────
        self._run_through_risk_manager(signals)

        # ── Phase 5: Telegram alert ───────────────────────────────────
        if not self.skip_telegram:
            stats_summary = self._build_result_summary(len(signals), len(submitted_trades))
            self._send_test_telegram(stats_summary)
        else:
            self._results.append(_TestResult(
                name="telegram_alert",
                status="SKIP",
                notes="--skip-telegram flag set.",
            ))

        # ── Final output ──────────────────────────────────────────────
        self._print_results()
        passed = self._all_passed()

        print("\n" + ("=" * 65))
        if passed:
            print("  SMOKE TEST PASSED ✓")
        else:
            fail_count = sum(1 for r in self._results if r.status == "FAIL")
            print(f"  SMOKE TEST FAILED ✗  ({fail_count} failure(s))")
        print("=" * 65 + "\n")

        return passed

    # ------------------------------------------------------------------
    # Check: imports
    # ------------------------------------------------------------------

    def _check_imports(self) -> None:
        """Verify all core GB-BRAIN modules can be imported. Prints PASS/FAIL per module."""
        print("  ── Import Check ─────────────────────────────────────────")

        modules = [
            ("simulate.paper_executor",     "PaperExecutor"),
            ("simulate.replay_mode",        "ReplayMode"),
            ("runtime.runtime_policy",      "RuntimePolicy"),
            ("runtime.live_observer",       "LiveObserver"),
            ("runtime.weekly_calibrator",   "WeeklyCalibrator"),
            ("execute.alpaca_bridge",       "AlpacaBridge"),
            ("strategies.custom",           "CipherEngine"),
            ("strategies.custom",           "ParallaxEngine"),
            ("monitor.risk_manager",        "RiskManager"),
            ("monitor.dashboard",           "app"),
            ("db.brain_db",                 "BrainDB"),
            ("config.settings",             None),
        ]

        all_pass = True
        for mod_name, attr in modules:
            try:
                mod = __import__(mod_name, fromlist=[attr] if attr else [])
                if attr and not hasattr(mod, attr):
                    raise ImportError(f"'{attr}' not found in {mod_name}")
                status = "PASS"
                notes  = f"{mod_name}.{attr}" if attr else mod_name
            except ImportError as exc:
                status = "FAIL"
                notes  = str(exc)
                all_pass = False
            except Exception as exc:  # noqa: BLE001
                status = "WARN"
                notes  = str(exc)

            icon = "✓" if status == "PASS" else ("✗" if status == "FAIL" else "!")
            print(f"    [{icon}] {status:4s}  {mod_name}")
            if status != "PASS":
                print(f"           └─ {notes}")

        self._results.append(_TestResult(
            name="imports",
            status="PASS" if all_pass else "FAIL",
            notes="All modules importable." if all_pass else "One or more imports failed.",
        ))
        print()

    # ------------------------------------------------------------------
    # Check: database
    # ------------------------------------------------------------------

    def _check_db(self) -> None:
        """Connect to SQLite and verify required tables exist. Prints PASS/FAIL per table."""
        print("  ── Database Check ───────────────────────────────────────")
        print(f"    DB path: {_DB_PATH}")

        if not _DB_PATH.exists():
            print(f"    [✗] DB file does not exist: {_DB_PATH}")
            self._results.append(_TestResult(
                name="db_tables",
                status="FAIL",
                notes=f"DB not found: {_DB_PATH}",
            ))
            print()
            return

        try:
            with sqlite3.connect(_DB_PATH) as conn:
                cursor = conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table';"
                )
                existing = {row[0] for row in cursor.fetchall()}
        except sqlite3.Error as exc:
            print(f"    [✗] Cannot connect to DB: {exc}")
            self._results.append(_TestResult(
                name="db_tables",
                status="FAIL",
                notes=f"SQLite error: {exc}",
            ))
            print()
            return

        all_pass = True
        for table in _REQUIRED_TABLES:
            present = table in existing
            icon    = "✓" if present else "✗"
            status  = "PASS" if present else "FAIL"
            if not present:
                all_pass = False
            print(f"    [{icon}] {status:4s}  table={table}")

        # Also report any extra tables found
        extra = existing - set(_REQUIRED_TABLES)
        if extra:
            print(f"    [i]       extra tables: {', '.join(sorted(extra))}")

        self._results.append(_TestResult(
            name="db_tables",
            status="PASS" if all_pass else "FAIL",
            notes=f"Present: {existing}",
        ))
        print()

    # ------------------------------------------------------------------
    # Check: .env / environment
    # ------------------------------------------------------------------

    def _check_env(self) -> None:
        """
        Load .env if present, then list which secrets are set vs missing.
        Values are never printed — only presence is checked.
        """
        print("  ── Environment / .env Check ─────────────────────────────")

        env_path = ROOT / ".env"
        if env_path.exists():
            try:
                _load_dotenv(env_path)
                print(f"    [✓] .env found and loaded: {env_path}")
            except Exception as exc:  # noqa: BLE001
                print(f"    [!] .env found but load error: {exc}")
        else:
            print(f"    [i] No .env file at {env_path} — using system environment.")

        present_keys:  list[str] = []
        missing_keys:  list[str] = []

        for key in _ENV_KEYS:
            val = os.environ.get(key, "")
            if val:
                present_keys.append(key)
                print(f"    [✓] SET    {key}")
            else:
                missing_keys.append(key)
                print(f"    [-] UNSET  {key}")

        notes = (
            f"{len(present_keys)} set, {len(missing_keys)} missing: "
            + (", ".join(missing_keys) if missing_keys else "none")
        )

        # Telegram specifically — warn if missing so test can be skipped
        telegram_ready = bool(
            os.environ.get("TELEGRAM_BOT_TOKEN") and os.environ.get("TELEGRAM_CHAT_ID")
        )
        status = "PASS" if present_keys else "WARN"

        self._results.append(_TestResult(
            name="env_check",
            status=status,
            notes=notes,
        ))
        print()

    # ------------------------------------------------------------------
    # Signal generation
    # ------------------------------------------------------------------

    def _forced_signals(self, n: int) -> list[dict]:
        """
        Create n synthetic CipherSignal-style dicts with realistic prices for self.symbol.

        Alternates between LONG (direction=1) and SHORT (direction=-1) to exercise both paths.

        Parameters
        ----------
        n : int  Number of synthetic signals to generate.

        Returns
        -------
        List of signal dicts.
        """
        params   = _SYMBOL_PARAMS.get(self.symbol, _SYMBOL_PARAMS["SPX"])
        entry    = params["entry"]
        sl_dist  = params["sl_dist"]
        signals: list[dict] = []

        for i in range(n):
            direction = 1 if i % 2 == 0 else -1
            sl  = entry - (sl_dist * direction)
            tp1 = entry + (sl_dist * 1.5 * direction)
            tp3 = entry + (sl_dist * 3.0 * direction)

            sig = {
                "direction":   direction,
                "entry_price": round(entry + (i * sl_dist * 0.1 * direction), 2),
                "stop_loss":   round(sl,  2),
                "tp1":         round(tp1, 2),
                "tp3":         round(tp3, 2),
                "score":       round(0.70 + (i % 3) * 0.05, 3),
                "reason":      f"smoke_forced_signal_{i+1}",
                "strategy":    "cipher" if i % 2 == 0 else "parallax",
                "symbol":      self.symbol,
            }
            signals.append(sig)
            logger.debug("_forced_signals[%d]: %s", i, sig)

        print(f"  Generated {n} synthetic signal(s) for {self.symbol}.")
        return signals

    def _engine_signals(self, symbol: str, tf: str) -> list[dict]:
        """
        Load last 200 bars from data cache and run CipherEngine + ParallaxEngine.

        Parameters
        ----------
        symbol : str  GB-BRAIN symbol.
        tf     : str  Timeframe string.

        Returns
        -------
        List of signal dicts from the engines.
        """
        print(f"  Loading last 200 bars from cache for {symbol} [{tf}] …")

        df = _load_cached_bars(symbol, tf, n_bars=200)
        if df is None or df.empty:
            print(f"  [✗] No cached data for {symbol} [{tf}] — engine signals unavailable.")
            return []

        signals: list[dict] = []
        try:
            from strategies.custom import CipherEngine, ParallaxEngine  # type: ignore
        except ImportError as exc:
            print(f"  [✗] strategies.custom not importable: {exc}")
            return signals

        for engine_cls, name in ((CipherEngine, "cipher"), (ParallaxEngine, "parallax")):
            try:
                engine = engine_cls(symbol=symbol)
                result = engine.evaluate(df)
                if result and result.get("direction", 0) != 0:
                    result.setdefault("strategy", name)
                    result.setdefault("symbol",   symbol)
                    signals.append(result)
                    print(f"  [✓] {name.upper():10s} → direction={result.get('direction')} "
                          f"score={result.get('score', 0):.3f}")
                else:
                    print(f"  [i] {name.upper():10s} → no signal on last bar.")
            except Exception as exc:  # noqa: BLE001
                print(f"  [✗] {name.upper():10s} → error: {exc}")
                logger.exception("_engine_signals: %s error", name)

        return signals

    # ------------------------------------------------------------------
    # Executor path
    # ------------------------------------------------------------------

    def _run_through_executor(self, signals: list[dict]) -> list:
        """
        Submit each signal to PaperExecutor and verify the trade appears in SQLite.

        Parameters
        ----------
        signals : list[dict]  Signal dicts to submit.

        Returns
        -------
        List of PaperTrade objects that were successfully opened.
        """
        print("  ── Paper Executor ───────────────────────────────────────")

        try:
            from simulate.paper_executor import PaperExecutor
        except ImportError as exc:
            print(f"  [✗] PaperExecutor not importable: {exc}")
            self._results.append(_TestResult(
                name="paper_executor",
                status="FAIL",
                notes=str(exc),
            ))
            return []

        executor = PaperExecutor(starting_balance=10_000.0)
        opened: list = []

        for i, sig in enumerate(signals):
            trade = executor.submit(
                signal=sig,
                symbol=sig.get("symbol", self.symbol),
                strategy=sig.get("strategy", "smoke"),
                timeframe=self.timeframe,
            )
            if trade:
                opened.append(trade)
                print(f"  [✓] Signal {i+1}: paper trade opened → {trade.id[:8]}…")
            else:
                print(f"  [!] Signal {i+1}: trade rejected (max_open / risk gate).")

        # Force-close all at synthetic exit price for DB write test
        if opened:
            sample_entry = opened[0].entry_price
            executor.force_close_all(bar_close=sample_entry * 1.005)
            n_saved = executor.save_to_db()
            if n_saved > 0:
                print(f"  [✓] SQLite write: {n_saved} paper trade(s) saved to live_trades.")
                self._results.append(_TestResult(
                    name="paper_executor",
                    status="PASS",
                    notes=f"{len(opened)} opened, {n_saved} written to DB.",
                ))
            else:
                print("  [✗] SQLite write failed — 0 trades saved.")
                self._results.append(_TestResult(
                    name="paper_executor",
                    status="FAIL",
                    notes="save_to_db returned 0.",
                ))
        else:
            self._results.append(_TestResult(
                name="paper_executor",
                status="WARN",
                notes="No trades opened (all rejected). Check max_open cap.",
            ))

        print()
        return opened

    # ------------------------------------------------------------------
    # Risk manager path
    # ------------------------------------------------------------------

    def _run_through_risk_manager(self, signals: list[dict]) -> None:
        """
        Call RiskManager.can_trade() for each signal and report the result.

        Parameters
        ----------
        signals : list[dict]  Signal dicts to test.
        """
        print("  ── Risk Manager ─────────────────────────────────────────")

        try:
            from monitor.risk_manager import RiskManager  # type: ignore
            rm = RiskManager()
        except ImportError as exc:
            print(f"  [!] RiskManager not importable: {exc}")
            self._results.append(_TestResult(
                name="risk_manager",
                status="WARN",
                notes=f"ImportError: {exc}",
            ))
            print()
            return
        except Exception as exc:  # noqa: BLE001
            print(f"  [!] RiskManager init error: {exc}")
            self._results.append(_TestResult(
                name="risk_manager",
                status="WARN",
                notes=f"InitError: {exc}",
            ))
            print()
            return

        all_checked = True
        for i, sig in enumerate(signals):
            sym   = sig.get("symbol",   self.symbol)
            strat = sig.get("strategy", "smoke")
            try:
                allowed = rm.can_trade(symbol=sym, strategy=strat)
                icon    = "✓" if allowed else "–"
                print(f"  [{icon}] Signal {i+1}: {sym}/{strat} → can_trade={allowed}")
            except Exception as exc:  # noqa: BLE001
                print(f"  [!] Signal {i+1}: RiskManager error — {exc}")
                all_checked = False

        self._results.append(_TestResult(
            name="risk_manager",
            status="PASS" if all_checked else "WARN",
            notes=f"Checked {len(signals)} signal(s).",
        ))
        print()

    # ------------------------------------------------------------------
    # Telegram
    # ------------------------------------------------------------------

    def _send_test_telegram(self, result_summary: str) -> None:
        """
        Send a test alert via Telegram if BOT_TOKEN + CHAT_ID are configured.
        If not configured, logs a skip and moves on.

        Parameters
        ----------
        result_summary : str  Brief smoke test result string for the message body.
        """
        print("  ── Telegram Alert ───────────────────────────────────────")

        bot_token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
        chat_id   = os.environ.get("TELEGRAM_CHAT_ID",   "")

        if not bot_token or not chat_id:
            print("  [i] TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID not set — skipping.")
            self._results.append(_TestResult(
                name="telegram_alert",
                status="SKIP",
                notes="Telegram credentials not configured.",
            ))
            print()
            return

        message = (
            f"🧪 GB-BRAIN Smoke Test\n"
            f"Symbol: {self.symbol}  Mode: {self.mode.upper()}\n"
            f"Time: {_utcnow()}\n\n"
            f"{result_summary}"
        )

        try:
            import urllib.request
            import json as _json

            url     = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            payload = _json.dumps({"chat_id": chat_id, "text": message}).encode("utf-8")
            req     = urllib.request.Request(url, data=payload,
                                             headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                resp_data = _json.loads(resp.read())
                if resp_data.get("ok"):
                    print("  [✓] Telegram alert sent successfully.")
                    self._results.append(_TestResult(
                        name="telegram_alert",
                        status="PASS",
                        notes="Message delivered.",
                    ))
                else:
                    print(f"  [✗] Telegram returned ok=false: {resp_data}")
                    self._results.append(_TestResult(
                        name="telegram_alert",
                        status="FAIL",
                        notes=f"ok=false: {resp_data}",
                    ))
        except Exception as exc:  # noqa: BLE001
            print(f"  [✗] Telegram send error: {exc}")
            self._results.append(_TestResult(
                name="telegram_alert",
                status="FAIL",
                notes=str(exc),
            ))
        print()

    # ------------------------------------------------------------------
    # Results table
    # ------------------------------------------------------------------

    def _print_results(self) -> None:
        """Print a clean table: test name | status | notes."""
        print("\n" + "=" * 65)
        print("  Results Summary")
        print("=" * 65)
        header = f"  {'Test':28s}  {'Status':6s}  Notes"
        print(header)
        print("  " + "-" * 62)
        for r in self._results:
            icon = {"PASS": "✓", "FAIL": "✗", "SKIP": "–", "WARN": "!", "PENDING": "?"}.get(
                r.status, "?"
            )
            print(f"  [{icon}] {r.name:26s}  {r.status:6s}  {r.notes}")
        print()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _all_passed(self) -> bool:
        """Return True if no results have status FAIL."""
        return not any(r.status == "FAIL" for r in self._results)

    def _build_result_summary(self, n_signals: int, n_trades: int) -> str:
        """Build a short text summary for Telegram."""
        passed = self._all_passed()
        overall = "PASSED ✓" if passed else "FAILED ✗"
        lines   = [f"Overall: {overall}", f"Signals: {n_signals}  Trades: {n_trades}"]
        for r in self._results:
            icon = "✓" if r.status == "PASS" else ("✗" if r.status == "FAIL" else "–")
            lines.append(f"  {icon} {r.name}: {r.status}")
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Module-level utilities
# ---------------------------------------------------------------------------

def _utcnow() -> str:
    return datetime.now(tz=timezone.utc).isoformat()


def _load_dotenv(path: Path) -> None:
    """Minimal .env parser — sets os.environ for KEY=VALUE lines."""
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, val = line.partition("=")
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = val


def _load_cached_bars(symbol: str, tf: str, n_bars: int = 200):
    """
    Load the last n_bars rows from a cached CSV for symbol/tf.
    Returns pd.DataFrame or None.
    """
    try:
        import pandas as pd
    except ImportError:
        return None

    stem       = symbol.upper()
    tf_clean   = tf.lower()
    candidates = [
        DATA_CACHE_DIR / f"{stem}_{tf_clean}.csv",
        DATA_CACHE_DIR / f"{stem}_{tf_clean}_cache.csv",
        DATA_CACHE_DIR / f"{stem}.csv",
        DATA_CACHE_DIR / f"{stem.lower()}_{tf_clean}.csv",
        DATA_CACHE_DIR / f"{stem.lower()}.csv",
    ]

    for path in candidates:
        if path.exists():
            try:
                df = pd.read_csv(path, index_col=0, parse_dates=True)
                df.columns = [c.lower() for c in df.columns]
                return df.tail(n_bars)
            except Exception:  # noqa: BLE001
                return None
    return None


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="GB-BRAIN Smoke Test — verify full signal→executor pipeline.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--mode",
        choices=["forced", "engine"],
        default="forced",
        help="Signal source: 'forced' uses synthetic signals; 'engine' uses real engines on cache.",
    )
    parser.add_argument(
        "--symbol",
        default="SPX",
        help="Instrument symbol (e.g. SPX, US30, BTC).",
    )
    parser.add_argument(
        "--tf",
        default="5m",
        dest="timeframe",
        help="Bar timeframe for engine mode (e.g. 5m, 15m).",
    )
    parser.add_argument(
        "--num-signals",
        type=int,
        default=5,
        help="Number of synthetic signals in forced mode.",
    )
    parser.add_argument(
        "--check-only",
        action="store_true",
        default=False,
        help="Only run import / DB / env checks — skip signal and executor tests.",
    )
    parser.add_argument(
        "--skip-telegram",
        action="store_true",
        default=False,
        help="Skip the Telegram alert test even if credentials are present.",
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
            logging.FileHandler(log_dir / "smoke_test.log", encoding="utf-8"),
        ],
    )


if __name__ == "__main__":
    _setup_logging()
    _args = _parse_args()

    test = SmokeTest(
        mode=_args.mode,
        symbol=_args.symbol,
        timeframe=_args.timeframe,
        num_signals=_args.num_signals,
        skip_telegram=_args.skip_telegram,
    )
    passed = test.run(check_only=_args.check_only)
    sys.exit(0 if passed else 1)
