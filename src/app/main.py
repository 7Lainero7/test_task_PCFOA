from fastapi import FastAPI

from src.app.database.base import BaseModel, engine
from src.app.routes import task, user

app = FastAPI(title="Test_task")

app.include_router(user.router)
app.include_router(task.router)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)


@app.get("/")
async def root():
    return {"message": "Pim pim pam pam"}
