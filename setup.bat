@echo off
chcp 65001 >nul
echo ===================================================
echo     antigravity-pause: One-Click Installer
echo ===================================================
python "%~dp0install.py"
pause
