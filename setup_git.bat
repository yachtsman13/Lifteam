@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo Setting up Git repository...

if not exist ".git" (
    git init
    git remote add origin https://github.com/yachtsman13/Lifteam.git 2>nul || git remote set-url origin https://github.com/yachtsman13/Lifteam.git
)

git add -A
git commit -m "LiftTeam v2.2 update" || true
git branch -M main
git push -u origin main --force

echo Repository pushed to https://github.com/yachtsman13/Lifteam.git
pause
