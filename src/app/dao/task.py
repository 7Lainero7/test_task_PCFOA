from sqlalchemy import and_, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.dao.base import BaseDAO
from src.app.models.task import Task
from src.app.schemas.task import TaskStatus

class TaskDAO(BaseDAO):
    model = Task

    @classmethod
    async def get_user_task(
        cls, 
        session: AsyncSession, 
        task_id: int, 
        owner_id: int
    ):
        query = select(cls.model).where(
            and_(
                cls.model.id == task_id,
                cls.model.owner_id == owner_id
            )
        )
        result = await session.execute(query)
        return result.scalars().first()

    @classmethod
    async def get_user_tasks(
        cls,
        session: AsyncSession,
        owner_id: int,
        status: TaskStatus = None,
        skip: int = 0,
        limit: int = 100
    ):
        query = select(cls.model).where(
            cls.model.owner_id == owner_id
        ).offset(skip).limit(limit)
        
        if status:
            query = query.where(cls.model.status == status)
            
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def create_with_owner(
        cls,
        session: AsyncSession,
        task_data: dict,
        owner_id: int
    ):
        task_data["owner_id"] = owner_id
        return await super().create(session, **task_data)

    @classmethod
    async def update_user_task(
        cls,
        session: AsyncSession,
        task_id: int,
        owner_id: int,
        update_data: dict
    ):
        query = (
            update(cls.model)
            .where(
                and_(
                    cls.model.id == task_id,
                    cls.model.owner_id == owner_id
                )
            )
            .values(**update_data)
            .returning(cls.model)
        )
        result = await session.execute(query)
        await session.commit()
        return result.scalars().first()

    @classmethod
    async def delete_user_task(
        cls,
        session: AsyncSession,
        task_id: int,
        owner_id: int
    ):
        query = delete(cls.model).where(
            and_(
                cls.model.id == task_id,
                cls.model.owner_id == owner_id
            )
        )
        await session.execute(query)
        await session.commit()
        return True
