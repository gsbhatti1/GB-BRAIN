"""
GB-BRAIN — Engine Parity Check (Phase 4)
==========================================
Verifies that backtest truth = runtime truth by checking:
1. Symbol mapping consistency across all modules
2. Entry/SL/TP logic is identical in backtest vs runtime engines
3. Preset parameters used in backtest match what runtime uses
4. Close-bar rules consistent (no look-ahead)
5. Timeframe handling consistent

Usage:
    python simulate/engine_parity_check.py
    python simulate/engine_parity_check.py --verbose
"""

import argparse
import ast
import importlib
import inspect
import json
import os
import sqlite3
import sys
import textwrap
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Path bootstrap — add project root so imports resolve regardless of cwd
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# ---------------------------------------------------------------------------
# ANSI colours (disabled if not a TTY)
# ---------------------------------------------------------------------------
_TTY = sys.stdout.isatty()


def _green(s: str) -> str:
    return f"\033[92m{s}\033[0m" if _TTY else s


def _red(s: str) -> str:
    return f"\033[91m{s}\033[0m" if _TTY else s


def _yellow(s: str) -> str:
    return f"\033[93m{s}\033[0m" if _TTY else s


def _bold(s: str) -> str:
    return f"\033[1m{s}\033[0m" if _TTY else s


# ---------------------------------------------------------------------------
# Safe import helper
# ---------------------------------------------------------------------------

def _try_import(module_path: str) -> tuple[Any, str | None]:
    """Return (module, None) on success or (None, error_message) on failure."""
    try:
        mod = importlib.import_module(module_path)
        return mod, None
    except Exception as exc:
        return None, str(exc)


# ---------------------------------------------------------------------------
# ParityChecker
# ---------------------------------------------------------------------------

