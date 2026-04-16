@echo off
chcp 65001 >nul
echo ==========================================
echo Updating Scheduled Tasks with Feedback
echo ==========================================
echo.

REM Remove old tasks
echo Removing old tasks...
schtasks /delete /tn "CryptoRiskRadar_06" /f >nul 2>&1
schtasks /delete /tn "CryptoRiskRadar_14" /f >nul 2>&1
schtasks /delete /tn "CryptoRiskRadar_22" /f >nul 2>&1

REM Create new tasks with feedback script
set PYTHON_PATH=C:\Users\Administrator\AppData\Local\Programs\Python\Python311\python.exe
set SCRIPT_PATH=F:\stepclaw\agents\blockchain-analyst\run_with_feedback.py
set WORK_DIR=F:\stepclaw\agents\blockchain-analyst

REM Task 1: 06:00 ET (18:00 CST)
echo Creating task: CryptoRiskRadar_06 (06:00 ET / 18:00 CST)...
schtasks /create /tn "CryptoRiskRadar_06" ^
  /tr "%PYTHON_PATH% %SCRIPT_PATH%" ^
  /sc daily /st 18:00 ^
  /ru SYSTEM ^
  /rl HIGHEST ^
  /f

REM Task 2: 14:00 ET (02:00 CST next day)
echo Creating task: CryptoRiskRadar_14 (14:00 ET / 02:00 CST)...
schtasks /create /tn "CryptoRiskRadar_14" ^
  /tr "%PYTHON_PATH% %SCRIPT_PATH%" ^
  /sc daily /st 02:00 ^
  /ru SYSTEM ^
  /rl HIGHEST ^
  /f

REM Task 3: 22:00 ET (10:00 CST)
echo Creating task: CryptoRiskRadar_22 (22:00 ET / 10:00 CST)...
schtasks /create /tn "CryptoRiskRadar_22" ^
  /tr "%PYTHON_PATH% %SCRIPT_PATH%" ^
  /sc daily /st 10:00 ^
  /ru SYSTEM ^
  /rl HIGHEST ^
  /f

echo.
echo ==========================================
echo Tasks Updated Successfully!
echo ==========================================
echo.
echo New schedule (all tasks now include feedback):
echo   06:00 ET = 18:00 CST (Pre-market)echo   14:00 ET = 02:00 CST (Mid-day)
echo   22:00 ET = 10:00 CST (Evening)
echo.
echo Check status with: schtasks /query | findstr Crypto
echo.
pause
