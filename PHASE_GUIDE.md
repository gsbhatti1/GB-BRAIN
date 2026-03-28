# GB-BRAIN — Phase Execution Guide

## Where You Are Now
After this update: Phase 1–5 code complete. Phase 3 is your next action.

## The Order of Operations

### RIGHT NOW — Phase 3: Prove It Works on PC

Step 1: Smoke Test (10 minutes)
```powershell
.\scripts\run_smoke.ps1
```
Expected: "SMOKE TEST PASSED" — all imports OK, DB tables exist, forced signals flow through paper_executor

Step 2: Replay Mode (20 minutes)
```powershell
.\scripts\run_replay.ps1
```
Expected: bar-by-bar replay on US30, signals generated, paper trades opened/closed, final P&L report

Step 3: Parity Check (5 minutes)
```powershell
.\scripts\run_parity.ps1
```
Expected: all 6 parity checks PASS — symbol maps agree, presets valid, no look-ahead

If all 3 pass → Phase 3 is DONE. Commit.

---

### THEN — Phase 5: VPS Deploy

Follow vps/DEPLOY.md step by step.
Run smoke test on VPS before anything else.

---

### THEN — Phase 6: Exchange Demo

```powershell
.\scripts\run_demo.ps1
```
Run for 1–2 weeks. Monitor fills and slippage via:
```powershell
python runtime/fill_tracker.py
python runtime/slippage_check.py
```

---

### THEN — Phase 7: Weekly Calibration

After 1 week of observed signals:
```powershell
.\scripts\run_calibrate.ps1
```
Check which lanes get promoted from "candidate" → "confirmed".

---

### THEN — Phase 8: Harden

Check kill switch works:
```powershell
.\scripts\run_kill.ps1 status
python runtime/kill_switch.py trip
python runtime/kill_switch.py reset
```
Review audit log: `db/audit.jsonl`
Review health check: `.\scripts\run_health.ps1`

---

### THEN — Phase 9: Go Live

Use capital_allocator.py Stage 1 (micro):
- 0.5% risk per trade
- 1 symbol only (start with ETH or US30 — whichever has best demo P&L)
- 1 bot only
- Watch for 2 weeks before advancing to Stage 2

---

## Dashboard

Start it any time:
```powershell
.\scripts\run_dashboard.ps1
```
Then open: http://localhost:5001

---

## If Anything Breaks

1. STOP — don't keep running
2. Backup DB: `copy db\gb_brain.db db\gb_brain_backup.db`
3. Check audit log: `python runtime/audit_log.py tail`
4. Check health: `.\scripts\run_health.ps1`
5. Trip kill switch: `python runtime/kill_switch.py trip`
6. Fix, test, reset kill switch, restart
