@echo off
chcp 65001 >nul
cd /d "%~dp0"
title Connect Four 7x6 AI - Nhom 13 Quick Launcher

if exist "%~dp0.venv\Scripts\python.exe" (
    set "PY_CMD=%~dp0.venv\Scripts\python.exe"
) else (
    set "PY_CMD=python"
)

:MENU
cls
echo ======================================================================
echo        CONNECT FOUR 7x6 GAME AI - NHOM 13 (GVHD: THAY DO NHU TAI)
echo ======================================================================
echo.
echo   Chon che do khoi chay nhanh:
echo.
echo   [1] Web App         (Mac dinh - Choi ngay tren Trinh duyet port 5000)
echo   [2] Desktop Pygame  (Giao dien do hoa Desktop 60 FPS)
echo   [3] Terminal CLI    (Choi nhanh tren cua so dong lenh)
echo   [4] Chay Unit Tests (Kiem tra 57 bai test tu dong Pytest)
echo   [0] Thoat
echo.
set "choice="
set /p choice="Nhap lua chon [0-4] (Nhan Enter de chon 1): "
if "%choice%"=="" set "choice=1"

if "%choice%"=="1" goto RUN_WEB
if "%choice%"=="2" goto RUN_GUI
if "%choice%"=="3" goto RUN_CLI
if "%choice%"=="4" goto RUN_TESTS
if "%choice%"=="0" exit /b 0
goto MENU

:RUN_WEB
echo.
echo [*] Dang khoi dong Web Server tai http://localhost:5000 ...
echo [*] Nhan Ctrl+C de dung server.
"%PY_CMD%" -m c4.ui.web_server --host 0.0.0.0 --port 5000
pause
exit /b 0

:RUN_GUI
echo.
echo [*] Dang mo giao dien Desktop Pygame...
start "" "%PY_CMD%" -m c4.ui.gui
exit /b 0

:RUN_CLI
echo.
"%PY_CMD%" -m c4.play --opponent alphabeta --depth 5
pause
goto MENU

:RUN_TESTS
echo.
"%PY_CMD%" -m pytest -v
pause
goto MENU
