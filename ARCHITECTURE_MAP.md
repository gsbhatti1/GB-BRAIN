# GB-BRAIN Architecture Map — Phase 1 Truth

## Mission
One repo, one signal truth, one database, two production lanes:

- **GB-CRYPTO-BOT** → BloFin demo/live for BTC, ETH, SOL futures
- **GB-INDICES** → OANDA practice/live for US30, NAS100, SPX500
- **Manual signal lane** → Cipher / Parallax / Combined for discretionary execution

## The actual repo spine

```text
harvest/harvest_github.py
    ↓
parse/extract_logic.py
    ↓
backtest/run_backtest.py
    ↓
backtest/score_and_sort.py
    ↓
SQLite (db/gb_brain.db)
    ↓
strategies/best | strategies/archive/trash

CUSTOM R&D:
strategies/custom/*
    ↓
backtest/run_custom_backtest.py
    ↓
SQLite

PHASE 1 NEW SHARED CONTROL LAYER:
config/symbol_registry.json
config/gb_strategy_gems.json
execute/gem_loader.py
execute/custom_live_engine.py
execute/live_observer.py
execute/weekly_calibrator.py
```

## Structural truth
The repo currently has two different signal worlds:

1. **Harvested strategy world**
   - generic logic extraction
   - generic backtesting
   - generic GEM scoring

2. **Custom institutional world**
   - Cipher
   - Parallax
   - Combined
   - custom backtesting
   - intended live/manual usage

Phase 1 exists to stop those worlds from drifting apart.

## Phase 1 decisions
- `symbol_registry.json` becomes the source of symbol truth
- `gb_strategy_gems.json` becomes the source of runtime profile truth
- `custom_live_engine.py` becomes the shared adapter for live and shadow use
- `live_observer.py` records candidate / confirmed / executed truth
- `weekly_calibrator.py` computes the 7-day scorecard
- SQLite remains the truth layer

## Pipeline after Phase 1

```text
GitHub push
   ↓
PC research / harvest / backtest
   ↓
SQLite + gem config update
   ↓
Shadow live custom engine
   ↓
Live observer tables
   ↓
Weekly calibration
   ↓
Promote / demote
   ↓
GB-CRYPTO-BOT or GB-INDICES
```

## Folder ownership
- `harvest/` = collect ideas
- `parse/` = extract rules from harvested files
- `backtest/` = historical testing
- `strategies/custom/` = authoritative institutional signal family
- `execute/` = runtime and broker execution
- `config/` = symbol truth + runtime truth
- `db/` = schema truth + persistence
- `monitor/` = reports / dashboards / health
- `webhook/` = inbound TV/manual triggers

## Do not delete yet
Do **not** blindly delete:
- `strategies/archive/trash/`
- harvested source corpus

Quarantine later if size becomes a maintenance problem, but keep until the new closed loop is stable.

## V2 north star
Backtest finds ideas.
Shadow live measures honesty.
Weekly calibration finds survivors.
Bots run only survivors.
