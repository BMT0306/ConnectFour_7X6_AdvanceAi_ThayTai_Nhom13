@echo off
chcp 65001 >nul
cd /d "%~dp0"
title Connect Four AI - Nhom 13 Launcher
cls
echo ======================================================================
echo          CONNECT FOUR 7x6 AI - NHOM 13 (DO NHU TAI)
echo ======================================================================
echo.
echo   Chon che do khoi chay:
echo.
echo   [1] Web App (Khuyen nghi - Choi ngay tren trinh duyet Browser)
echo   [2] Docker Container (Chay tren Docker cong 5000)
echo   [3] Desktop App (Giao dien do hoa Pygame)
echo   [4] Thoat
echo.
set /p choice="Nhap lua chon cua ban [1-4] (Mac dinh 1): "
if "%choice%"=="" set choice=1

if "%choice%"=="1" (
    call RUN_WEB.bat
) else if "%choice%"=="2" (
    call RUN_DOCKER.bat
) else if "%choice%"=="3" (
    call RUN_GAME.bat
) else (
    exit /b 0
)
