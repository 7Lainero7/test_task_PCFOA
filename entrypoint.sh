#!/bin/bash
set -e

# Ждём PostgreSQL
echo "Waiting for PostgreSQL..."
sleep 3

# Прогоняем миграции
echo "Running Alembic migrations..."
alembic upgrade head

# Запускаем FastAPI
echo "Starting FastAPI..."
exec uvicorn src.app.main:app --host 0.0.0.0 --port 8000
