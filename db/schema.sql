-- ══════════════════════════════════════════════
-- GB-BRAIN Database Schema
-- SQLite is truth. Everything flows through here.
-- Phase 1 adds signal honesty + weekly calibration tables.
-- ══════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS strategies (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT UNIQUE NOT NULL,
    source_file     TEXT,
    source_repo     TEXT,
    category        TEXT,
    indicators      TEXT,
    entry_logic     TEXT,
    exit_logic      TEXT,
    parameters      TEXT,
    logic_hash      TEXT,
    status          TEXT DEFAULT 'pending',
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at      TEXT
);

CREATE INDEX IF NOT EXISTS idx_strategies_status ON strategies(status);
CREATE INDEX IF NOT EXISTS idx_strategies_hash ON strategies(logic_hash);

CREATE TABLE IF NOT EXISTS backtest_results (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    strategy_id     INTEGER NOT NULL,
    symbol          TEXT NOT NULL,
    timeframe       TEXT NOT NULL,
    data_source     TEXT,
    start_date      TEXT,
    end_date        TEXT,
    total_trades    INTEGER,
    wins            INTEGER,
    losses          INTEGER,
    win_rate        REAL,
    total_return    REAL,
    max_drawdown    REAL,
    profit_factor   REAL,
    sharpe_ratio    REAL,
    avg_rr          REAL,
    composite_score REAL,
    status          TEXT,
    run_at          TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY(strategy_id) REFERENCES strategies(id)
);

CREATE INDEX IF NOT EXISTS idx_bt_strategy ON backtest_results(strategy_id);
CREATE INDEX IF NOT EXISTS idx_bt_status ON backtest_results(status);
CREATE INDEX IF NOT EXISTS idx_bt_score ON backtest_results(composite_score);

CREATE TABLE IF NOT EXISTS live_trades (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    strategy_id     INTEGER,
    bot_id          INTEGER,
    broker          TEXT NOT NULL,
    symbol          TEXT NOT NULL,
    side            TEXT NOT NULL,
    units           REAL,
    entry_price     REAL,
    exit_price      REAL,
    stop_loss       REAL,
    take_profit     REAL,
    pnl             REAL,
    pnl_pct         REAL,
    fees            REAL DEFAULT 0,
    status          TEXT DEFAULT 'open',
    opened_at       TEXT,
    closed_at       TEXT,
    FOREIGN KEY(strategy_id) REFERENCES strategies(id),
    FOREIGN KEY(bot_id) REFERENCES bots(id)
);

CREATE INDEX IF NOT EXISTS idx_trades_status ON live_trades(status);
CREATE INDEX IF NOT EXISTS idx_trades_bot ON live_trades(bot_id);

CREATE TABLE IF NOT EXISTS bots (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT UNIQUE NOT NULL,
    strategy_id     INTEGER NOT NULL,
    broker          TEXT NOT NULL,
    symbol          TEXT NOT NULL,
    timeframe       TEXT NOT NULL,
    leverage        REAL DEFAULT 1,
    max_position    REAL,
    stop_loss_pct   REAL,
    take_profit_pct REAL,
    is_active       INTEGER DEFAULT 0,
    is_paper        INTEGER DEFAULT 1,
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at      TEXT,
    FOREIGN KEY(strategy_id) REFERENCES strategies(id)
);

CREATE TABLE IF NOT EXISTS harvest_log (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    repo_full_name  TEXT NOT NULL,
    file_path       TEXT NOT NULL,
    file_hash       TEXT,
    downloaded_at   TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE(repo_full_name, file_path)
);

CREATE INDEX IF NOT EXISTS idx_harvest_repo ON harvest_log(repo_full_name);

CREATE TABLE IF NOT EXISTS daily_pnl (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    bot_id           INTEGER,
    date             TEXT NOT NULL,
    broker           TEXT NOT NULL,
    starting_balance REAL,
    ending_balance   REAL,
    realized_pnl     REAL,
    unrealized_pnl   REAL,
    trade_count      INTEGER DEFAULT 0,
    recorded_at      TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY(bot_id) REFERENCES bots(id)
);

