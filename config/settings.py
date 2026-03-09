"""
GB-BRAIN — Central Settings
============================
All configuration in one file. Uses .env for secrets.
Cross-platform paths (Windows + Linux VPS).
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# ── Load .env from project root ──────────────
ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")

# ── Database ─────────────────────────────────
DB_PATH = ROOT_DIR / "db" / "gb_brain.db"

# ── Directories ──────────────────────────────
STAGING_DIR    = ROOT_DIR / "strategies" / "staging"
BEST_DIR       = ROOT_DIR / "strategies" / "best"
ARCHIVE_DIR    = ROOT_DIR / "strategies" / "archive" / "trash"
CUSTOM_DIR     = ROOT_DIR / "strategies" / "custom"
DATA_CACHE_DIR = ROOT_DIR / "backtest" / "data_cache"

# ── API Keys (from .env) ─────────────────────
GITHUB_TOKEN    = os.getenv("GITHUB_TOKEN", "")
BINANCE_KEY     = os.getenv("BINANCE_API_KEY", "")
BINANCE_SECRET  = os.getenv("BINANCE_API_SECRET", "")
ALPACA_KEY      = os.getenv("ALPACA_API_KEY", "")
ALPACA_SECRET   = os.getenv("ALPACA_API_SECRET", "")
ALPACA_BASE_URL = os.getenv("ALPACA_BASE_URL", "https://paper-api.alpaca.markets")
OANDA_ACCOUNT   = os.getenv("OANDA_ACCOUNT_ID", "")
OANDA_TOKEN     = os.getenv("OANDA_API_TOKEN", "")
OANDA_URL       = os.getenv("OANDA_API_URL", "https://api-fxpractice.oanda.com")
BLOFIN_KEY      = os.getenv("BLOFIN_API_KEY", "")
BLOFIN_SECRET   = os.getenv("BLOFIN_API_SECRET", "")
BLOFIN_PASS     = os.getenv("BLOFIN_PASSPHRASE", "")
TELEGRAM_TOKEN  = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT   = os.getenv("TELEGRAM_CHAT_ID", "")
TV_SECRET       = os.getenv("TV_WEBHOOK_SECRET", "")
TV_PORT         = int(os.getenv("TV_WEBHOOK_PORT", "5000"))

# ── Tickers ──────────────────────────────────
CRYPTO_TICKERS = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]
INDEX_TICKERS  = ["^NDX", "^DJI", "^GSPC"]  # NAS100, US30, SPX500

# Friendly names for display / reports
TICKER_NAMES = {
    "BTCUSDT": "BTC",
    "ETHUSDT": "ETH",
    "SOLUSDT": "SOL",
    "^NDX":    "NAS100",
    "^DJI":    "US30",
    "^GSPC":   "SPX500",
}

ALL_TICKERS = CRYPTO_TICKERS + INDEX_TICKERS

# ── Timeframes ───────────────────────────────
TIMEFRAMES = ["5m", "15m", "1h"]

# Yahoo Finance interval mapping
YF_INTERVALS = {
    "1m":  {"interval": "1m",  "period": "7d"},
    "5m":  {"interval": "5m",  "period": "60d"},
    "15m": {"interval": "15m", "period": "60d"},
    "30m": {"interval": "30m", "period": "60d"},
    "1h":  {"interval": "1h",  "period": "730d"},
}

# Binance interval mapping
BINANCE_INTERVALS = {
    "1m":  "1m",
    "5m":  "5m",
    "15m": "15m",
    "30m": "30m",
    "1h":  "1h",
}

# ── Backtest Settings ────────────────────────
BACKTEST_CASH       = 10_000    # Starting capital for backtests
BACKTEST_COMMISSION = 0.001     # 0.1% per trade
MIN_TRADES          = 30        # Ignore strategies with fewer trades

# ── Scoring Thresholds ───────────────────────
GEM_WIN_RATE   = 55.0    # Win rate >= 55% AND positive returns = GEM
PASS_WIN_RATE  = 40.0    # Win rate >= 40% = PASS (mediocre)
                          # Below 40% = TRASH

# Composite score weights
SCORE_WEIGHTS = {
    "win_rate":      0.35,
    "total_return":  0.30,
    "profit_factor": 0.20,
    "trade_count":   0.15,
}

# ── Risk Management ──────────────────────────
MAX_DAILY_LOSS_PCT  = 0.10   # Stop trading if 10% daily loss
MAX_DRAWDOWN_PCT    = 0.25   # Hard stop at 25% drawdown
MAX_POSITION_PCT    = 0.50   # Max 50% of balance per position
COOLDOWN_SECONDS    = 300    # 5 min cooldown after loss

# ── Harvester Settings ───────────────────────
HARVEST_MAX_DEPTH   = 3      # Max folder depth when scanning repos
HARVEST_RATE_SLEEP  = 3      # Seconds between GitHub API queries
HARVEST_FILE_SLEEP  = 0.3    # Seconds between file downloads

# ── Logging ──────────────────────────────────
LOG_LEVEL = "INFO"
LOG_FILE  = ROOT_DIR / "gb_brain.log"

# ── Ensure directories exist ─────────────────
# Ticker-specific folders for GEMs
TICKER_FOLDERS = ["btc", "eth", "sol", "nas100", "us30", "spx"]

for d in [STAGING_DIR, ARCHIVE_DIR, CUSTOM_DIR, DATA_CACHE_DIR, DB_PATH.parent]:
    d.mkdir(parents=True, exist_ok=True)
for tf in TICKER_FOLDERS:
    (BEST_DIR / tf).mkdir(parents=True, exist_ok=True)
