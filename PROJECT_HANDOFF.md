# GB-BRAIN Project Handoff — Phase 1

## Snapshot
- Base repo snapshot reviewed: `a59f67c8f6ce8b0eb17c13706333af77867236b2`
- Review tag: `review-2026-03-10-v2`
- Structural repair phase: **Phase 1 foundation**

## What changed in this pack
This pack introduces:
- real docs replacing placeholders
- shared symbol registry
- shared gem loader
- shared custom live engine adapter
- live observer schema + runtime
- weekly calibrator skeleton
- updated gem config format
- updated gem test scripts

## Why this phase exists
The repo had a split-brain problem:
- custom backtest truth was strong
- live execution truth was using a different signal path

Phase 1 does **not** claim to complete the full live rewrite.
It builds the clean backbone so that Phase 2 can wire runtime execution without confusion.

## Known structural truths
- Harvest/backtest lane and custom/live lane both exist
- SQLite is already the right truth layer
- Custom engines are the strongest research core
- Runtime config was too weak and too fragmented
- Placeholder docs would create future confusion

## Known limitations after Phase 1
- `execute/bot_runner.py` and `execute/grid_bot.py` are not fully rewritten yet
- Intrabar candidate logging still depends on how often the live runner polls
- Paper/live execution parity is still a Phase 2 task
- Cross-asset risk normalization still needs Phase 2 attention

## Next phases
### Phase 2
- replace live runtime path with shared custom engine truth
- wire BloFin crypto runner and OANDA indices runner to observer tables
- add shadow/live toggle
- add better execution persistence

### Phase 3
- walk-forward optimizer
- automatic weekly promote/demote
- VPS deployment + service manager
- agent orchestration

## Repo cleanup policy
Delete only after proof.
Prefer:
- replace placeholder docs
- remove committed review zips
- quarantine bulky historical folders later
- never delete the custom strategy family

## Open questions
- final BloFin leverage defaults by symbol
- OANDA instrument naming conventions in your account
- whether manual signal lane should use same DB or a second DB
- whether live observer should run close-only first or intrabar from day one
