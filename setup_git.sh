#!/bin/bash
# LiftTeam v2.2 — Setup Git repository and push to GitHub

cd "$(dirname "$0")"

REPO_URL="https://github.com/yachtsman13/Lifteam.git"

echo "Setting up Git repository..."

if [ ! -d ".git" ]; then
    git init
    git remote add origin "$REPO_URL" 2>/dev/null || git remote set-url origin "$REPO_URL"
fi

git add -A
git commit -m "LiftTeam v2.2 update" || true
git branch -M main
git push -u origin main --force

echo "Repository pushed to $REPO_URL"
