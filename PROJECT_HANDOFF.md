# GB-BRAIN — Project Handoff

## Last Reviewed
Date: 2026-03-28
Commit: latest main branch
Status: Phase 1–2 complete, Phase 3 in progress

## Architecture
One pipeline. One database. SQLite is truth.
Harvest → Extract → Backtest → Score → Deploy → Monitor

Phases:
- Phase 1 (Core repair): DONE — structure stable, SQLite aligned, config clean
- Phase 2 (Runtime spine): DONE — bot_runner, risk_manager, oanda/blofin/telegram wired
- Phase 3 (PC simulation): IN PROGRESS — replay, smoke test, paper executor
- Phase 4 (Strategy truth): PENDING
- Phase 5 (VPS deploy): PENDING
- Phase 6 (Exchange demo): PENDING
- Phase 7 (Weekly calibration): PENDING
- Phase 8 (Production hardening): PENDING
- Phase 9 (Live rollout): PENDING

## What Changed (Recent)
- Added alpaca_bridge.py (Alpaca broker support)
- Added runtime/runtime_policy.py (lane-based policy system)
- Added runtime/live_observer.py (real-time signal observer)
- Added runtime/weekly_calibrator.py (weekly GEM promotion/demotion)
- Added simulate/replay_mode.py (PC replay without live exchange)
- Added simulate/smoke_test.py (forced-signal smoke testing)
- Added simulate/paper_executor.py (paper trade simulation)
- Added monitor/dashboard.py (Flask GEM/trade dashboard)
- Added vps/ deployment scripts
- Fixed PROJECT_HANDOFF.md (this file)

## Known Bugs / Gaps
- BloFin WebSocket path not yet wired to live_observer
- Alpaca bridge tested on paper only — verify order types for indices
- monitor/ templates need CSS polish
- Weekly calibrator needs 30+ days of live_trades data to be meaningful
- VPS deploy scripts written for Ubuntu 22.04 / Debian — test before using

## Next Steps
1. Run smoke test: `python simulate/smoke_test.py --symbol SPX --mode forced`
2. Run replay: `python simulate/replay_mode.py --ticker US30 --tf 5m`
3. Deploy to VPS: follow vps/DEPLOY.md
4. Connect BloFin demo WebSocket
5. Run weekly calibrator after 1 week of paper data

## Open Questions
- Which VPS provider? (DigitalOcean / Vultr / AWS recommended)
- BloFin demo WebSocket — confirm endpoint URL with BloFin docs
- Alpaca — need real API keys for paper account to test fills

## Rules
- SQLite is truth — all data flows through db/gb_brain.db
- STOP → Backup → Patch → Run → Verify — no yolo changes
- Capital is priority — risk management enforced at every level
- Deterministic — same inputs = same outputs, always
- .env for secrets — NEVER commit API keys
