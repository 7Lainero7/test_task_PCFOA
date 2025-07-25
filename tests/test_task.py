import pytest
from httpx import AsyncClient, ASGITransport
from src.app.main import app


@pytest.mark.asyncio
async def test_task_crud(auth_headers):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Создание задачи
        task_data = {
            "title": "Test Task",
            "description": "This is a test task"
        }
        response = await ac.post("/tasks/", json=task_data, headers=auth_headers)
        assert response.status_code == 200
        task = response.json()
        task_id = task["id"]
        assert task["title"] == "Test Task"

        # Получение задачи
        response = await ac.get(f"/tasks/{task_id}", headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["title"] == "Test Task"

        # Обновление задачи
        update_data = {
            "title": "Updated Task",
            "description": "Updated description"
        }
        response = await ac.put(f"/tasks/{task_id}", json=update_data, headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["title"] == "Updated Task"

        # Удаление задачи
        response = await ac.delete(f"/tasks/{task_id}", headers=auth_headers)
        assert response.status_code == 200

        # Проверка, что задача удалена
        response = await ac.get(f"/tasks/{task_id}", headers=auth_headers)
        assert response.status_code == 404
