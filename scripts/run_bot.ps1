# GB-BRAIN - Start a trading bot
param(
    [string]$Strategy,
    [string]$Broker = "oanda",
    [string]$Symbol = "SPX",
    [string]$Timeframe = "1h",
    [int]$Leverage = 1,
    [int]$Interval = 60,
    [switch]$Live,
    [switch]$List
)

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot\..

if ($List) {
    python execute/bot_runner.py --list
    exit
}

if (-not $Strategy) {
    Write-Host "Usage:" -ForegroundColor Cyan
    Write-Host '  .\scripts\run_bot.ps1 -List'
    Write-Host '  .\scripts\run_bot.ps1 -Strategy "Bollinger" -Broker oanda -Symbol SPX'
    Write-Host '  .\scripts\run_bot.ps1 -Strategy "keithorange" -Broker blofin -Symbol SOL -Leverage 3'
    exit
}

$args = @("execute/bot_runner.py",
    "--strategy", $Strategy,
    "--broker", $Broker,
    "--symbol", $Symbol,
    "--timeframe", $Timeframe,
    "--leverage", $Leverage,
    "--interval", $Interval)

if ($Live) { $args += "--live" } else { $args += "--paper" }

Write-Host "Starting GB-BRAIN Bot..." -ForegroundColor Green
python @args
