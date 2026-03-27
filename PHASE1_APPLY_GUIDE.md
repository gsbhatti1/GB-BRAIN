# GB-BRAIN Phase 1 Apply Guide

## Copy/replace these files
Replace existing:
- `ARCHITECTURE_MAP.md`
- `PROJECT_HANDOFF.md`
- `TEST_MATRIX.md`
- `SETUP_GUIDE.md`
- `config/gb_strategy_gems.json`
- `config/settings.py`
- `db/schema.sql`
- `db/brain_db.py`
- `execute/test_read_gems.py`
- `execute/test_apply_gem_params.py`

Add new:
- `config/symbol_registry.json`
- `execute/gem_loader.py`
- `execute/custom_live_engine.py`
- `execute/live_observer.py`
- `execute/weekly_calibrator.py`
- `execute/custom_signal_runner.py`

## Apply order
1. Copy files
2. Run database init
3. Run gem tests
4. Run one shadow custom signal command
5. Run weekly calibrator

## Safety rule
Do not connect live capital until:
- DB schema initializes cleanly
- shadow runner works
- observer summary works
- weekly calibration runs cleanly
