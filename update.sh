#!/bin/bash
# LiftTeam v2.2 — Update project from GitHub

cd "$(dirname "$0")"

echo "Updating LiftTeam from GitHub..."
git pull origin main --force
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
echo "Update complete"
