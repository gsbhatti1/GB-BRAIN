"""
GB-BRAIN — Database Layer
==========================
SQLite is truth. All reads/writes go through here.
Phase 1 adds helper methods for signal honesty tracking.
"""

import sys
import json
import sqlite3
from pathlib import Path
from typing import Any, Mapping

_THIS_DIR = Path(__file__).resolve().parent
_ROOT = _THIS_DIR.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

_SCHEMA_PATH = _THIS_DIR / "schema.sql"


def get_db_path():
    from config.settings import DB_PATH
    return DB_PATH


def connect(db_path=None):
    path = db_path or get_db_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path))
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path=None):
    path = db_path or get_db_path()
    schema = _SCHEMA_PATH.read_text(encoding="utf-8")
    conn = connect(path)
    try:
        conn.executescript(schema)
        conn.commit()
        print(f"[OK] Database ready: {path}")
    finally:
        conn.close()


def _to_json(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def insert_strategy(conn, *, name, source_file=None, source_repo=None,
                    category=None, indicators=None, entry_logic=None,
                    exit_logic=None, parameters=None, logic_hash=None):
    try:
        cur = conn.execute(
            """INSERT OR IGNORE INTO strategies
               (name, source_file, source_repo, category,
                indicators, entry_logic, exit_logic, parameters, logic_hash)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (name, source_file, source_repo, category,
             indicators, entry_logic, exit_logic, parameters, logic_hash),
        )
        conn.commit()
        if cur.lastrowid:
            return cur.lastrowid
        row = conn.execute("SELECT id FROM strategies WHERE name = ?", (name,)).fetchone()
        return row["id"] if row else None
    except Exception as exc:
        print(f"[ERROR] insert_strategy: {exc}")
        return None


def insert_backtest(conn, *, strategy_id, symbol, timeframe, data_source=None,
                    start_date=None, end_date=None, total_trades=0,
                    wins=0, losses=0, win_rate=0.0, total_return=0.0,
                    max_drawdown=0.0, profit_factor=0.0, sharpe_ratio=0.0,
                    avg_rr=0.0, composite_score=0.0, status="pending"):
    cur = conn.execute(
        """INSERT INTO backtest_results
           (strategy_id, symbol, timeframe, data_source,
            start_date, end_date, total_trades, wins, losses,
            win_rate, total_return, max_drawdown, profit_factor,
            sharpe_ratio, avg_rr, composite_score, status)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (strategy_id, symbol, timeframe, data_source,
         start_date, end_date, total_trades, wins, losses,
         win_rate, total_return, max_drawdown, profit_factor,
         sharpe_ratio, avg_rr, composite_score, status),
    )
    conn.commit()
    return cur.lastrowid


def insert_harvest_log(conn, *, repo_full_name, file_path, file_hash=None):
    try:
        before = conn.total_changes
        conn.execute(
            """INSERT OR IGNORE INTO harvest_log
               (repo_full_name, file_path, file_hash)
               VALUES (?, ?, ?)""",
            (repo_full_name, file_path, file_hash),
        )
        conn.commit()
        return conn.total_changes > before
    except Exception:
        return False


def is_harvested(conn, repo_full_name, file_path):
    row = conn.execute(
        "SELECT 1 FROM harvest_log WHERE repo_full_name = ? AND file_path = ?",
        (repo_full_name, file_path),
    ).fetchone()
    return row is not None


def get_strategies_by_status(conn, status):
    return conn.execute("SELECT * FROM strategies WHERE status = ?", (status,)).fetchall()


def get_top_backtests(conn, min_trades=30, limit=50):
    return conn.execute(
        """SELECT br.*, s.name as strategy_name, s.category
           FROM backtest_results br
           JOIN strategies s ON s.id = br.strategy_id
           WHERE br.total_trades >= ?
           ORDER BY br.composite_score DESC
           LIMIT ?""",
        (min_trades, limit),
    ).fetchall()


def update_strategy_status(conn, strategy_id, status):
    conn.execute(
        "UPDATE strategies SET status = ?, updated_at = datetime('now') WHERE id = ?",
        (status, strategy_id),
    )
    conn.commit()


def insert_signal_candidate(conn, *, bot_name: str, strategy_family: str, symbol: str,
                            timeframe: str, broker: str, bar_timestamp: str,
                            direction: int, entry_price=None, stop_loss=None,
                            tp1=None, tp2=None, tp3=None, score=None, source=None,
                            reason=None, preset_version=None, status="candidate",
                            payload=None):
    cur = conn.execute(
        """INSERT INTO signal_candidates
           (bot_name, strategy_family, symbol, timeframe, broker, bar_timestamp,
            direction, entry_price, stop_loss, tp1, tp2, tp3, score, source,
            reason, preset_version, status, payload_json)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (bot_name, strategy_family, symbol, timeframe, broker, bar_timestamp,
         direction, entry_price, stop_loss, tp1, tp2, tp3, score, source,
         reason, preset_version, status, _to_json(payload)),
    )
    conn.commit()
    return cur.lastrowid


def insert_signal_confirmation(conn, *, candidate_id: int, is_confirmed: bool,
                               confirmation_bar_ts=None, invalidation_reason=None,
                               payload=None):
    cur = conn.execute(
        """INSERT INTO signal_confirmations
           (candidate_id, confirmation_bar_ts, is_confirmed, invalidation_reason, payload_json)
           VALUES (?, ?, ?, ?, ?)""",
        (candidate_id, confirmation_bar_ts, int(bool(is_confirmed)),
         invalidation_reason, _to_json(payload)),
    )
    conn.commit()
    return cur.lastrowid


def insert_trade_execution(conn, *, bot_name: str, execution_mode: str, broker: str,
                           symbol: str, timeframe: str, side: str,
                           candidate_id=None, confirmation_id=None, units=None,
                           leverage=1, entry_price=None, stop_loss=None,
                           take_profit=None, payload=None):
    cur = conn.execute(
        """INSERT INTO trade_executions
           (candidate_id, confirmation_id, bot_name, execution_mode, broker, symbol,
            timeframe, side, units, leverage, entry_price, stop_loss, take_profit, payload_json)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (candidate_id, confirmation_id, bot_name, execution_mode, broker, symbol,
         timeframe, side, units, leverage, entry_price, stop_loss, take_profit,
         _to_json(payload)),
    )
    conn.commit()
    return cur.lastrowid


def close_trade_execution(conn, *, execution_id: int, exit_price=None, fees=0.0,
                          pnl=None, pnl_pct=None, status="closed", payload=None):
    conn.execute(
        """UPDATE trade_executions
           SET exit_price = ?, fees = ?, pnl = ?, pnl_pct = ?, status = ?,
               closed_at = datetime('now'),
               payload_json = COALESCE(?, payload_json)
           WHERE id = ?""",
        (exit_price, fees, pnl, pnl_pct, status, _to_json(payload), execution_id),
    )
    conn.commit()


def insert_weekly_calibration(conn, *, window_start: str, window_end: str,
                              bot_name: str, strategy_family: str, symbol: str,
                              timeframe: str, broker: str, candidate_count=0,
                              confirmed_count=0, invalidated_count=0,
                              executed_count=0, win_count=0, loss_count=0,
                              honesty_ratio=0.0, execution_ratio=0.0,
                              live_precision=0.0, avg_score=None, action=None,
                              notes=None):
    conn.execute(
        """INSERT OR REPLACE INTO weekly_calibration
           (window_start, window_end, bot_name, strategy_family, symbol, timeframe,
            broker, candidate_count, confirmed_count, invalidated_count,
            executed_count, win_count, loss_count, honesty_ratio,
            execution_ratio, live_precision, avg_score, action, notes)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (window_start, window_end, bot_name, strategy_family, symbol, timeframe,
         broker, candidate_count, confirmed_count, invalidated_count,
         executed_count, win_count, loss_count, honesty_ratio,
         execution_ratio, live_precision, avg_score, action, notes),
    )
    conn.commit()


def get_stats(conn):
    stats = {}
    stats["total_strategies"] = conn.execute("SELECT COUNT(*) FROM strategies").fetchone()[0]
    stats["pending"] = conn.execute("SELECT COUNT(*) FROM strategies WHERE status = 'pending'").fetchone()[0]
    stats["tested"] = conn.execute("SELECT COUNT(*) FROM strategies WHERE status = 'tested'").fetchone()[0]
    stats["gems"] = conn.execute("SELECT COUNT(*) FROM strategies WHERE status = 'gem'").fetchone()[0]
    stats["trash"] = conn.execute("SELECT COUNT(*) FROM strategies WHERE status = 'trash'").fetchone()[0]
    stats["total_backtests"] = conn.execute("SELECT COUNT(*) FROM backtest_results").fetchone()[0]
    stats["total_harvested"] = conn.execute("SELECT COUNT(*) FROM harvest_log").fetchone()[0]
    stats["signal_candidates"] = conn.execute("SELECT COUNT(*) FROM signal_candidates").fetchone()[0]
    stats["signal_confirmations"] = conn.execute("SELECT COUNT(*) FROM signal_confirmations").fetchone()[0]
    stats["trade_executions"] = conn.execute("SELECT COUNT(*) FROM trade_executions").fetchone()[0]
    stats["weekly_calibration"] = conn.execute("SELECT COUNT(*) FROM weekly_calibration").fetchone()[0]
    return stats


if __name__ == "__main__":
    init_db()
