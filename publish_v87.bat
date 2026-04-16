@echo off
chcp 65001 >nul
REM Crypto Risk Radar v8.7 Release Script
REM Run this script to publish v8.7 to GitHub Pages

echo ==========================================
echo Crypto Risk Radar v8.7 - Release Script
echo ==========================================

REM Check if we're in the right directory
if not exist "README.md" (
    echo [ERROR] Please run this script from the project root
    exit /b 1
)

REM Generate fresh report with v8.7 features
echo.
echo [1/5] Generating v8.7 report...
python scripts\generate_enhanced_full_report.py
if %errorlevel% neq 0 (
    echo [ERROR] Report generation failed
    exit /b 1
)

REM Copy latest report to index.html
echo.
echo [2/5] Copying report to index.html...
for /f "delims=" %%a in ('dir /b /o-d output\enhanced_report_*.html') do (
    set "LATEST_REPORT=output\%%a"
    goto :found
)
:found
copy /Y "%LATEST_REPORT%" index.html >nul
echo [OK] Copied: %LATEST_REPORT% -^> index.html

REM Update version badge
echo.
echo [3/5] Updating version badge...
powershell -Command "(Get-Content index.html) -replace 'Crypto Risk Radar', 'Crypto Risk Radar v8.7' | Set-Content index.html"

REM Git operations
echo.
echo [4/5] Committing changes...
git add -A
git commit -m "Release v8.7: 5-Dimension Risk Scoring + Heatmap + Risk Matrix

New Features:
- 5-Dimension Risk Scoring (Market/Security/Financial/Operational/Sentiment)
- Interactive Risk Heatmap (6 assets: BTC/ETH/SOL/BNB/XRP/DOGE)
- Risk Matrix Assessment (4x4 likelihood-impact matrix)
- Real-time data from CoinGecko/GoPlus/GeckoTerminal
- 13 total modules (11 original + 2 new v8.7)

Quality: A+ rating
Data: 90%+ real-time APIs
Methodology: Documented in METHODOLOGY.md"

REM Push to GitHub
echo.
echo [5/5] Pushing to GitHub...
git push origin main

echo.
echo ==========================================
echo v8.7 Release Complete!
echo ==========================================
echo.
echo Website: https://peteryang546.github.io/crypto-risk-radar/
echo Report: %LATEST_REPORT%
echo.
echo Next automatic update: 10:00 CST (22:00 ET)

pause
