# ══════════════════════════════════════════════
# GB-BRAIN — Initialize Database
# Run this FIRST before anything else
# ══════════════════════════════════════════════

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot\..

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  GB-BRAIN — Database Init" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check .env exists
if (-not (Test-Path ".env")) {
    Write-Host "[ERROR] .env file not found!" -ForegroundColor Red
    Write-Host "  Copy .env.example to .env and fill in your API keys." -ForegroundColor Yellow
    Write-Host "  Command: Copy-Item .env.example .env" -ForegroundColor Yellow
    exit 1
}

# Init database
python db/brain_db.py
if ($LASTEXITCODE -ne 0) { Write-Host "[FAIL] Database init failed" -ForegroundColor Red; exit 1 }

Write-Host ""
Write-Host "[DONE] Database ready!" -ForegroundColor Green
Write-Host ""
