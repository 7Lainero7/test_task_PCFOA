from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context
import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.app.config import Settings
from src.app.database.base import Base
from src.app.models.task import Task
from src.app.models.user import User

settings = Settings()

config = context.config
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)
fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline():
    """Запуск миграций в offline режиме."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        render_as_batch=True  # Важно для SQLite
    )

    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection):
    context.configure(
        connection=connection, 
        target_metadata=target_metadata,
        compare_type=True,
        render_as_batch=True
    )

    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online():
    """Запуск миграций в online режиме."""
    connectable = create_async_engine(
        config.get_main_option("sqlalchemy.url"),
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())