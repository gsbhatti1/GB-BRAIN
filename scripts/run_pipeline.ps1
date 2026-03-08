# ══════════════════════════════════════════════
# GB-BRAIN — Full Pipeline
# Runs: Harvest → Extract → Fetch Data → Backtest → Score
# ══════════════════════════════════════════════

param(
    [int]$HarvestPages = 2,
    [int]$BacktestLimit = 0,
    [switch]$SkipHarvest,
    [switch]$SkipFetch,
    [switch]$Report
)

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot\..

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  GB-BRAIN — Full Pipeline" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# ── Step 0: Check prerequisites ──────────────
if (-not (Test-Path ".env")) {
    Write-Host "[ERROR] .env not found. Run: Copy-Item .env.example .env" -ForegroundColor Red
    exit 1
}
if (-not (Test-Path "db/gb_brain.db")) {
    Write-Host "[INFO] Database not found. Initializing..." -ForegroundColor Yellow
    python db/brain_db.py
}

# ── Step 1: Harvest ──────────────────────────
if (-not $SkipHarvest) {
    Write-Host ""
    Write-Host "── STEP 1: HARVEST ──" -ForegroundColor Yellow
    python harvest/harvest_github.py --pages $HarvestPages
    if ($LASTEXITCODE -ne 0) { Write-Host "[WARN] Harvest had errors" -ForegroundColor Yellow }
} else {
    Write-Host "[SKIP] Harvest" -ForegroundColor Gray
}

# ── Step 2: Extract Logic ────────────────────
Write-Host ""
Write-Host "── STEP 2: EXTRACT LOGIC ──" -ForegroundColor Yellow
python parse/extract_logic.py
if ($LASTEXITCODE -ne 0) { Write-Host "[WARN] Extraction had errors" -ForegroundColor Yellow }

# ── Step 3: Fetch Market Data ────────────────
if (-not $SkipFetch) {
    Write-Host ""
    Write-Host "── STEP 3: FETCH DATA ──" -ForegroundColor Yellow
    python backtest/fetch_data.py
    if ($LASTEXITCODE -ne 0) { Write-Host "[WARN] Data fetch had errors" -ForegroundColor Yellow }
} else {
    Write-Host "[SKIP] Data fetch" -ForegroundColor Gray
}

# ── Step 4: Run Backtests ────────────────────
Write-Host ""
Write-Host "── STEP 4: BACKTEST ──" -ForegroundColor Yellow
$btArgs = @()
if ($BacktestLimit -gt 0) { $btArgs += "--limit", $BacktestLimit }
python backtest/run_backtest.py @btArgs
if ($LASTEXITCODE -ne 0) { Write-Host "[WARN] Backtest had errors" -ForegroundColor Yellow }

# ── Step 5: Score & Sort ─────────────────────
Write-Host ""
Write-Host "── STEP 5: SCORE & SORT ──" -ForegroundColor Yellow
$scoreArgs = @()
if ($Report) { $scoreArgs += "--report" }
python backtest/score_and_sort.py @scoreArgs
if ($LASTEXITCODE -ne 0) { Write-Host "[WARN] Scoring had errors" -ForegroundColor Yellow }

# ── Done ─────────────────────────────────────
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  PIPELINE COMPLETE" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "  Check strategies/best/ for GEMs" -ForegroundColor Cyan
Write-Host "  Check strategies/archive/trash/ for rejected" -ForegroundColor Gray
if ($Report) {
    Write-Host "  Check monitor/reports/ for Excel rankings" -ForegroundColor Cyan
}
Write-Host ""
