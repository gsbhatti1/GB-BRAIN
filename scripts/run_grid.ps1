# GB-BRAIN - Start Grid Bot for BloFin Crypto Futures
param(
    [string]$Symbol = "ETH",
    [int]$Leverage = 3,
    [int]$Grids = 10,
    [float]$Spacing = 0.5,
    [float]$TP = 1.0,
    [float]$SL = 3.0,
    [string]$Timeframe = "15m",
    [int]$Interval = 60,
    [switch]$Live,
    [switch]$Config
)

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot\..

$args = @("execute/grid_bot.py",
    "--symbol", $Symbol,
    "--leverage", $Leverage,
    "--grids", $Grids,
    "--spacing", $Spacing,
    "--tp", $TP,
    "--sl", $SL,
    "--timeframe", $Timeframe,
    "--interval", $Interval)

if ($Config) { $args += "--config" }
elseif ($Live) { $args += "--live" }
else { $args += "--paper" }

Write-Host "GB-BRAIN Grid Bot: $Symbol-USDT | ${Leverage}x | $Grids grids" -ForegroundColor Green
python @args
