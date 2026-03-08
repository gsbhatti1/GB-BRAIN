# GB-BRAIN — Score results and sort strategies
param([switch]$Report)

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot\..

$args = @("backtest/score_and_sort.py")
if ($Report) { $args += "--report" }

Write-Host "── GB-BRAIN: SCORE & SORT ──" -ForegroundColor Yellow
python @args
