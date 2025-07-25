import pytest
from httpx import ASGITransport, AsyncClient

from src.app.main import app


@pytest.mark.asyncio
async def test_register_and_login():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post(
            "/register",
            json={"username": "nos", "email": "nos@example.com", "password": "qwer"},
        )
        print("REGISTER RESPONSE:", response.status_code, response.json())
        assert response.status_code == 200

        response = await ac.post("/token", data={"username": "nos", "password": "qwer"})
        print("TOKEN RESPONSE:", response.status_code, response.json())
        assert response.status_code == 200
        token = response.json()["access_token"]

        headers = {"Authorization": f"Bearer {token}"}
        response = await ac.get("/me", headers=headers)
        assert response.status_code == 200
        assert response.json()["username"] == "nos"
