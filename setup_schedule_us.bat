@echo off
REM Setup Windows Scheduled Tasks for Crypto Risk Radar (US Time Format)
REM Runs every 8 hours at 10:00 PM, 6:00 AM, 2:00 PM EST

echo ============================================
echo Crypto Risk Radar - Schedule Setup (US Time)
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
schtasks /delete /tn "%TASK_NAME%_22" /f >nul 2>&1
schtasks /delete /tn "%TASK_NAME%_06" /f >nul 2>&1
schtasks /delete /tn "%TASK_NAME%_14" /f >nul 2>&1

REM Create Task 1: 06:00 EST - Pre-market
echo Creating Task 1: 06:00 EST - Pre-market...
schtasks /create /tn "%TASK_NAME%_06" /tr "\"%PYTHON_PATH%\" \"%SCRIPT_PATH%\"" ^
    /sc daily /st 06:00 /f

REM Create Task 2: 14:00 EST - Mid-day
echo Creating Task 2: 14:00 EST - Mid-day...
schtasks /create /tn "%TASK_NAME%_14" /tr "\"%PYTHON_PATH%\" \"%SCRIPT_PATH%\"" ^
    /sc daily /st 14:00 /f

REM Create Task 3: 22:00 EST - Evening
echo Creating Task 3: 22:00 EST - Evening...
schtasks /create /tn "%TASK_NAME%_22" /tr "\"%PYTHON_PATH%\" \"%SCRIPT_PATH%\"" ^
    /sc daily /st 22:00 /f

echo.
echo ============================================
echo Schedule Created Successfully!
echo ============================================
echo.
echo Schedule (EST - US Eastern Time):
echo   - 06:00 EST (Pre-market Analysis)
echo   - 14:00 EST (Mid-day Update)
echo   - 22:00 EST (Evening Summary)
echo.
echo Corresponding Beijing Time:
echo   - 18:00 CST (Same Day)
echo   - 02:00 CST (Next Day)
echo   - 10:00 CST (Next Day)
echo.
echo Interval: Every 8 hours (3 times per day)
echo.
echo To verify, run: schtasks /query /tn "%TASK_NAME%*"
echo To remove, run: schtasks /delete /tn "%TASK_NAME%*" /f
echo.
pause
