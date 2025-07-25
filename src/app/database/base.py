from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from src.app.config import settings

if settings.DB_ENGINE == "postgresql":
    DATABASE_URL = settings.DATABASE_URL
    engine = create_async_engine(DATABASE_URL, echo=True)
    SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

elif settings.DB_ENGINE == "sqlite":
    from sqlalchemy import create_engine

    engine = create_engine(
        settings.DATABASE_URL, connect_args={"check_same_thread": False}
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

metadata_obj = MetaData(schema=settings.DB_SCHEME)


class BaseModel(DeclarativeBase):
    metadata = metadata_obj


async def get_async_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session
