# GB-BRAIN — Harvest strategies from GitHub
param([int]$Pages = 2, [string[]]$Category)

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot\..

$args = @("harvest/harvest_github.py", "--pages", $Pages)
if ($Category) { $args += "--category"; $args += $Category }

Write-Host "── GB-BRAIN: HARVEST ──" -ForegroundColor Yellow
python @args
