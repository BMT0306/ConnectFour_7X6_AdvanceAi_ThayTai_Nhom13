Write-Host "========================================================" -ForegroundColor Cyan
Write-Host " RUNNING ALL CONNECT FOUR TESTS (CONNECT4-AI)" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan

if (Test-Path ".\.venv\Scripts\pytest.exe") {
    & ".\.venv\Scripts\pytest.exe" -v
} else {
    pytest -v
}
