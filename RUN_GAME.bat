@echo off
cd /d "%~dp0"
echo ========================================================
echo   DANG KHOI DONG CONNECT FOUR GAME AI (NHOM 13)
echo ========================================================
if exist ".venv\Scripts\python.exe" (
    start "" ".venv\Scripts\python.exe" scripts\run_gui.py
) else (
    start "" python scripts\run_gui.py
)
