@echo off
chcp 65001 >nul
:: Check Administrator Privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [INFO] Requesting Administrator privileges to remove Windows Firewall rules...
    powershell -NoProfile -Command "Start-Process cmd.exe -ArgumentList '/c \"\"%~dp0disable_killswitch.bat\"\"' -Verb RunAs"
    exit /b
)

title Antigravity Kill Switch - Disable
echo ========================================================
echo   Antigravity Outbound Firewall Kill Switch - DISABLE
echo ========================================================
echo.

python "%~dp0cli.py" killswitch disable

echo.
echo ========================================================
python "%~dp0cli.py" killswitch status
echo ========================================================
echo.
pause
