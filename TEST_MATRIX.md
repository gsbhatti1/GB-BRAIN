# GB-BRAIN Test Matrix — Phase 1

## Goal
Every file in this pack should be testable before any live brokerage wiring happens.

## 1) Database schema
### Command
```powershell
python -c "from db.brain_db import init_db; init_db()"
```

### Expect
- database initializes cleanly
- no SQL syntax error
- new Phase 1 tables exist

### Check
```powershell
sqlite3 .\db\gb_brain.db ".tables"
```

Should include:
- `signal_candidates`
- `signal_confirmations`
- `trade_executions`
- `weekly_calibration`

---

## 2) Symbol registry
### Command
```powershell
python -c "from execute.gem_loader import load_symbol_registry; import json; print(json.dumps(load_symbol_registry(), indent=2)[:500])"
```

### Expect
- JSON loads
- BTC / ETH / SOL / US30 / NAS100 / SPX500 are present

---

## 3) Gem config
### Command
```powershell
python execute/test_read_gems.py
python execute/test_apply_gem_params.py
```

### Expect
- prints active runtime profiles
- prints params for a selected strategy family / symbol / timeframe

---

## 4) Custom live engine import
### Command
```powershell
python -c "from execute.custom_live_engine import CustomLiveEngine; print('OK')"
```

### Expect
- imports cleanly
- no missing symbol registry / gem loader errors

---

## 5) Shadow signal run
### Command
```powershell
python execute/custom_signal_runner.py --family combined --symbol SOL --timeframe 15m --broker yfinance --once --shadow
```

### Expect
- candles fetched
- latest confirmed signal printed, or an explicit 'no confirmed signal'
- no crash

---

## 6) Live observer CLI
### Command
```powershell
python execute/live_observer.py --init
python execute/live_observer.py --summary --days 7
```

### Expect
- tables created if missing
- summary prints even if counts are zero

---

## 7) Weekly calibrator
### Command
```powershell
python execute/weekly_calibrator.py --days 7
```

### Expect
- grouped summary prints
- writes zero or more rows into `weekly_calibration`
- does not fail on empty history

---

## 8) Custom backtest list
### Command
```powershell
python backtest/run_custom_backtest.py --list
```

### Expect
- lists available custom tickers
- confirms Phase 1 pack did not break custom backtest discovery

---

## Fail-fast rule
Do not connect any live account until tests 1–7 pass on:
- Windows dev PC
- VPS paper environment
