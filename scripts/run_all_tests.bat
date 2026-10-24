@echo off
echo ========================================================
echo  RUNNING ALL CONNECT FOUR TESTS (CONNECT4-AI)
echo ========================================================
if exist ".venv\Scripts\pytest.exe" (
    ".venv\Scripts\pytest.exe" -v
) else (
    pytest -v
)
pause
