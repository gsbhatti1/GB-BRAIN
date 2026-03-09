# GB-BRAIN - Start TradingView Webhook Listener
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot\..

Write-Host "Starting GB-BRAIN Webhook Listener..." -ForegroundColor Green
Write-Host "  POST /webhook  - TradingView alerts" -ForegroundColor Cyan
Write-Host "  GET  /health   - Health check" -ForegroundColor Cyan
Write-Host "  POST /kill     - Emergency stop" -ForegroundColor Cyan
Write-Host ""
python webhook/tv_listener.py
