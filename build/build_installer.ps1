$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $PSScriptRoot
$iss = Join-Path $root 'installer\SIAP-RTC.iss'

$compiler = @(
    "$env:ProgramFiles(x86)\Inno Setup 6\ISCC.exe",
    "$env:ProgramFiles\Inno Setup 6\ISCC.exe"
) | Where-Object { Test-Path $_ } | Select-Object -First 1

if (-not $compiler) {
    throw 'No se encontró Inno Setup 6 (ISCC.exe). Instálelo en el equipo de construcción.'
}

& $compiler $iss
if ($LASTEXITCODE -ne 0) {
    throw "Inno Setup terminó con código $LASTEXITCODE"
}

Write-Host 'Instalador SIAP-RTC generado correctamente.'
