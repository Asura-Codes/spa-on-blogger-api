# This script sets up a Python virtual environment and installs required packages
# Usage: .\setup.ps1

$venvPath = ".venv"

if (-Not (Test-Path $venvPath)) {
    python -m venv $venvPath
    Write-Host "Virtual environment created at $venvPath"
} else {
    Write-Host "Virtual environment already exists at $venvPath"
}

$activateScript = ".venv\Scripts\Activate.ps1"
Write-Host "To activate the virtual environment, run:`n    . $activateScript"

Write-Host "To install requirements, run:`n    . $activateScript; pip install -r requirements.txt"
