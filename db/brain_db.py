"""
GB-BRAIN — Database Layer
==========================
SQLite is truth. All reads/writes go through here.
"""

import sys
import sqlite3
from pathlib import Path

# Ensure project root is on sys.path
_THIS_DIR = Path(__file__).resolve().parent
_ROOT = _THIS_DIR.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

_SCHEMA_PATH = _THIS_DIR / "schema.sql"


def get_db_path():
    """Import settings lazily to avoid circular imports."""
    from config.settings import DB_PATH
    return DB_PATH


def connect(db_path=None):
    """Get a connection with WAL mode and foreign keys enabled."""
    path = db_path or get_db_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path))
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path=None):
    """Create all tables from schema.sql."""
    path = db_path or get_db_path()
    schema = _SCHEMA_PATH.read_text(encoding="utf-8")
    conn = connect(path)
    try:
        conn.executescript(schema)
        conn.commit()
        print(f"[OK] Database ready: {path}")
    finally:
        conn.close()


def insert_strategy(conn, *, name, source_file=None, source_repo=None,
                     category=None, indicators=None, entry_logic=None,
                     exit_logic=None, parameters=None, logic_hash=None):
    """Insert a strategy. Returns the id. Skips duplicates by name."""
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
        # Already existed — fetch the id
        row = conn.execute(
            "SELECT id FROM strategies WHERE name = ?", (name,)
        ).fetchone()
        return row["id"] if row else None
    except Exception as e:
        print(f"[ERROR] insert_strategy: {e}")
        return None


def insert_backtest(conn, *, strategy_id, symbol, timeframe, data_source=None,
                     start_date=None, end_date=None, total_trades=0,
                     wins=0, losses=0, win_rate=0.0, total_return=0.0,
                     max_drawdown=0.0, profit_factor=0.0, sharpe_ratio=0.0,
                     avg_rr=0.0, composite_score=0.0, status="pending"):
    """Insert a backtest result. Returns the id."""
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
    """Log a harvested file. Returns True if new, False if duplicate."""
    try:
        conn.execute(
            """INSERT OR IGNORE INTO harvest_log
               (repo_full_name, file_path, file_hash)
               VALUES (?, ?, ?)""",
            (repo_full_name, file_path, file_hash),
        )
        conn.commit()
        return conn.total_changes > 0
    except Exception:
        return False


def is_harvested(conn, repo_full_name, file_path):
    """Check if a file was already harvested."""
    row = conn.execute(
        "SELECT 1 FROM harvest_log WHERE repo_full_name = ? AND file_path = ?",
        (repo_full_name, file_path),
    ).fetchone()
    return row is not None


def get_strategies_by_status(conn, status):
    """Get all strategies with a given status."""
    return conn.execute(
        "SELECT * FROM strategies WHERE status = ?", (status,)
    ).fetchall()


def get_top_backtests(conn, min_trades=30, limit=50):
    """Get top backtest results by composite score."""
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
    """Update strategy status (pending/tested/gem/pass/trash)."""
    conn.execute(
        "UPDATE strategies SET status = ?, updated_at = datetime('now') WHERE id = ?",
        (status, strategy_id),
    )
    conn.commit()


def get_stats(conn):
    """Quick stats for dashboard."""
    stats = {}
    stats["total_strategies"] = conn.execute(
        "SELECT COUNT(*) FROM strategies"
    ).fetchone()[0]
    stats["pending"] = conn.execute(
        "SELECT COUNT(*) FROM strategies WHERE status = 'pending'"
    ).fetchone()[0]
    stats["tested"] = conn.execute(
        "SELECT COUNT(*) FROM strategies WHERE status = 'tested'"
    ).fetchone()[0]
    stats["gems"] = conn.execute(
        "SELECT COUNT(*) FROM strategies WHERE status = 'gem'"
    ).fetchone()[0]
    stats["trash"] = conn.execute(
        "SELECT COUNT(*) FROM strategies WHERE status = 'trash'"
    ).fetchone()[0]
    stats["total_backtests"] = conn.execute(
        "SELECT COUNT(*) FROM backtest_results"
    ).fetchone()[0]
    stats["total_harvested"] = conn.execute(
        "SELECT COUNT(*) FROM harvest_log"
    ).fetchone()[0]
    return stats


# ── Run directly to initialize ───────────────
if __name__ == "__main__":
    init_db()
