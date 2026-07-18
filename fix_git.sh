#!/bin/bash
# LiftTeam v2.2 — Fix Git issues

cd "$(dirname "$0")"

echo "Fixing Git repository..."

git remote remove origin 2>/dev/null || true
git remote add origin https://github.com/yachtsman13/Lifteam.git

git add -A
git commit -m "LiftTeam v2.2 fix" || true
git branch -M main
git push -u origin main --force

echo "Git repository fixed and pushed"
