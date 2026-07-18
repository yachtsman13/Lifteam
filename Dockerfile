# LiftTeam v2.2 — Docker-контейнер
# Использование: docker build -t lifteam .
#               docker run -p 8000:8000 lifteam

FROM python:3.12-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Рабочая директория
WORKDIR /app

# Копирование зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование проекта
COPY . .

# Создание .env из примера (если нет)
RUN if [ ! -f .env ]; then cp .env.example .env; fi

# Миграции и инициализация (выполняются при старте контейнера, не при сборке)
# RUN python manage.py migrate
# RUN python manage.py init_cells

# Статические файлы
RUN python manage.py collectstatic --noinput

# Порт
EXPOSE 8000

# Запуск
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "lifteam.wsgi:application"]
