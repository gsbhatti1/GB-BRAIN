# GB-BRAIN — Run backtests on extracted strategies
param([int]$Limit = 0, [string]$Symbol, [string]$Timeframe)

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot\..

$args = @("backtest/run_backtest.py")
if ($Limit -gt 0) { $args += "--limit"; $args += $Limit }
if ($Symbol) { $args += "--symbol"; $args += $Symbol }
if ($Timeframe) { $args += "--timeframe"; $args += $Timeframe }

Write-Host "── GB-BRAIN: BACKTEST ──" -ForegroundColor Yellow
python @args
