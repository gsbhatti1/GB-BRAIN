# FULL NEW CONTENT FOR 3_backtest_engine.py

import os
import json
import warnings
from datetime import datetime
from pathlib import Path

import importlib.util
import pandas as pd
import ta
import sqlite3
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

warnings.filterwarnings("ignore")


def load_config():
    spec = importlib.util.spec_from_file_location(
        "config",
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "0_config.py"),
    )
    cfg = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cfg)
    return cfg


cfg = load_config()

CACHE = os.path.join(cfg.RESULTS_DIR, "data_cache")
DB_PATH = Path(__file__).resolve().parent / "db" / "strategies.db"


class RSIStrat(Strategy):
    rsi_p = 14

    def init(self):
        self.rsi = self.I(
            lambda x: ta.momentum.RSIIndicator(pd.Series(x), self.rsi_p)
            .rsi()
            .values,
            self.data.Close,
        )

    def next(self):
        if self.rsi[-1] < 30:
            self.buy()
        elif self.rsi[-1] > 70 and self.position:
            self.position.close()


class MACross(Strategy):
    fast = 10
    slow = 20

    def init(self):
        self.fma = self.I(
            lambda x: pd.Series(x).rolling(self.fast).mean().values, self.data.Close
        )
        self.sma = self.I(
            lambda x: pd.Series(x).rolling(self.slow).mean().values, self.data.Close
        )

    def next(self):
        if crossover(self.fma, self.sma):
            self.buy()
        elif crossover(self.sma, self.fma) and self.position:
            self.position.close()


class MACDStrat(Strategy):
    def init(self):
        c = pd.Series(self.data.Close)
        m = ta.trend.MACD(c)
        self.macd = self.I(lambda: m.macd().values)
        self.signal = self.I(lambda: m.macd_signal().values)

    def next(self):
        if crossover(self.macd, self.signal):
            self.buy()
        elif crossover(self.signal, self.macd) and self.position:
            self.position.close()


class BBStrat(Strategy):
    def init(self):
        c = pd.Series(self.data.Close)
        b = ta.volatility.BollingerBands(c)
        self.upper = self.I(lambda: b.bollinger_hband().values)
        self.lower = self.I(lambda: b.bollinger_lband().values)

    def next(self):
        if self.data.Close[-1] < self.lower[-1]:
            self.buy()
        elif self.data.Close[-1] > self.upper[-1] and self.position:
            self.position.close()


STRAT_MAP = {
    "RSI": RSIStrat,
    "MACD": MACDStrat,
    "BB": BBStrat,
    "EMA": MACross,
    "MA": MACross,
    "GENERIC": MACross,
    "STOCH": RSIStrat,
}


def stars(w):
    return 5 if w >= 80 else 4 if w >= 60 else 3 if w >= 40 else 2 if w >= 20 else 1


ALL_TICKERS = cfg.CRYPTO_TICKERS + list(cfg.STOCK_TICKERS)


def ensure_db_schema() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS strategies (
                id INTEGER PRIMARY KEY,
                strategy_name TEXT UNIQUE,
                source_file TEXT,
                logic_hash TEXT,
                created_at TEXT
            );

            CREATE TABLE IF NOT EXISTS backtest_results (
                id INTEGER PRIMARY KEY,
                strategy_id INTEGER,
                run_timestamp TEXT,
                timeframe TEXT,
                symbol TEXT,
                total_trades INTEGER,
                win_rate REAL,
                total_return REAL,
                max_dd REAL,
                profit_factor REAL,
                status TEXT,
                composite_score REAL,
                FOREIGN KEY(strategy_id) REFERENCES strategies(id)
            );
            """
        )
        conn.commit()
    finally:
        conn.close()


def save_result_to_db(rec: dict) -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.cursor()

        cur.execute(
            """
            INSERT OR IGNORE INTO strategies (
                strategy_name, source_file, logic_hash, created_at
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                rec["strategy"],
                rec.get("source_file", "unknown"),
                rec.get("logic_hash"),
                datetime.utcnow().isoformat(),
            ),
        )

        cur.execute(
            "SELECT id FROM strategies WHERE strategy_name = ?",
            (rec["strategy"],),
        )
        row = cur.fetchone()
        if row is None:
            raise RuntimeError(f"Strategy not found after insert: {rec['strategy']}")
        strategy_id = row[0]

        cur.execute(
            """
            INSERT INTO backtest_results (
                strategy_id,
                run_timestamp,
                timeframe,
                symbol,
                total_trades,
                win_rate,
                total_return,
                max_dd,
                profit_factor,
                status,
                composite_score
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                strategy_id,
                datetime.utcnow().isoformat(),
                rec["timeframe"],
                rec["ticker"],
                rec["trades"],
                rec["win_rate"],
                rec["return_pct"],
                None,
                None,
                "pending_score",
                None,
            ),
        )

        conn.commit()
    finally:
        conn.close()


def run_bt(s, ticker, tf):
    path = os.path.join(CACHE, f"{ticker}_{tf}.csv")
    if not os.path.exists(path):
        return None
    df = pd.read_csv(path, index_col=0, parse_dates=True)
    df.columns = [c.capitalize() for c in df.columns]
    df = df.dropna()
    if len(df) < 100:
        return None
    try:
        bt = Backtest(
            df,
            STRAT_MAP.get(s["type"], MACross),
            cash=10000,
            commission=0.001,
        )
        st = bt.run()
        if st["# Trades"] < cfg.MIN_TRADES:
            return None
        return {
            "strategy": s["name"],
            "ticker": ticker,
            "timeframe": tf,
            "win_rate": round(st["Win Rate [%]"], 2),
            "return_pct": round(st["Return [%]"], 2),
            "trades": st["# Trades"],
            "stars": stars(st["Win Rate [%]"]),
            "type": s["type"],
        }
    except Exception:
        return None


def main() -> None:
    ensure_db_schema()

    with open(os.path.join(cfg.RESULTS_DIR, "strategy_registry.json")) as f:
        strats = json.load(f)

    results = []
    done = 0
    total = len(strats) * len(ALL_TICKERS) * len(cfg.TIMEFRAMES)
    print(f"\nRunning {total:,} backtests...\n")
    for s in strats:
        for ticker in ALL_TICKERS:
            for tf in cfg.TIMEFRAMES:
                r = run_bt(s, ticker, tf)
                if r:
                    results.append(r)
                    save_result_to_db(r)
                done += 1
                if done % 5000 == 0:
                    print(
                        f"  {done:,}/{total:,} ({round(done/total*100,1)}%) | hits: {len(results):,}"
                    )

    out_path = os.path.join(cfg.RESULTS_DIR, "raw_results.csv")
    pd.DataFrame(results).to_csv(out_path, index=False)
    print(f"\nDone! {len(results):,} valid results saved to {out_path}\n")


if __name__ == "__main__":
    main()
