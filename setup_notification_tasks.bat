@echo off
echo ==========================================
echo Setting Up Tasks with Notification
echo ==========================================
echo.

REM Remove old tasks
echo Removing old tasks...
schtasks /delete /tn "CryptoRiskRadar_06" /f >nul 2>&1
schtasks /delete /tn "CryptoRiskRadar_14" /f >nul 2>&1
schtasks /delete /tn "CryptoRiskRadar_22" /f >nul 2>&1

set PYTHON=C:\Users\Administrator\AppData\Local\Programs\Python\Python311\python.exe
set SCRIPT=F:\stepclaw\agents\blockchain-analyst\run_with_notification.py

REM Task 1: 06:00 ET = 18:00 CST
echo Creating: 06:00 ET (18:00 CST)...
schtasks /create /tn "CryptoRiskRadar_06" /tr "%PYTHON% %SCRIPT%" /sc daily /st 18:00 /ru SYSTEM /rl HIGHEST /f

REM Task 2: 14:00 ET = 02:00 CST
echo Creating: 14:00 ET (02:00 CST)...
schtasks /create /tn "CryptoRiskRadar_14" /tr "%PYTHON% %SCRIPT%" /sc daily /st 02:00 /ru SYSTEM /rl HIGHEST /f

REM Task 3: 22:00 ET = 10:00 CST
echo Creating: 22:00 ET (10:00 CST)...
schtasks /create /tn "CryptoRiskRadar_22" /tr "%PYTHON% %SCRIPT%" /sc daily /st 10:00 /ru SYSTEM /rl HIGHEST /f

echo.
echo ==========================================
echo Tasks Created with Notification!
echo ==========================================
echo.
echo Schedule:
echo   18:00 CST (06:00 ET) - Pre-market
echo   02:00 CST (14:00 ET) - Mid-day
echo   10:00 CST (22:00 ET) - Evening
echo.
echo You will receive a notification after EACH run.
echo.
pause
