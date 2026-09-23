@echo off
chcp 65001 >nul
:: Check Administrator Privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [INFO] Requesting Administrator privileges to configure Windows Firewall...
    powershell -NoProfile -Command "Start-Process cmd.exe -ArgumentList '/c \"\"%~dp0enable_killswitch.bat\"\"' -Verb RunAs"
    exit /b
)

title Antigravity Kill Switch - Enable
echo ========================================================
echo   Antigravity Outbound Firewall Kill Switch - ENABLE
echo ========================================================
echo.

python "%~dp0cli.py" killswitch enable

echo.
echo ========================================================
python "%~dp0cli.py" killswitch status
echo ========================================================
echo.
pause
