#!/bin/bash
# LiftTeam v2.2 — Update version in all files
# Usage: ./update_version.sh [VERSION]

cd "$(dirname "$0")"

NEW_VERSION="${1:-v2.2}"
OLD_VERSION="v2.2"

echo "Updating version from $OLD_VERSION to $NEW_VERSION..."

# Update files
sed -i "s/LiftTeam v2.2/LiftTeam $NEW_VERSION/g" README.md 2>/dev/null || true
sed -i "s/LiftTeam v2.2/LiftTeam $NEW_VERSION/g" CHANGELOG.md 2>/dev/null || true
sed -i "s/LiftTeam v2.2/LiftTeam $NEW_VERSION/g" lifteam_launcher.py 2>/dev/null || true
sed -i "s/LiftTeam v2.2/LiftTeam $NEW_VERSION/g" start.sh 2>/dev/null || true
sed -i "s/LiftTeam v2.2/LiftTeam $NEW_VERSION/g" start.bat 2>/dev/null || true
sed -i "s/LiftTeam v2.2/LiftTeam $NEW_VERSION/g" Dockerfile 2>/dev/null || true

echo "Version updated to $NEW_VERSION"
