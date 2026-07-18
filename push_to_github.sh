#!/bin/bash
# LiftTeam — Push to GitHub (единый скрипт)

cd "$(dirname "$0")"

REPO_URL="https://github.com/yachtsman13/Lifteam.git"

echo ""
echo "  ================================================"
echo "   LiftTeam — Push to GitHub"
echo "  ================================================"
echo ""

# 1. Проверка Git
if ! command -v git &> /dev/null; then
    echo "  [ERROR] Git не найден"
    exit 1
fi

# === ИСПРАВЛЕНИЕ: ВСЕГДА сбрасываем remote ===
echo "  [1/6] Настройка remote URL..."
git remote remove origin 2>/dev/null || true
git remote add origin "$REPO_URL"
echo "  [OK] Remote: $REPO_URL"

# 2. Проверка .git
if [ ! -d ".git" ]; then
    echo "  [ERROR] Не найден .git"
    exit 1
fi

# 3. Git identity
if [ -z "$(git config user.name)" ] || [ -z "$(git config user.email)" ]; then
    echo "  [2/6] Настройка Git identity..."
    git config user.name "yachtsman13"
    git config user.email "yachtsman13@github.com"
else
    echo "  [OK] Git identity: $(git config user.name)"
fi

# 4. Safe directory
if ! git config --global --get-regexp safe.directory | grep -q "$(pwd)"; then
    echo "  [3/6] Добавление safe.directory..."
    git config --global --add safe.directory "$(pwd)"
fi

# 5. Добавление файлов
echo "  [4/6] Добавление файлов..."
git add -A

# 6. Коммит
echo "  [5/6] Создание коммита..."
if git diff --cached --quiet; then
    echo "  [INFO] Нет изменений для коммита"
else
    git commit -m "LiftTeam v2.2.3 update"
    echo "  [OK] Коммит создан"
fi

# 7. Пуш
echo "  [6/6] Отправка на GitHub..."
echo ""
git push -u origin main --force

if [ $? -eq 0 ]; then
    echo ""
    echo "  [OK] Успешно отправлено на $REPO_URL"
else
    echo ""
    echo "  [ERROR] Ошибка отправки."
    echo "  Создайте Personal Access Token: https://github.com/settings/tokens"
    echo "  Права: repo"
    echo ""
    echo "  Затем: git remote set-url origin https://TOKEN@github.com/yachtsman13/Lifteam.git"
fi
