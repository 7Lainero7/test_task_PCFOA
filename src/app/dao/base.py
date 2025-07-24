from typing import Type, TypeVar
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar('ModelType')

class BaseDAO:
    model: Type[ModelType] = None

    @classmethod
    async def get_by_id(cls, session: AsyncSession, id: int):
        query = select(cls.model).where(cls.model.id == id)
        result = await session.execute(query)
        return result.scalars().first()

    @classmethod
    async def get_all(cls, session: AsyncSession, **filters):
        query = select(cls.model)
        if filters:
            query = query.filter_by(**filters)
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def create(cls, session: AsyncSession, **data):
        instance = cls.model(**data)
        session.add(instance)
        await session.commit()
        await session.refresh(instance)
        return instance

    @classmethod
    async def update(cls, session: AsyncSession, id: int, **data):
        query = (
            update(cls.model)
            .where(cls.model.id == id)
            .values(**data)
            .returning(cls.model)
        )
        result = await session.execute(query)
        await session.commit()
        return result.scalars().first()

    @classmethod
    async def delete(cls, session: AsyncSession, id: int):
        query = delete(cls.model).where(cls.model.id == id)
        await session.execute(query)
        await session.commit()
        return True
