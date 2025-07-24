from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.dao.base import BaseDAO
from src.app.models.user import User


class UserDAO(BaseDAO):
    model = User

    @classmethod
    async def get_by_username(cls, session: AsyncSession, username: str):
        query = select(cls.model).where(cls.model.username == username)
        result = await session.execute(query)
        return result.scalars().first()

    @classmethod
    async def get_by_email(cls, session: AsyncSession, email: str):
        query = select(cls.model).where(cls.model.email == email)
        result = await session.execute(query)
        return result.scalars().first()

    @classmethod
    async def create_user(cls, session: AsyncSession, user_data: dict):
        from src.app.core.security import get_password_hash
        hashed_password = get_password_hash(user_data["password"])
        user_data["hashed_password"] = hashed_password
        del user_data["password"]
        return await super().create(session, **user_data)

    @classmethod
    async def update_user(
        cls, 
        session: AsyncSession, 
        user_id: int, 
        update_data: dict
    ):
        from src.app.core.security import get_password_hash
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data["password"])
            del update_data["password"]
        return await super().update(session, user_id, **update_data)
