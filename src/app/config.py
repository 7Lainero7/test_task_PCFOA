from os import getenv

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())


class Settings:
    DB_ENGINE = getenv("DB_ENGINE", default="postgresql")  # или "sqlite"
    DB_HOST = getenv("DB_HOST", default="localhost")
    DB_PORT = getenv("DB_PORT", default="5432")
    DB_NAME = getenv("DB_NAME", default="postgres")
    DB_USER = getenv("DB_USER", default="postgres")
    DB_PASSWORD = getenv("DB_PASSWORD", default="qwer")
    DB_SCHEME = getenv("DB_SCHEME", default="PCF")

    @property
    def DATABASE_URL(self) -> str:
        if self.DB_ENGINE == "sqlite":
            return "sqlite+aiosqlite:///./sql_app.db"
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    SECRET_KEY = getenv("SECRET_KEY", default="SECRET_KEY")
    ALGORITHM = getenv("ALGORITHM", default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = 30


settings = Settings()