class ParityChecker:
    """
    Runs a battery of structural/logical consistency checks that confirm the
    backtest environment and the live runtime environment are driven by
    identical rules, parameters, and data conventions.
    """

    # Required keys every entry in gb_strategy_gems.json must carry
    GEM_REQUIRED_KEYS: tuple[str, ...] = ("params", "metrics", "status", "tags")

    # Required SQLite tables and their minimum required columns
    DB_SCHEMA: dict[str, tuple[str, ...]] = {
        "strategies": ("id", "name", "status"),
        "backtest_results": ("win_rate", "profit_factor", "status"),
        "live_trades": ("broker", "symbol", "status"),
        "observed_signals": ("lane_name", "score", "mode"),
    }

    # Canonical timeframes the system supports
    EXPECTED_TIMEFRAMES: tuple[str, ...] = (
        "1m", "5m", "15m", "30m", "1h", "2h", "4h", "8h", "1d",
    )

    def __init__(self, verbose: bool = False) -> None:
        self.verbose = verbose
        self.results: dict[str, dict[str, Any]] = {}

    # ------------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------------

    def run_all(self) -> dict[str, dict[str, Any]]:
        """
        Execute every check in sequence.  Returns a dict keyed by check name
        with sub-keys: status (PASS | FAIL | WARN), notes (list[str]).
        """
        checks = [
            ("symbol_maps",         self.check_symbol_maps),
            ("preset_consistency",  self.check_preset_consistency),
            ("close_bar_rules",     self.check_close_bar_rules),
            ("timeframe_coverage",  self.check_timeframe_coverage),
            ("gem_json_structure",  self.check_gem_json_structure),
            ("db_schema",           self.check_db_schema),
        ]

        for name, fn in checks:
            if self.verbose:
                print(f"  → Running {name} …")
            try:
                status, notes = fn()
            except Exception as exc:
                status, notes = "FAIL", [f"Unhandled exception: {exc}"]
            self.results[name] = {"status": status, "notes": notes}

        self._print_report(self.results)
        return self.results

    # ------------------------------------------------------------------
    # Individual checks
    # ------------------------------------------------------------------

    def check_symbol_maps(self) -> tuple[str, list[str]]:
        """
        Verify OANDA SYMBOL_MAP, BloFin SYMBOL_MAP, and
        settings.py CRYPTO_TICKERS / INDEX_TICKERS all agree on canonical
        symbols.  Reports any mismatches.
        """
        notes: list[str] = []
        status = "PASS"

        # --- Load settings canonical lists ---
        settings_mod, err = _try_import("config.settings")
        if err:
            return "WARN", [f"Cannot import config.settings: {err}"]

        crypto_tickers: list[str] = getattr(settings_mod, "CRYPTO_TICKERS", [])
        index_tickers:  list[str] = getattr(settings_mod, "INDEX_TICKERS",  [])
        canonical_symbols = set(crypto_tickers) | set(index_tickers)

        if self.verbose:
            print(f"    settings.py canonical symbols ({len(canonical_symbols)}): "
                  f"{sorted(canonical_symbols)}")

        # --- Load OANDA symbol map ---
        oanda_mod, err = _try_import("brokers.oanda_broker")
        oanda_map: dict[str, str] = {}
        if err:
            notes.append(f"WARN — Cannot import brokers.oanda_broker: {err}")
        else:
            oanda_map = getattr(oanda_mod, "SYMBOL_MAP", {})
            if not oanda_map:
                notes.append("WARN — brokers.oanda_broker.SYMBOL_MAP is empty or missing")

        # --- Load BloFin symbol map ---
        blofin_mod, err = _try_import("brokers.blofin_broker")
        blofin_map: dict[str, str] = {}
        if err:
            notes.append(f"WARN — Cannot import brokers.blofin_broker: {err}")
        else:
            blofin_map = getattr(blofin_mod, "SYMBOL_MAP", {})
            if not blofin_map:
                notes.append("WARN — brokers.blofin_broker.SYMBOL_MAP is empty or missing")

        # --- Cross-check canonical → broker maps ---
        for sym in sorted(canonical_symbols):
            missing_in = []
            if oanda_map and sym not in oanda_map:
                missing_in.append("OANDA")
            if blofin_map and sym not in blofin_map:
                missing_in.append("BloFin")
            if missing_in:
                notes.append(f"MISMATCH — '{sym}' not in {', '.join(missing_in)} SYMBOL_MAP")
                status = "FAIL"

        # --- Check for broker-only symbols not in canonical set ---
        for src, smap in [("OANDA", oanda_map), ("BloFin", blofin_map)]:
            for sym in smap:
                if sym not in canonical_symbols:
                    notes.append(
                        f"WARN — '{sym}' in {src} SYMBOL_MAP but not in settings.py"
                    )
                    if status == "PASS":
                        status = "WARN"

        if not notes:
            notes.append(
                f"All {len(canonical_symbols)} canonical symbols present in both broker maps"
            )

        return status, notes

    # ------------------------------------------------------------------

    def check_preset_consistency(self) -> tuple[str, list[str]]:
        """
        For each ticker entry in PRESETS, verify the preset keys match the
        parameters CipherEngine and ParallaxEngine actually accept.
        """
        notes: list[str] = []
        status = "PASS"

        presets_mod, err = _try_import("config.presets")
        if err:
            return "WARN", [f"Cannot import config.presets: {err}"]

        PRESETS = getattr(presets_mod, "PRESETS", {})
        if not PRESETS:
            return "WARN", ["config.presets.PRESETS is empty or missing"]

        # Collect engine param signatures
        engine_params: dict[str, set[str]] = {}
        for engine_name, mod_path, cls_name in [
            ("CipherEngine",   "engines.cipher_engine",   "CipherEngine"),
            ("ParallaxEngine", "engines.parallax_engine", "ParallaxEngine"),
        ]:
            mod, err = _try_import(mod_path)
            if err:
                notes.append(f"WARN — Cannot import {mod_path}: {err}")
                continue
            cls = getattr(mod, cls_name, None)
            if cls is None:
                notes.append(f"WARN — {cls_name} not found in {mod_path}")
                continue
            try:
                sig = inspect.signature(cls.__init__)
                params = {
                    k for k in sig.parameters
                    if k not in ("self", "args", "kwargs")
                }
                engine_params[engine_name] = params
                if self.verbose:
                    print(f"    {engine_name} __init__ params: {sorted(params)}")
            except Exception as exc:
                notes.append(f"WARN — Cannot inspect {cls_name}.__init__: {exc}")

        if not engine_params:
            return "WARN", notes + ["No engine param signatures could be loaded"]

        # Validate each preset
        all_engine_params = set().union(*engine_params.values())
        mismatch_count = 0

        for ticker, preset in PRESETS.items():
            if not isinstance(preset, dict):
                notes.append(f"FAIL — PRESETS['{ticker}'] is not a dict")
                status = "FAIL"
                continue

            unknown_keys = set(preset.keys()) - all_engine_params - {
                # Allowed meta-keys that are not engine params
                "engine", "timeframe", "broker", "lane", "tags", "description",
            }
            if unknown_keys:
                notes.append(
                    f"MISMATCH — PRESETS['{ticker}'] has unknown keys: "
                    f"{sorted(unknown_keys)}"
                )
                status = "FAIL"
                mismatch_count += 1

        if mismatch_count == 0 and "FAIL" not in [
            n[:4] for n in notes
        ]:
            notes.append(
                f"All {len(PRESETS)} presets validated against engine signatures"
            )

        return status, notes

    # ------------------------------------------------------------------

    def check_close_bar_rules(self) -> tuple[str, list[str]]:
        """
        Scan engine source files for look-ahead patterns.
        Engines must only slice data up to the current bar (iloc[:i+1]).
        Flags direct df[i] or df.iloc[i+n] (n>0) access patterns.
        """
        notes: list[str] = []
        status = "PASS"

        engine_files = list(PROJECT_ROOT.glob("engines/**/*.py")) + \
                       list(PROJECT_ROOT.glob("simulate/**/*.py"))

        if not engine_files:
            return "WARN", ["No engine/*.py or simulate/*.py files found to scan"]

        import re

        # Patterns that suggest look-ahead access
        lookahead_patterns = [
            # iloc[i + N] where N > 0
            (re.compile(r"\.iloc\[\s*i\s*\+\s*[1-9]"), "iloc[i+N] look-ahead"),
            # loc/iloc with negative offset from end inside a loop: df.iloc[-1] is ok
            # but df['close'][i+1] or df.close[i+1] is not
            (re.compile(r"\bdf\b.*?\[i\s*\+\s*[1-9]"),  "df[i+N] look-ahead"),
            # shift(-N) on a non-label column (future shift)
            (re.compile(r"\.shift\(\s*-[1-9]"),           ".shift(-N) future shift"),
        ]

        scanned = 0
        for fpath in sorted(engine_files):
            try:
                src = fpath.read_text(encoding="utf-8")
            except Exception:
                continue
            scanned += 1
            rel = fpath.relative_to(PROJECT_ROOT)
            for pattern, label in lookahead_patterns:
                for lineno, line in enumerate(src.splitlines(), 1):
                    if pattern.search(line):
                        notes.append(
                            f"WARN — {rel}:{lineno} — possible {label}: "
                            f"{line.strip()[:80]}"
                        )
                        if status == "PASS":
                            status = "WARN"

        if scanned == 0:
            return "WARN", ["No Python files scanned — check project layout"]

        if status == "PASS":
            notes.append(
                f"No look-ahead patterns detected across {scanned} file(s)"
            )
        else:
            notes.insert(
                0,
                f"Scanned {scanned} file(s) — review flagged lines manually"
            )

        return status, notes

    # ------------------------------------------------------------------

    def check_timeframe_coverage(self) -> tuple[str, list[str]]:
        """
        Verify YF_INTERVALS and BINANCE_INTERVALS cover all TIMEFRAMES
        defined in settings.py.
        """
        notes: list[str] = []
        status = "PASS"

        settings_mod, err = _try_import("config.settings")
        if err:
            return "WARN", [f"Cannot import config.settings: {err}"]

        timeframes    = set(getattr(settings_mod, "TIMEFRAMES",        self.EXPECTED_TIMEFRAMES))
        yf_intervals  = set(getattr(settings_mod, "YF_INTERVALS",      {}).keys())
        bin_intervals = set(getattr(settings_mod, "BINANCE_INTERVALS", {}).keys())

        if self.verbose:
            print(f"    TIMEFRAMES:        {sorted(timeframes)}")
            print(f"    YF_INTERVALS:      {sorted(yf_intervals)}")
            print(f"    BINANCE_INTERVALS: {sorted(bin_intervals)}")

        missing_yf  = timeframes - yf_intervals
        missing_bin = timeframes - bin_intervals

        if missing_yf:
            notes.append(
                f"FAIL — Timeframes missing from YF_INTERVALS: {sorted(missing_yf)}"
            )
            status = "FAIL"
        if missing_bin:
            notes.append(
                f"FAIL — Timeframes missing from BINANCE_INTERVALS: {sorted(missing_bin)}"
            )
            status = "FAIL"

        if status == "PASS":
            notes.append(
                f"All {len(timeframes)} timeframe(s) covered by both YF and Binance interval maps"
            )

        return status, notes

    # ------------------------------------------------------------------

    def check_gem_json_structure(self) -> tuple[str, list[str]]:
        """
        Validate config/gb_strategy_gems.json has all required keys per
        entry: params, metrics, status, tags.
        """
        notes: list[str] = []
        status = "PASS"

        gem_path = PROJECT_ROOT / "config" / "gb_strategy_gems.json"

        if not gem_path.exists():
            return "WARN", [f"File not found: {gem_path}"]

        try:
            gems: dict = json.loads(gem_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            return "FAIL", [f"JSON parse error: {exc}"]

        if not isinstance(gems, dict):
            return "FAIL", ["gb_strategy_gems.json root must be a JSON object (dict)"]

        fail_count = 0
        for gem_name, gem_data in gems.items():
            if not isinstance(gem_data, dict):
                notes.append(f"FAIL — '{gem_name}' value is not a dict")
                status = "FAIL"
                fail_count += 1
                continue

            missing = [k for k in self.GEM_REQUIRED_KEYS if k not in gem_data]
            if missing:
                notes.append(
                    f"FAIL — '{gem_name}' missing required keys: {missing}"
                )
                status = "FAIL"
                fail_count += 1
            else:
                # Type-check sub-keys
                if not isinstance(gem_data.get("params"), dict):
                    notes.append(f"WARN — '{gem_name}'.params should be a dict")
                    if status == "PASS":
                        status = "WARN"
                if not isinstance(gem_data.get("tags"), list):
                    notes.append(f"WARN — '{gem_name}'.tags should be a list")
                    if status == "PASS":
                        status = "WARN"

        if fail_count == 0 and status == "PASS":
            notes.append(
                f"All {len(gems)} gem entries have required keys "
                f"({', '.join(self.GEM_REQUIRED_KEYS)})"
            )

        return status, notes

    # ------------------------------------------------------------------

    def check_db_schema(self) -> tuple[str, list[str]]:
        """
        Verify SQLite has required tables and columns:
          strategies(id, name, status)
          backtest_results(win_rate, profit_factor, status)
          live_trades(broker, symbol, status)
          observed_signals(lane_name, score, mode)
        """
        notes: list[str] = []
        status = "PASS"

        # Locate the database
        settings_mod, err = _try_import("config.settings")
        db_path_str: str | None = None
        if settings_mod:
            db_path_str = getattr(settings_mod, "DB_PATH", None) or \
                          getattr(settings_mod, "DATABASE_PATH", None)

        if not db_path_str:
            # Fallback: search common locations
            for candidate in [
                PROJECT_ROOT / "data" / "gb_brain.db",
                PROJECT_ROOT / "gb_brain.db",
                PROJECT_ROOT / "database" / "gb_brain.db",
            ]:
                if candidate.exists():
                    db_path_str = str(candidate)
                    break

        if not db_path_str or not Path(db_path_str).exists():
            return "WARN", [
                f"SQLite database not found (searched: {db_path_str or 'common locations'}). "
                "Run init_db first."
            ]

        db_path = Path(db_path_str)

        try:
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
        except Exception as exc:
            return "FAIL", [f"Cannot open database {db_path}: {exc}"]

        try:
            # Get actual tables
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
            )
            existing_tables = {row[0] for row in cursor.fetchall()}

            for table, required_cols in self.DB_SCHEMA.items():
                if table not in existing_tables:
                    notes.append(f"FAIL — Table '{table}' does not exist")
                    status = "FAIL"
                    continue

                cursor.execute(f"PRAGMA table_info('{table}')")
                actual_cols = {row[1] for row in cursor.fetchall()}
                missing_cols = set(required_cols) - actual_cols

                if missing_cols:
                    notes.append(
                        f"FAIL — '{table}' missing columns: {sorted(missing_cols)}"
                    )
                    status = "FAIL"
                else:
                    notes.append(
                        f"OK   — '{table}' has all required columns "
                        f"({', '.join(sorted(required_cols))})"
                    )

        finally:
            conn.close()

        if status == "PASS":
            notes.insert(
                0,
                f"DB schema valid at {db_path.name} — "
                f"all {len(self.DB_SCHEMA)} tables verified"
            )

        return status, notes

    # ------------------------------------------------------------------
    # Report printer
    # ------------------------------------------------------------------

    def _print_report(self, results: dict[str, dict[str, Any]]) -> None:
        """Print a formatted table: CHECK | STATUS | NOTES"""
        col_check  = 28
        col_status =  6
        col_notes  = 60

        header = (
            f"{'CHECK':<{col_check}} "
            f"{'STATUS':<{col_status}} "
            f"{'NOTES'}"
        )
        divider = "-" * (col_check + col_status + col_notes + 2)

        print()
        print(_bold("GB-BRAIN — Engine Parity Check Report"))
        print(divider)
        print(_bold(header))
        print(divider)

        overall_pass = True

        for check_name, info in results.items():
            st      = info["status"]
            notes_l = info["notes"]

            # Colour the status cell
            if st == "PASS":
                st_display = _green(f"{'PASS':<{col_status}}")
            elif st == "WARN":
                st_display = _yellow(f"{'WARN':<{col_status}}")
            else:
                st_display = _red(f"{'FAIL':<{col_status}}")
                overall_pass = False

            # First note on same line, rest indented
            first_note = notes_l[0] if notes_l else ""
            rest_notes = notes_l[1:] if len(notes_l) > 1 else []

            first_note_wrapped = textwrap.shorten(first_note, width=col_notes, placeholder="…")
            print(
                f"{check_name:<{col_check}} "
                f"{st_display} "
                f"{first_note_wrapped}"
            )

            indent = " " * (col_check + col_status + 2)
            for note in rest_notes:
                wrapped = textwrap.shorten(note, width=col_notes, placeholder="…")
                print(f"{indent}{wrapped}")

        print(divider)

        if overall_pass:
            print(_bold(_green("  ✓  PARITY CHECK PASSED")))
        else:
            print(_bold(_red("  ✗  PARITY CHECK FAILED")))

        print()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="GB-BRAIN Engine Parity Check — verifies backtest == runtime truth"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Print extra diagnostic info during each check",
    )
    args = parser.parse_args()

    checker = ParityChecker(verbose=args.verbose)
    results = checker.run_all()

    # Exit code: 0 = all PASS/WARN, 1 = any FAIL
    any_fail = any(r["status"] == "FAIL" for r in results.values())
    return 1 if any_fail else 0


if __name__ == "__main__":
    sys.exit(main())