-- ══════════════════════════════════════════════
-- Phase 1 live-observer truth tables
-- ══════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS signal_candidates (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    bot_name            TEXT NOT NULL,
    strategy_family     TEXT NOT NULL,
    symbol              TEXT NOT NULL,
    timeframe           TEXT NOT NULL,
    broker              TEXT NOT NULL,
    bar_timestamp       TEXT NOT NULL,
    observed_at         TEXT NOT NULL DEFAULT (datetime('now')),
    direction           INTEGER NOT NULL,
    entry_price         REAL,
    stop_loss           REAL,
    tp1                 REAL,
    tp2                 REAL,
    tp3                 REAL,
    score               REAL,
    source              TEXT,
    reason              TEXT,
    preset_version      TEXT,
    status              TEXT NOT NULL DEFAULT 'candidate',
    payload_json        TEXT
);

CREATE INDEX IF NOT EXISTS idx_sigcand_lookup
    ON signal_candidates(bot_name, strategy_family, symbol, timeframe, broker, bar_timestamp);
CREATE INDEX IF NOT EXISTS idx_sigcand_status ON signal_candidates(status);

CREATE TABLE IF NOT EXISTS signal_confirmations (
    id                       INTEGER PRIMARY KEY AUTOINCREMENT,
    candidate_id             INTEGER NOT NULL,
    confirmed_at             TEXT NOT NULL DEFAULT (datetime('now')),
    confirmation_bar_ts      TEXT,
    is_confirmed             INTEGER NOT NULL DEFAULT 1,
    invalidation_reason      TEXT,
    payload_json             TEXT,
    FOREIGN KEY(candidate_id) REFERENCES signal_candidates(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_sigconf_candidate ON signal_confirmations(candidate_id);
CREATE INDEX IF NOT EXISTS idx_sigconf_flag ON signal_confirmations(is_confirmed);

CREATE TABLE IF NOT EXISTS trade_executions (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    candidate_id        INTEGER,
    confirmation_id     INTEGER,
    bot_name            TEXT NOT NULL,
    execution_mode      TEXT NOT NULL,
    broker              TEXT NOT NULL,
    symbol              TEXT NOT NULL,
    timeframe           TEXT NOT NULL,
    side                TEXT NOT NULL,
    units               REAL,
    leverage            REAL DEFAULT 1,
    entry_price         REAL,
    exit_price          REAL,
    stop_loss           REAL,
    take_profit         REAL,
    fees                REAL DEFAULT 0,
    pnl                 REAL,
    pnl_pct             REAL,
    status              TEXT NOT NULL DEFAULT 'open',
    opened_at           TEXT NOT NULL DEFAULT (datetime('now')),
    closed_at           TEXT,
    payload_json        TEXT,
    FOREIGN KEY(candidate_id) REFERENCES signal_candidates(id),
    FOREIGN KEY(confirmation_id) REFERENCES signal_confirmations(id)
);

CREATE INDEX IF NOT EXISTS idx_tradeexec_status ON trade_executions(status);
CREATE INDEX IF NOT EXISTS idx_tradeexec_lookup
    ON trade_executions(bot_name, symbol, timeframe, broker, opened_at);

CREATE TABLE IF NOT EXISTS weekly_calibration (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    window_start        TEXT NOT NULL,
    window_end          TEXT NOT NULL,
    bot_name            TEXT NOT NULL,
    strategy_family     TEXT NOT NULL,
    symbol              TEXT NOT NULL,
    timeframe           TEXT NOT NULL,
    broker              TEXT NOT NULL,
    candidate_count     INTEGER NOT NULL DEFAULT 0,
    confirmed_count     INTEGER NOT NULL DEFAULT 0,
    invalidated_count   INTEGER NOT NULL DEFAULT 0,
    executed_count      INTEGER NOT NULL DEFAULT 0,
    win_count           INTEGER NOT NULL DEFAULT 0,
    loss_count          INTEGER NOT NULL DEFAULT 0,
    honesty_ratio       REAL NOT NULL DEFAULT 0,
    execution_ratio     REAL NOT NULL DEFAULT 0,
    live_precision      REAL NOT NULL DEFAULT 0,
    avg_score           REAL,
    action              TEXT,
    notes               TEXT,
    created_at          TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE(window_start, window_end, bot_name, strategy_family, symbol, timeframe, broker)
);

CREATE INDEX IF NOT EXISTS idx_weekcal_lookup
    ON weekly_calibration(bot_name, strategy_family, symbol, timeframe, broker, window_end);
