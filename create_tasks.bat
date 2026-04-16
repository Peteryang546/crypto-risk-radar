@echo off
chcp 65001
setlocal enabledelayedexpansion

echo ============================================
echo Creating Crypto Risk Radar Scheduled Tasks
echo ============================================
echo.

REM Check admin
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] Please run as Administrator!
    pause
    exit /b 1
)

set "PYTHON=C:\Users\Administrator\AppData\Local\Programs\Python\Python311\python.exe"
set "SCRIPT=F:\stepclaw\agents\blockchain-analyst\run_analysis.py"
set "TASK=CryptoRiskRadar"

echo Removing existing tasks...
schtasks /delete /tn "%TASK%_06" /f >nul 2>&1
schtasks /delete /tn "%TASK%_14" /f >nul 2>&1
schtasks /delete /tn "%TASK%_22" /f >nul 2>&1

echo.
echo Creating Task 1: 06:00 EST...
schtasks /create /tn "%TASK%_06" /tr "%PYTHON% %SCRIPT%" /sc daily /st 06:00 /f
if %errorLevel% equ 0 (
    echo [OK] Task 1 created
) else (
    echo [FAIL] Task 1 failed
)

echo.
echo Creating Task 2: 14:00 EST...
schtasks /create /tn "%TASK%_14" /tr "%PYTHON% %SCRIPT%" /sc daily /st 14:00 /f
if %errorLevel% equ 0 (
    echo [OK] Task 2 created
) else (
    echo [FAIL] Task 2 failed
)

echo.
echo Creating Task 3: 22:00 EST...
schtasks /create /tn "%TASK%_22" /tr "%PYTHON% %SCRIPT%" /sc daily /st 22:00 /f
if %errorLevel% equ 0 (
    echo [OK] Task 3 created
) else (
    echo [FAIL] Task 3 failed
)

echo.
echo ============================================
echo Verifying tasks...
echo ============================================
schtasks /query /tn "%TASK%*"

echo.
pause
