# 📝 Task Manager API

Простой REST API сервис для управления списком задач. Реализован на FastAPI с поддержкой авторизации, миграций, тестов и Docker.

---

## 🚀 Возможности

- ✅ Создание задач (`title`, `description`, `status`)
- ✅ Просмотр списка задач с фильтрацией по статусу
- ✅ Обновление и удаление задач
- ✅ JWT-авторизация
- ✅ Swagger-документация (`/docs`)
- ✅ Alembic миграции
- ✅ Docker-окружение
- ✅ Тесты с `pytest`, `httpx`, `pytest-asyncio`

---

## 📦 Установка и запуск

### 1. Клонируй репозиторий

```bash
git clone https://github.com/7Lainero7/test_task_PCFOA.git
cd test_task_PCFOA
```

### 2. Создайте .env

 #### Для локального запуска:
 ```
    DB_ENGINE=postgresql
    DB_HOST=localhost
    DB_PORT=5432
    DB_NAME=postgres
    DB_USER=postgres
    DB_PASSWORD=qwer
    SECRET_KEY=SECRET_KEY
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    DB_SCHEME=PCF
 ```

 #### Для Docker:
 ```
    DB_ENGINE=postgresql
    DB_HOST=db
    DB_PORT=5432
    DB_NAME=tasks_db
    DB_USER=postgres
    DB_PASSWORD=postgres
    SECRET_KEY=SECRET_KEY
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    DB_SCHEME=PCF
 ```


### 3. Запусти через Docker

```bash
docker-compose up --build
```

### 4. Документация

- Swagger: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🧪 Тесты

```bash
pytest
```

---

## ⚙️ Миграции

```bash
alembic revision --autogenerate -m "init"
alembic upgrade head
```

---

## 🔐 Авторизация

- Регистрация: `POST /register` через json!
- Получение токена: `POST /token` через form-data!
- Использование: `Authorization: Bearer <token>`

---

## 📁 Структура проекта

```
src/
├── app/
│   ├── core/         # Безопасность, конфигурация
│   ├── dao/          # Доступ к данным
│   ├── database/     # Подключение к БД
│   ├── models/       # SQLAlchemy модели
│   ├── routes/       # API роуты
│   ├── schemas/      # Pydantic схемы
│   └── main.py       # Точка входа
tests/
├── test_user.py
├── test_task.py
└── conftest.py
```

---

## 📄 Лицензия

MIT
