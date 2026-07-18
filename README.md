# LiftTeam v2.5.1.1

Система управления заказами на ремонт лифтов и складом радиодеталей.

## Быстрый старт

### Windows (Standalone)
```cmd
cd %USERPROFILE%\Downloads\Lifteam
python lifteam_launcher.py
```

### Linux / macOS (Standalone)
```bash
cd ~/Downloads/Lifteam
python3 lifteam_launcher.py
```

### Docker
```bash
cd ~/Downloads/Lifteam
./start.sh
```

## Логин по умолчанию
- **Логин:** `admin`
- **Пароль:** `admin123`

## Стек
- Python 3.12, Django 5.1, DRF 3.17
- Bootstrap 5, vanilla JS
- SQLite (standalone) / PostgreSQL 15 (Docker)
- Redis 7 (опционально), Django Channels, WebSocket
- Nginx (reverse proxy)

## Развёртывание из .bundle

### 1. Распаковка (Windows)
```cmd
cd %USERPROFILE%\Downloads
mkdir Lifteam
cd Lifteam
git clone ..\lifteam-v2.5.1.bundle .
python lifteam_launcher.py
```

### 2. Распаковка (Linux/macOS)
```bash
cd ~/Downloads
mkdir Lifteam && cd Lifteam
git clone ../lifteam-v2.5.1.bundle .
python3 lifteam_launcher.py
```

### 3. Обновление на GitHub
```cmd
cd %USERPROFILE%\Downloads\Lifteam
push_to_github.bat
```

Или вручную:
```cmd
git remote set-url origin https://TOKEN@github.com/yachtsman13/Lifteam.git
git push -u origin main --force
git remote set-url origin https://github.com/yachtsman13/Lifteam.git
```

## Автор
yachtsman13 — https://github.com/yachtsman13/Lifteam


## Примечание: jsDelivr кэширование
После push на GitHub jsDelivr CDN может показывать старые файлы до 24 часов.
Проверяйте актуальность кода через GitHub Web: https://github.com/yachtsman13/Lifteam
