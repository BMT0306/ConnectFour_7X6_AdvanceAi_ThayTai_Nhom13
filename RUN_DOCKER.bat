@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ========================================================
echo   KHOI DONG CONNECT FOUR AI QUA DOCKER (NHOM 13)
echo ========================================================
echo [1] Kiem tra Docker daemon...
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo [LOI] Docker chua duoc bat hoac chua khoi dong xong!
    echo Vui long mo Docker Desktop truoc roi chay lai.
    pause
    exit /b 1
)

echo [2] Dang build va khoi chay Docker container...
docker compose up -d --build

echo [3] Dang mo trinh duyet tai http://localhost:5000 ...
start "" http://localhost:5000

echo.
echo ========================================================
echo   DA KHOI DONG THANH CONG TAI: http://localhost:5000
echo   De dung container go: docker compose down
echo ========================================================
pause
