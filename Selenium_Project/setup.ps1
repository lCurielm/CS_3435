<#
PowerShell helper to create a virtual environment and install dependencies.

Usage:
  .\setup.ps1            # create venv and install deps
  .\setup.ps1 --test     # also run a quick headless smoke test

#>

[CmdletBinding()]
param(
    [switch]$Test
)

$root = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent
Push-Location $root

Write-Host "Checking for Python..."

# Prefer the py launcher if available, else try 'python'
$pyCmd = $null
if (Get-Command py -ErrorAction SilentlyContinue) {
    $pyCmd = "py -3"
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    $pyCmd = "python"
}

if (-not $pyCmd) {
    Write-Error "Python was not found in PATH. Install Python 3.8+ from https://www.python.org/ and re-run this script."
    Pop-Location
    exit 1
}

$venvDir = Join-Path $root ".venv"
if (-not (Test-Path $venvDir)) {
    Write-Host "Creating virtual environment in $venvDir"
    & $pyCmd -m venv $venvDir
} else {
    Write-Host "Virtual environment already exists at $venvDir"
}

$venvPython = Join-Path $venvDir "Scripts\python.exe"
if (-not (Test-Path $venvPython)) {
    Write-Error "Virtual environment python not found at $venvPython"
    Pop-Location
    exit 1
}

Write-Host "Upgrading pip and installing requirements..."
& $venvPython -m pip install --upgrade pip
& $venvPython -m pip install -r requirements.txt

if ($Test) {
    Write-Host "Running smoke test (headless)..."
    & $venvPython Selenium.py --url https://example.com --headless
}

Write-Host "Done. To activate the venv in PowerShell: .\\.venv\\Scripts\\Activate.ps1"
Pop-Location
