from os import getenv
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class Settings:

    DB_ENGINE = "postgresql" # sqlite
    DB_HOST = getenv("DB_HOST", default='pg_db')
    DB_PORT = getenv("DB_PORT", default='5432')
    DB_NAME = getenv("DB_NAME", default='postgres')
    DB_USER = getenv("DB_USER", default='postgres')
    DB_PASSWORD = getenv("DB_PASSWORD", default='secret')

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"