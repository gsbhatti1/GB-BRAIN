# GB-BRAIN — Project Handoff

## Last Reviewed
Date: 2026-03-28
Commit: 1cff243
Status: ALL 9 PHASES COMPLETE — system live on VPS

## Architecture
One pipeline. One database. SQLite is truth.
Harvest → Extract → Backtest → Score → Deploy → Monitor

## Phase Status
- Phase 1 (Core repair): DONE
- Phase 2 (Runtime spine): DONE
- Phase 3 (PC simulation): DONE — smoke test, replay, parity all PASS
- Phase 4 (Strategy truth): DONE — CombinedEngine, gb_strategy_gems.json
- Phase 5 (VPS deploy): DONE — Ubuntu 24.04, supervisor running
- Phase 6 (Exchange demo): DONE — OANDA practice + BloFin demo both running
- Phase 7 (Weekly calibration): DONE — calibration_loop.py running clean
- Phase 8 (Production hardening): DONE — kill_switch ARMED, health_check OK=6
- Phase 9 (Live rollout): DONE — live_runner Stage 1 MICRO active

## VPS Details
- IP: 144.202.57.0
- OS: Ubuntu 24.04 LTS
- Python venv: /home/gb-brain/GB-BRAIN/.venv/bin/python
- DB: /home/gb-brain/GB-BRAIN/db/gb_brain.db
- Logs: /var/log/gb-brain/

## Supervisor Processes (all RUNNING)
- gb-observer: polls 6 lanes every 60s, writes to observed_signals, heartbeat every 5min
- gb-webhook: Flask on port 5000, receives TradingView alerts
- gb-demo: demo_runner --broker oanda --symbol US30 --tf 5m (OANDA practice)
- gb-demo-blofin: demo_runner --broker blofin --symbol ETH --tf 5m (BloFin demo)
- gb-live: live_runner --broker oanda --symbol US30 --tf 5m (Stage 1 MICRO, 0.5% risk)

## Capital Allocator
- Current stage: 1 — MICRO
- Risk per trade: 0.5%
- Max positions: 1
- Max daily loss: 1.0%
- Advance to Stage 2 after 2 weeks of clean live operation:
  python3 -m runtime.live_runner --advance-stage

## Broker Setup
- OANDA: practice account (fxpractice.oanda.com) — indices: US30, NAS100, SPX500
- BloFin: demo account ($1000 paper) — crypto: ETH, BTC, SOL
- Both brokers use demo/practice API keys — no real capital at risk yet

## Weekly Workflow
1. Sunday 6am UTC: calibration_loop runs automatically
2. Sunday 9am MDT: reminder to run harvest on PC
3. Run harvest on PC: harvest → parse → backtest → score_and_sort
4. Review new GEMs, update config/gb_strategy_gems.json if needed
5. git push → VPS auto-pulls at 3am UTC daily

## Harvest Pipeline (run on PC weekly)
python harvest/harvest_github.py --pages 2
python parse/extract_logic.py
python backtest/run_backtest.py --limit 100
python backtest/score_and_sort.py --report

## Monitoring Commands (VPS)
python3 -m runtime.health_check
python3 -m runtime.fill_tracker --broker oanda
python3 -m runtime.slippage_check --broker oanda
python3 -m runtime.calibration_loop --dry-run
tail -f /var/log/gb-brain/live.log
supervisorctl status

## Emergency Stop
python3 -m runtime.kill_switch trip     # stop new orders
python3 -m runtime.kill_switch halt     # full stop
python3 -m runtime.kill_switch status   # check state
python3 -m runtime.kill_switch reset    # re-arm (requires confirmation)

## Key Files Modified (this session)
- runtime/demo_runner.py: complete rewrite — correct import paths, CombinedEngine, schema fixes
- runtime/live_runner.py: NEW — Phase 9 live runner with CapitalAllocator sizing
- runtime/calibration_loop.py: fixed import paths and lookback_days kwarg
- runtime/health_check.py: fixed HTTPError handling, OANDA_API_TOKEN, telegram import
- runtime/live_observer.py: added observer_heartbeat.json write for health_check
- execute/alpaca_bridge.py: rewritten for alpaca-py SDK
- simulate/smoke_test.py: fixed OANDA key name and can_trade args
- simulate/replay_mode.py: fixed CSV numeric coerce for ^DJI rows
- simulate/engine_parity_check.py: fixed gem loop depth

## Rules
- SQLite is truth — all data flows through db/gb_brain.db
- STOP → Backup → Patch → Run → Verify — no yolo changes
- Capital is priority — risk management enforced at every level
- Deterministic — same inputs = same outputs, always
- .env for secrets — NEVER commit API keys
