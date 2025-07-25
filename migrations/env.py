import sys
import os
from logging.config import fileConfig
from os.path import abspath, dirname
from alembic import context
from sqlalchemy import engine_from_config, pool, text

sys.path.insert(0, dirname(dirname(dirname(abspath(__file__)))))

from src.app.config import settings
from src.app.database.base import BaseModel
from src.app.models.task import Task
from src.app.models.user import User

# Alembic config
config = context.config
SYNC_DATABASE_URL = settings.DATABASE_URL.replace("asyncpg", "psycopg2")
config.set_main_option("sqlalchemy.url", SYNC_DATABASE_URL)

SCHEMA = settings.DB_SCHEME or "public"
config.set_main_option("DB_SCHEME", SCHEMA)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = BaseModel.metadata
print("SYNC_DATABASE_URL =", SYNC_DATABASE_URL)
print("TARGET SCHEMA =", SCHEMA)

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        render_as_batch=True,
        version_table_schema=SCHEMA
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        print(f"Creating schema if not exists: {SCHEMA}")
        connection.execution_options(isolation_level="AUTOCOMMIT").execute(
            text(f'CREATE SCHEMA IF NOT EXISTS "{SCHEMA}"')
        )

        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            render_as_batch=True,
            version_table_schema=SCHEMA
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
