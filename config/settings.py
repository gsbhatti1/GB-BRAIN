"""
GB-BRAIN — Central Settings
============================
All configuration in one file. Uses .env for secrets.
Cross-platform paths (Windows + Linux VPS).
"""

import os
from pathlib import Path
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")

# ── Database ─────────────────────────────────
DB_PATH = ROOT_DIR / "db" / "gb_brain.db"

# ── Directories ──────────────────────────────
STAGING_DIR = ROOT_DIR / "strategies" / "staging"
BEST_DIR = ROOT_DIR / "strategies" / "best"
ARCHIVE_DIR = ROOT_DIR / "strategies" / "archive" / "trash"
CUSTOM_DIR = ROOT_DIR / "strategies" / "custom"
DATA_CACHE_DIR = ROOT_DIR / "backtest" / "data_cache"
CONFIG_DIR = ROOT_DIR / "config"
DOCS_DIR = ROOT_DIR
GEMS_CONFIG_PATH = CONFIG_DIR / "gb_strategy_gems.json"
SYMBOL_REGISTRY_PATH = CONFIG_DIR / "symbol_registry.json"

# ── API Keys (from .env) ─────────────────────
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
BINANCE_KEY = os.getenv("BINANCE_API_KEY", "")
BINANCE_SECRET = os.getenv("BINANCE_API_SECRET", "")
ALPACA_KEY = os.getenv("ALPACA_API_KEY", "")
ALPACA_SECRET = os.getenv("ALPACA_API_SECRET", "")
ALPACA_BASE_URL = os.getenv("ALPACA_BASE_URL", "https://paper-api.alpaca.markets")
OANDA_ACCOUNT = os.getenv("OANDA_ACCOUNT_ID", "")
OANDA_TOKEN = os.getenv("OANDA_API_TOKEN", "")
OANDA_URL = os.getenv("OANDA_API_URL", "https://api-fxpractice.oanda.com")
BLOFIN_KEY = os.getenv("BLOFIN_API_KEY", "")
BLOFIN_SECRET = os.getenv("BLOFIN_API_SECRET", "")
BLOFIN_PASS = os.getenv("BLOFIN_PASSPHRASE", "")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT = os.getenv("TELEGRAM_CHAT_ID", "")
TV_SECRET = os.getenv("TV_WEBHOOK_SECRET", "")
TV_PORT = int(os.getenv("TV_WEBHOOK_PORT", "5000"))

# ── Tickers ──────────────────────────────────
CRYPTO_TICKERS = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]
INDEX_TICKERS = ["^NDX", "^DJI", "^GSPC"]

TICKER_NAMES = {
    "BTCUSDT": "BTC",
    "ETHUSDT": "ETH",
    "SOLUSDT": "SOL",
    "^NDX": "NAS100",
    "^DJI": "US30",
    "^GSPC": "SPX500",
}
ALL_TICKERS = CRYPTO_TICKERS + INDEX_TICKERS

# ── Timeframes ───────────────────────────────
TIMEFRAMES = ["5m", "15m", "30m", "1h"]

YF_INTERVALS = {
    "1m": {"interval": "1m", "period": "7d"},
    "5m": {"interval": "5m", "period": "60d"},
    "15m": {"interval": "15m", "period": "60d"},
    "30m": {"interval": "30m", "period": "60d"},
    "1h": {"interval": "1h", "period": "730d"},
}

BINANCE_INTERVALS = {
    "1m": "1m",
    "5m": "5m",
    "15m": "15m",
    "30m": "30m",
    "1h": "1h",
}

# ── Backtest Settings ────────────────────────
BACKTEST_CASH = 10_000
BACKTEST_COMMISSION = 0.001
MIN_TRADES = 30

# ── Scoring Thresholds ───────────────────────
GEM_WIN_RATE = 55.0
PASS_WIN_RATE = 40.0
SCORE_WEIGHTS = {
    "win_rate": 0.35,
    "total_return": 0.30,
    "profit_factor": 0.20,
    "trade_count": 0.15,
}

# ── Risk Management ──────────────────────────
MAX_DAILY_LOSS_PCT = 0.10
MAX_DRAWDOWN_PCT = 0.25
MAX_POSITION_PCT = 0.10
COOLDOWN_SECONDS = 900

# ── Runtime Identity ─────────────────────────
BOT_NAMES = ["GB-CRYPTO-BOT", "GB-INDICES", "MANUAL-SIGNALS"]
LIVE_OBSERVER_DEFAULT_DAYS = 7
