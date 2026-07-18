@echo off
chcp 65001 >nul
cd /d "%~dp0"

if "%~1"=="" (
    echo Usage: update_version.bat [VERSION]
    echo Example: update_version.bat v2.3
    exit /b 1
)

set NEW_VERSION=%~1
echo Updating version to %NEW_VERSION%...

powershell -Command "(Get-Content README.md) -replace 'LiftTeam v[0-9]+\.[0-9]+', 'LiftTeam %NEW_VERSION%' | Set-Content README.md" 2>nul || true
powershell -Command "(Get-Content CHANGELOG.md) -replace 'LiftTeam v[0-9]+\.[0-9]+', 'LiftTeam %NEW_VERSION%' | Set-Content CHANGELOG.md" 2>nul || true
powershell -Command "(Get-Content lifteam_launcher.py) -replace 'LiftTeam v[0-9]+\.[0-9]+', 'LiftTeam %NEW_VERSION%' | Set-Content lifteam_launcher.py" 2>nul || true
powershell -Command "(Get-Content start.bat) -replace 'LiftTeam v[0-9]+\.[0-9]+', 'LiftTeam %NEW_VERSION%' | Set-Content start.bat" 2>nul || true
powershell -Command "(Get-Content start.sh) -replace 'LiftTeam v[0-9]+\.[0-9]+', 'LiftTeam %NEW_VERSION%' | Set-Content start.sh" 2>nul || true

echo Version updated to %NEW_VERSION%
