# 🧠 GB-BRAIN

**One repo. One database. One pipeline.**  
Harvest trading strategies from GitHub → Backtest on real data → Score & rank → Deploy winning bots.

## What It Does

| Step | Script | What Happens |
|------|--------|-------------|
| **Harvest** | `harvest/harvest_github.py` | Scans 70+ GitHub queries, downloads .py/.pine strategy files |
| **Extract** | `parse/extract_logic.py` | Reads each file, extracts indicators + entry/exit conditions |
| **Fetch Data** | `backtest/fetch_data.py` | Downloads OHLCV from Binance (crypto) + Yahoo (indices) |
| **Backtest** | `backtest/run_backtest.py` | Runs backtests using extracted logic, saves to SQLite |
| **Score** | `backtest/score_and_sort.py` | Composite scoring → GEM / PASS / TRASH classification |

## Quick Start

### 1. Clone & Setup

```powershell
git clone https://github.com/gsbhatti1/GB-BRAIN.git
cd GB-BRAIN
pip install -r requirements.txt
Copy-Item .env.example .env
# Edit .env with your API keys
```

### 2. Initialize Database

```powershell
.\scripts\init_db.ps1
```

### 3. Run Full Pipeline

```powershell
.\scripts\run_pipeline.ps1 -Report
```

Or run steps individually:

```powershell
.\scripts\run_harvest.ps1 -Pages 2
.\scripts\run_backtest.ps1 -Limit 100
.\scripts\run_score.ps1 -Report
```

## Folder Structure

```
GB-BRAIN/
├── harvest/          ← GitHub strategy scraper
├── parse/            ← Logic extraction
├── backtest/         ← Engine + data cache
├── strategies/
│   ├── staging/      ← Raw downloaded files
│   ├── best/         ← GEMs (60%+ win rate, positive returns)
│   │   ├── crypto/   ← BTC, ETH, SOL strategies
│   │   └── indices/  ← NAS100, US30, SPX500 strategies
│   ├── archive/      ← Tested, didn't make the cut
│   └── custom/       ← Your strategies (CIPHER, PARALLAX, ORB)
├── execute/          ← Broker bridges + risk management
├── webhook/          ← TradingView listener
├── monitor/          ← Dashboard + reports
├── db/               ← SQLite database + schema
├── config/           ← Settings + .env
└── scripts/          ← One-click PowerShell runners
```

## Tickers

| Category | Symbols |
|----------|---------|
| **GB-Crypto** | BTC-USDT, ETH-USDT, SOL-USDT |
| **GB-Indices** | NAS100 (^NDX), US30 (^DJI), SPX500 (^GSPC) |

## Brokers

| Broker | Use | Status |
|--------|-----|--------|
| OANDA | Indices (demo) | Ready |
| BloFin | Crypto futures | Ready |
| Binance | Crypto spot/futures | Ready |
| Alpaca | US stocks | Ready |

## Rules

- **SQLite is truth** — all data flows through `db/gb_brain.db`
- **STOP → Backup → Patch → Run → Verify** — no yolo changes
- **Capital is priority** — risk management enforced at every level
- **Deterministic** — same inputs = same outputs, always
- **.env for secrets** — NEVER commit API keys

## GEM Classification

A strategy is a **GEM** when:
- Win rate ≥ 55%
- Total return > 0%
- Profit factor > 1.0

Everything below 40% win rate or with heavy drawdown = **TRASH**.
