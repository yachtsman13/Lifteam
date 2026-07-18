@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo Updating LiftTeam from GitHub...
git pull origin main --force
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
echo Update complete
pause
