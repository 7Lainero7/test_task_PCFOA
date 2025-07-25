#!/bin/bash
set -e

# Ждём, пока Postgres поднимется
echo "⏳ Waiting for PostgreSQL..."
sleep 3

# Применяем миграции
echo "📦 Running Alembic migrations..."
alembic upgrade head

# Запускаем приложение
echo "🚀 Starting FastAPI..."
exec uvicorn src.app.main:app --host 0.0.0.0 --port 8000 --reload
