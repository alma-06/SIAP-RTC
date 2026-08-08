$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
python -m pip install pyinstaller

if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }
if (Test-Path "build") { Remove-Item -Recurse -Force "build" }

python -m PyInstaller `
  --noconfirm `
  --clean `
  --name SIAP-RTC `
  --windowed `
  --paths . `
  app/main.py

Write-Host "Build completado: $Root\dist\SIAP-RTC"
