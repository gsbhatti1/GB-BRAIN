-- ══════════════════════════════════════════════
-- GB-BRAIN Database Schema
-- SQLite is truth. Everything flows through here.
-- ══════════════════════════════════════════════

-- strategies: Every strategy ever discovered
CREATE TABLE IF NOT EXISTS strategies (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT UNIQUE NOT NULL,
    source_file     TEXT,
    source_repo     TEXT,
    category        TEXT,                              -- crypto | indices | custom
    indicators      TEXT,                              -- JSON: ["EMA","RSI","MACD"]
    entry_logic     TEXT,                              -- Human-readable entry conditions
    exit_logic      TEXT,                              -- Human-readable exit conditions
    parameters      TEXT,                              -- JSON: {"ema_fast":9,"rsi_period":14}
    logic_hash      TEXT,                              -- SHA256 of logic for dedup
    status          TEXT DEFAULT 'pending',            -- pending | tested | gem | pass | trash
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at      TEXT
);

CREATE INDEX IF NOT EXISTS idx_strategies_status ON strategies(status);
CREATE INDEX IF NOT EXISTS idx_strategies_hash ON strategies(logic_hash);

-- backtest_results: Every backtest ever run
CREATE TABLE IF NOT EXISTS backtest_results (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    strategy_id     INTEGER NOT NULL,
    symbol          TEXT NOT NULL,
    timeframe       TEXT NOT NULL,
    data_source     TEXT,                              -- yahoo | binance | alpaca
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
    status          TEXT,                              -- GEM | PASS | TRASH
    run_at          TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY(strategy_id) REFERENCES strategies(id)
);

CREATE INDEX IF NOT EXISTS idx_bt_strategy ON backtest_results(strategy_id);
CREATE INDEX IF NOT EXISTS idx_bt_status ON backtest_results(status);
CREATE INDEX IF NOT EXISTS idx_bt_score ON backtest_results(composite_score);

-- live_trades: Every trade executed by bots
CREATE TABLE IF NOT EXISTS live_trades (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    strategy_id     INTEGER,
    bot_id          INTEGER,
    broker          TEXT NOT NULL,                     -- oanda | blofin | binance | alpaca
    symbol          TEXT NOT NULL,
    side            TEXT NOT NULL,                     -- buy | sell
    units           REAL,
    entry_price     REAL,
    exit_price      REAL,
    stop_loss       REAL,
    take_profit     REAL,
    pnl             REAL,
    pnl_pct         REAL,
    fees            REAL DEFAULT 0,
    status          TEXT DEFAULT 'open',               -- open | closed | cancelled
    opened_at       TEXT,
    closed_at       TEXT,
    FOREIGN KEY(strategy_id) REFERENCES strategies(id),
    FOREIGN KEY(bot_id) REFERENCES bots(id)
);

CREATE INDEX IF NOT EXISTS idx_trades_status ON live_trades(status);
CREATE INDEX IF NOT EXISTS idx_trades_bot ON live_trades(bot_id);

-- bots: Active bot configurations
CREATE TABLE IF NOT EXISTS bots (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT UNIQUE NOT NULL,
    strategy_id     INTEGER NOT NULL,
    broker          TEXT NOT NULL,                     -- oanda | blofin | binance | alpaca
    symbol          TEXT NOT NULL,
    timeframe       TEXT NOT NULL,
    leverage        REAL DEFAULT 1,
    max_position    REAL,
    stop_loss_pct   REAL,
    take_profit_pct REAL,
    is_active       INTEGER DEFAULT 0,                 -- 0 = paused, 1 = running
    is_paper        INTEGER DEFAULT 1,                 -- 1 = demo, 0 = live
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at      TEXT,
    FOREIGN KEY(strategy_id) REFERENCES strategies(id)
);

-- harvest_log: Track what we've already harvested (dedup)
CREATE TABLE IF NOT EXISTS harvest_log (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    repo_full_name  TEXT NOT NULL,                     -- e.g. "user/repo"
    file_path       TEXT NOT NULL,
    file_hash       TEXT,                              -- SHA256 of content
    downloaded_at   TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE(repo_full_name, file_path)
);

CREATE INDEX IF NOT EXISTS idx_harvest_repo ON harvest_log(repo_full_name);

-- daily_pnl: Daily P&L snapshots for monitoring
CREATE TABLE IF NOT EXISTS daily_pnl (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    bot_id          INTEGER,
    date            TEXT NOT NULL,
    broker          TEXT NOT NULL,
    starting_balance REAL,
    ending_balance  REAL,
    realized_pnl    REAL,
    unrealized_pnl  REAL,
    trade_count     INTEGER DEFAULT 0,
    recorded_at     TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY(bot_id) REFERENCES bots(id)
);
