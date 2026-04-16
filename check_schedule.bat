@echo off
REM Check Crypto Risk Radar scheduled tasks status

echo ============================================
echo Crypto Risk Radar - Schedule Status Check
echo ============================================
echo.

echo Checking for existing tasks...
schtasks /query /tn "CryptoRiskRadar*" 2>nul

if %errorLevel% neq 0 (
    echo.
    echo [WARNING] No tasks found!
    echo.
    echo To set up automation, run as Administrator:
    echo   setup_schedule_us.bat
    echo.
) else (
    echo.
    echo [OK] Tasks found above
    echo.
    echo Next run times:
    schtasks /query /tn "CryptoRiskRadar*" /fo LIST | findstr "Next Run"
)

echo.
echo Manual run command:
echo   python run_analysis.py
echo.
pause
