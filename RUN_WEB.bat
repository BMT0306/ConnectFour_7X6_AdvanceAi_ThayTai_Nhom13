@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ========================================================
echo   DANG KHOI DONG CONNECT FOUR AI WEB APP (NHOM 13)
echo ========================================================
echo [1] Kiem tra moi truong Python...
if exist "%~dp0.venv\Scripts\python.exe" (
    set "PY_CMD=%~dp0.venv\Scripts\python.exe"
) else (
    set "PY_CMD=python"
)

echo [2] Dang mo trinh duyet tai http://127.0.0.1:5000 ...
start "" http://127.0.0.1:5000

echo [3] Dang khoi dong Web Server tai cong 5000...
"%PY_CMD%" "%~dp0scripts\run_web.py" --host 0.0.0.0 --port 5000 --no-browser
pause
