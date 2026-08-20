$ErrorActionPreference = "Stop"
$ProjectRoot = Get-Location
$venvPython = Join-Path $ProjectRoot ".venv\Scripts\python.exe"

if (-not (Test-Path $venvPython)) {
    Write-Host "Virtual environment not found." -ForegroundColor Red
    exit 1
}

Write-Host "==> Running Django check" -ForegroundColor Cyan
& $venvPython manage.py check
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "==> Running Django tests" -ForegroundColor Cyan
& $venvPython manage.py test tests -v 2
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "QA checks completed successfully." -ForegroundColor Green