# ПРОМПТ: LiftTeam

## Контекст
Проект LiftTeam — система управления заказами на ремонт лифтов и складом радиодеталей.
Репозиторий: https://github.com/yachtsman13/Lifteam

## Как ИИ читает файлы проекта


### Важно: jsDelivr кэширует файлы
jsDelivr CDN кэширует файлы GitHub на 24 часа. После push на GitHub новые файлы могут не отображаться сразу.

**Решения:**
1. Подождите 10-30 минут после push
2. Используйте параметр очистки кэша: `?nocache=1`
3. Проверяйте через GitHub Web: `https://github.com/yachtsman13/Lifteam/blob/main/...`
4. Используйте raw.githubusercontent.com (если доступен)

**Проверка актуальности:**
Сравните `v2.X` в заголовке файла с версией в репозитории. Если версия отличается — файл закэширован.

### jsDelivr CDN (основной способ)
jsDelivr предоставляет прямой доступ к файлам GitHub-репозитория через CDN:

```
https://cdn.jsdelivr.net/gh/yachtsman13/Lifteam@main/<путь_к_файлу>
```

**Ключевые особенности:**
- Работает даже если GitHub недоступен напрямую
- Кэширует файлы на edge-серверах (Cloudflare, Fastly)
- Если файл удалён — автоматически fallback на предыдущую версию
- Поддерживает директиву `@main` для последнего коммита ветки main
- Для конкретного коммита: `@<commit_hash>`
- Для тега: `@v2.5.1`

**Примеры URL:**
```
https://cdn.jsdelivr.net/gh/yachtsman13/Lifteam@main/lifteam/settings.py
https://cdn.jsdelivr.net/gh/yachtsman13/Lifteam@main/core/models.py
https://cdn.jsdelivr.net/gh/yachtsman13/Lifteam@main/requirements.txt
```

**Ограничения:**
- Файлы > 20 MB могут не загружаться
- Нет доступа к git-истории (только текущие файлы)
- Нельзя просматривать директории — только конкретные файлы

### Git Bundle (для полной работы)
Пользователь присылает файл `.bundle` — это полный git-репозиторий в одном файле.

**Как работать с bundle:**
```bash
# Распаковать
mkdir Lifteam && cd Lifteam
git bundle unbundle lifteam-vX.X.X.bundle

# Или клонировать
mkdir Lifteam && cd Lifteam
git init
git bundle unbundle ../lifteam-vX.X.X.bundle
```

**Преимущества bundle:**
- Полная история коммитов
- Все ветки
- Возможность diff между версиями
- Работа офлайн

## КРИТИЧЕСКОЕ ПРАВИЛО: Нельзя работать над проектом без исходных файлов

**ЗАПРЕЩЕНО:**
- Пытаться вспомнить или восстановить код из памяти
- Создавать "новую версию" с нуля
- Предполагать содержимое файлов без их прочтения
- Использовать устаревшие данные из предыдущих сессий

**ОБЯЗАТЕЛЬНО:**
1. Перед началом работы — прочитать ВСЕ ключевые файлы через jsDelivr
2. Если jsDelivr недоступен — запросить bundle от пользователя
3. Сравнить прочитанный код с тем, что было в предыдущей сессии
4. Вносить изменения только в контексте существующего кода

## Порядок работы над проектом

### 1. Получение актуального состояния
```
1. Прочитать README.md через jsDelivr
2. Прочитать CHANGELOG.md — понять текущую версию
3. Прочитать lifteam/settings.py, core/models.py, core/views.py
4. Прочитать requirements.txt
5. Сравнить с предыдущим состоянием из памяти
```

### 2. Внесение изменений
```
1. Редактировать конкретные файлы
2. Обновить версию во ВСЕХ файлах (update_version.bat/sh)
3. Обновить CHANGELOG.md
4. Обновить PROMPT.md если изменился процесс работы
5. Обновить README.md
```

### 3. Сборка и передача
```
1. Создать git commit
2. Создать git bundle: git bundle create lifteam-vX.X.X.bundle main
3. Прислать bundle пользователю
4. Пользователь распаковывает и продолжает работу
```

## Текущая версия
v2.5.1 — standalone (SQLite) + Docker (PostgreSQL + Redis + Nginx)

## Стек
Python 3.12, Django 5.1, DRF 3.17, Bootstrap 5, vanilla JS
SQLite (dev) / PostgreSQL 15 (prod), Redis 7, Django Channels, WebSocket

## Ключевые правила
1. Employee.USERNAME_FIELD = 'username' (авторизация по логину)
2. Все шаблоны — Bootstrap 5 с sidebar-навигацией
3. Миграции в core/migrations/
4. Служебные файлы ДОЛЖНЫ присутствовать и актуализироваться в каждой версии:
   start.bat/sh, setup_git.bat/sh, push_to_github.bat/sh, fix_git.bat/sh,
   update.bat/sh, update_version.bat/sh, lifteam_launcher.py, TZ, PROMPT, README, CHANGELOG
5. При обновлении версии обновлять номер во ВСЕХ файлах
6. Для обновления версии использовать: update_version.bat [ВЕРСИЯ] или update_version.sh [ВЕРСИЯ]
7. Все .bat и .sh файлы должны содержать cd в папку скрипта (cd /d "%%~dp0" или cd "$(dirname "$0")")
8. setup_git.bat/sh автоматически инициализирует репозиторий и пушит на GitHub с force

## Запуск одним файлом
python lifteam_launcher.py — проверяет Python, pip, устанавливает зависимости,
создаёт БД, администратора, ячейки и запускает сервер.

## Как получить файлы
Через jsDelivr: https://cdn.jsdelivr.net/gh/yachtsman13/Lifteam@main/...
Или git clone https://github.com/yachtsman13/Lifteam.git

## Логотип
Проект использует логотип LiftTeam (круглый, синий, с микросхемой).
Файл логотипа: core/static/img/lift_team_logo.png
Размещён в static/ для отображения в приложении.
