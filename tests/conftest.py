import sys
import os
from httpx import AsyncClient, ASGITransport
import pytest_asyncio
import pytest_asyncio
from sqlalchemy import delete



sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.app.main import app
from src.app.database.base import get_async_session
from src.app.models.task import Task
from src.app.models.user import User


@pytest_asyncio.fixture
async def auth_headers():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        await ac.post("/register", json={
            "username": "nos",
            "email": "nos@example.com",
            "password": "qwer"
        })
        response = await ac.post("/token", data={
            "username": "nos",
            "password": "qwer"
        })
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}


@pytest_asyncio.fixture(autouse=True)
async def clear_db():
    session_gen = get_async_session()
    session = await anext(session_gen)
    try:
        await session.execute(delete(Task))
        await session.execute(delete(User))
        await session.commit()
    finally:
        await session.close()

