<#!
.SYNOPSIS
Builds a self-contained Sentinel.exe for Windows distribution.

.DESCRIPTION
Run from an activated development virtual environment. The resulting
dist\Sentinel.exe includes Python and PySide6, so the recipient does not need
either installed.
#>

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $projectRoot

$localVenvPython = Join-Path $projectRoot ".venv\Scripts\python.exe"
$sharedVenvPython = Join-Path (Split-Path -Parent (Split-Path -Parent $projectRoot)) ".venv\Scripts\python.exe"

if (Test-Path $localVenvPython) {
    $python = $localVenvPython
}
elseif (Test-Path $sharedVenvPython) {
    # Supports the existing development layout where .venv sits above the repo.
    $python = $sharedVenvPython
}
else {
    $python = (Get-Command python -ErrorAction Stop).Source
}

Write-Host "Using Python: $python"

& $python -m pip install -r requirements-build.txt
if ($LASTEXITCODE -ne 0) {
    throw "Could not install build dependencies. No release was created."
}

& $python -m PyInstaller `
    --noconfirm `
    --clean `
    --windowed `
    --onefile `
    --name Sentinel `
    --paths src `
    Sentinel.pyw

if ($LASTEXITCODE -ne 0) {
    throw "PyInstaller failed. No release was created."
}

Write-Host "Build complete: $projectRoot\dist\Sentinel.exe"

$isccPath = (Get-Command "ISCC.exe" -ErrorAction SilentlyContinue).Source
if (-not $isccPath) {
    $knownPath = Join-Path ${env:ProgramFiles(x86)} "Inno Setup 6\ISCC.exe"
    if (Test-Path $knownPath) {
        $isccPath = $knownPath
    }
}

if ($isccPath) {
    & $isccPath "installer\Sentinel.iss"
    Write-Host "Installer complete: $projectRoot\release\Sentinel-Setup.exe"
}
else {
    Write-Host "Install Inno Setup, then rerun this script to create Sentinel-Setup.exe."
}
