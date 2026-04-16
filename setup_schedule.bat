@echo off
REM Setup Windows Scheduled Tasks for Crypto Risk Radar
REM Runs every 8 hours at 14:00, 22:00, 06:00 Beijing Time (06:00, 14:00, 22:00 UTC)

echo ============================================
echo Crypto Risk Radar - Schedule Setup
echo ============================================
echo.

REM Check if running as admin
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] Please run as Administrator!
    pause
    exit /b 1
)

set "TASK_NAME=CryptoRiskRadar"
set "PYTHON_PATH=C:\Users\Administrator\AppData\Local\Programs\Python\Python311\python.exe"
set "SCRIPT_PATH=F:\stepclaw\agents\blockchain-analyst\run_analysis.py"

REM Remove existing tasks
echo Removing existing tasks...
schtasks /delete /tn "%TASK_NAME%_14" /f >nul 2>&1
schtasks /delete /tn "%TASK_NAME%_22" /f >nul 2>&1
schtasks /delete /tn "%TASK_NAME%_06" /f >nul 2>&1

REM Create Task 1: 14:00 Beijing Time (06:00 UTC) - EU Morning
echo Creating Task 1: 14:00 (EU Morning)...
schtasks /create /tn "%TASK_NAME%_14" /tr "\"%PYTHON_PATH%\" \"%SCRIPT_PATH%\"" ^
    /sc daily /st 14:00 /f

REM Create Task 2: 22:00 Beijing Time (14:00 UTC) - US Pre-market
echo Creating Task 2: 22:00 (US Pre-market)...
schtasks /create /tn "%TASK_NAME%_22" /tr "\"%PYTHON_PATH%\" \"%SCRIPT_PATH%\"" ^
    /sc daily /st 22:00 /f

REM Create Task 3: 06:00 Beijing Time (22:00 UTC) - US Active
echo Creating Task 3: 06:00 (US Active)...
schtasks /create /tn "%TASK_NAME%_06" /tr "\"%PYTHON_PATH%\" \"%SCRIPT_PATH%\"" ^
    /sc daily /st 06:00 /f

echo.
echo ============================================
echo Schedule Created Successfully!
echo ============================================
echo.
echo Tasks created:
echo   - %TASK_NAME%_14 : 14:00 (06:00 UTC)
echo   - %TASK_NAME%_22 : 22:00 (14:00 UTC)
echo   - %TASK_NAME%_06 : 06:00 (22:00 UTC)
echo.
echo To verify, run: schtasks /query /tn "%TASK_NAME%*"
echo To remove, run: schtasks /delete /tn "%TASK_NAME%*" /f
echo.
pause
