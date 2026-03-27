# GB-BRAIN Setup Guide — Phase 1

## Purpose
This guide sets up the **foundation repair layer**:
- shared symbols
- shared gem runtime profiles
- shared live observer
- weekly calibration

It does **not** claim a finished production deployment yet.

## 1) Copy files
Drop the replacement files from this pack into the repo root, preserving folders.

## 2) Python environment
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 3) Environment file
```powershell
Copy-Item .env.example .env
notepad .env
```

Fill:
- OANDA practice creds
- BloFin demo creds
- Telegram bot creds
- TradingView webhook secret

## 4) Initialize database
```powershell
python -c "from db.brain_db import init_db; init_db()"
```

## 5) Verify symbol + gem config
```powershell
python execute/test_read_gems.py
python execute/test_apply_gem_params.py
```

## 6) Run shadow custom engine once
### Crypto example
```powershell
python execute/custom_signal_runner.py --family combined --symbol SOL --timeframe 15m --broker blofin --once --shadow
```

### Indices example
```powershell
python execute/custom_signal_runner.py --family cipher --symbol US30 --timeframe 5m --broker yfinance --once --shadow
```

## 7) View live observer summary
```powershell
python execute/live_observer.py --summary --days 7
```

## 8) Run weekly calibration
```powershell
python execute/weekly_calibrator.py --days 7
```

## PC vs VPS split
### Run on PC
- repo editing
- strategy harvest
- parser work
- heavy backtests
- local AI research

### Run on VPS
- shadow runner loop
- paper/live bots
- webhook listener
- Telegram alerts
- weekly calibration cron / scheduled task

## Deployment recommendation
### Dev machine
Windows PC is fine for:
- GB-BRAIN research
- custom backtests
- model experimentation
- docs and repo management

### Production machine
Use a VPS for:
- 24/7 bot uptime
- restarts after network failures
- broker access
- weekly jobs
- monitoring

Do not put unrestricted local agents on the same machine that stores live exchange secrets.

## Minimum safe order
1. custom backtest
2. shadow live
3. weekly calibration
4. paper execution
5. limited live capital
