from typing import Annotated

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from src.app.config import Settings

if Settings.DB_ENGINE == "postgresql":
    DATABASE_URL = Settings.DATABASE_URL
    engine = create_async_engine(DATABASE_URL, echo=True)
    SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

elif Settings.DB_ENGINE == "sqlite":
    from sqlalchemy import create_engine
    SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

metadata_obj = MetaData(schema="PCF")


class BaseModel(DeclarativeBase):
    metadata = metadata_obj