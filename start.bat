@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo.
echo   ================================================
echo    LiftTeam v2.2.4.4.3.2 — Starting Standalone Server
echo   ================================================
echo.
python lifteam_launcher.py
pause
