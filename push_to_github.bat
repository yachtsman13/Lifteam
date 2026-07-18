@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo.
echo   ================================================
echo    LiftTeam v2.5 — Push to GitHub
echo   ================================================
echo.

:: Проверка Git
where git >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo   [ERROR] Git не найден. Установите: https://git-scm.com/download/win
    pause
    exit /b 1
)

:: === ВСЕГДА сбрасываем remote на GitHub ===
echo   [1/6] Настройка remote URL...
git remote remove origin 2>nul
git remote add origin https://github.com/yachtsman13/Lifteam.git
echo   [OK] Remote: https://github.com/yachtsman13/Lifteam.git

:: Проверка .git
if not exist ".git" (
    echo   [ERROR] Не найден .git. Запустите setup_git.bat
    pause
    exit /b 1
)

:: Проверка user.name и user.email
git config user.name >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo   [2/6] Настройка Git identity...
    git config user.name "yachtsman13"
    git config user.email "yachtsman13@github.com"
) else (
    echo   [OK] Git identity: yachtsman13
)

:: Проверка safe.directory
git config --global --get-regexp safe.directory | findstr /C:"%~dp0" >nul
if %ERRORLEVEL% NEQ 0 (
    echo   [3/6] Добавление safe.directory...
    git config --global --add safe.directory "%~dp0"
) else (
    echo   [OK] safe.directory настроен
)

:: Добавление файлов
echo   [4/6] Добавление файлов...
git add -A

:: Коммит
echo   [5/6] Создание коммита...
git commit -m "LiftTeam v2.5 update" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo   [INFO] Нет изменений для коммита (или коммит уже есть)
)

:: Проверка интернет-соединения
echo   [6/6] Проверка соединения с GitHub...
ping -n 1 github.com >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo   [ERROR] GitHub недоступен. Проверьте интернет-соединение или VPN.
    echo   Код ошибки: Could not resolve host: github.com
    echo.
    echo   Решения:
    echo     1. Включите VPN
    echo     2. Смените DNS на 8.8.8.8
    echo     3. Загрузите файлы вручную через GitHub Web
    pause
    exit /b 1
)

:: Пуш
echo.
echo   Отправка на GitHub...
echo   Введите логин GitHub и Personal Access Token когда запросит.
echo.
git push -u origin main --force

if %ERRORLEVEL% EQU 0 (
    echo.
    echo   [OK] Успешно отправлено на https://github.com/yachtsman13/Lifteam
    echo   Проверьте: https://github.com/yachtsman13/Lifteam
) else (
    echo.
    echo   [ERROR] Ошибка отправки.
    echo.
    echo   Решение: создайте Personal Access Token:
    echo     https://github.com/settings/tokens ^> Generate new token
    echo     Права: repo (полный доступ к репозиториям)
    echo.
    echo   Затем выполните:
    echo     git remote set-url origin https://TOKEN@github.com/yachtsman13/Lifteam.git
    echo     git push -u origin main --force
    echo     git remote set-url origin https://github.com/yachtsman13/Lifteam.git
)

echo.
pause
