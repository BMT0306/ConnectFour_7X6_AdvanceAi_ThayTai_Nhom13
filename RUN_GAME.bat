@echo off
cd /d "%~dp0"
echo ========================================================
echo   DANG KHOI DONG CONNECT FOUR GAME AI (NHOM 13)
echo ========================================================
if exist "%~dp0.venv\Scripts\python.exe" (
    start "" "%~dp0.venv\Scripts\python.exe" "%~dp0scripts\run_gui.py"
) else (
    start "" python "%~dp0scripts\run_gui.py"
)
