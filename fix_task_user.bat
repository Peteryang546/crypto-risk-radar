@echo off
chcp 65001 >nul
echo ==========================================
echo Fix Task Scheduler - Change User to Current
echo ==========================================
echo.

set "USERNAME=%USERDOMAIN%\%USERNAME%"
echo Current user: %USERNAME%
echo.

:: Delete and recreate tasks with current user
schtasks /delete /tn "CryptoRiskRadar_06" /f >nul 2>&1
schtasks /delete /tn "CryptoRiskRadar_14" /f >nul 2>&1
schtasks /delete /tn "CryptoRiskRadar_22" /f >nul 2>&1

echo [1/3] Recreating CryptoRiskRadar_06 (18:00 CST)...
schtasks /create /tn "CryptoRiskRadar_06" /tr "C:\Users\Administrator\AppData\Local\Programs\Python\Python311\python.exe F:\stepclaw\agents\blockchain-analyst\run_with_notification.py" /sc daily /st 18:00 /ru "%USERNAME%" /rp /rl HIGHEST /f

echo [2/3] Recreating CryptoRiskRadar_14 (02:00 CST)...
schtasks /create /tn "CryptoRiskRadar_14" /tr "C:\Users\Administrator\AppData\Local\Programs\Python\Python311\python.exe F:\stepclaw\agents\blockchain-analyst\run_with_notification.py" /sc daily /st 02:00 /ru "%USERNAME%" /rp /rl HIGHEST /f

echo [3/3] Recreating CryptoRiskRadar_22 (10:00 CST)...
schtasks /create /tn "CryptoRiskRadar_22" /tr "C:\Users\Administrator\AppData\Local\Programs\Python\Python311\python.exe F:\stepclaw\agents\blockchain-analyst\run_with_notification.py" /sc daily /st 10:00 /ru "%USERNAME%" /rp /rl HIGHEST /f

echo.
echo ==========================================
echo Tasks recreated successfully!
echo ==========================================
echo.
echo Schedule (CST):
echo   - 02:00 (CryptoRiskRadar_14)
echo   - 10:00 (CryptoRiskRadar_22)
echo   - 18:00 (CryptoRiskRadar_06)
echo.
pause
