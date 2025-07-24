from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session
from src.app.dao.task import TaskDAO
from src.app.schemas.task import Task, TaskCreate, TaskUpdate
from src.app.core.security import get_current_user
from src.app.models.user import User


router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=Task)
async def create_task(
    task_data: TaskCreate,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    return await TaskDAO.create_with_owner(
        session=session,
        task_data=task_data.model_dump(),
        owner_id=current_user.id
    )


@router.get("/", response_model=list[Task])
async def read_tasks(
    status: str = None,
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    return await TaskDAO.get_user_tasks(
        session=session,
        owner_id=current_user.id,
        status=status,
        skip=skip,
        limit=limit
    )


@router.get("/{task_id}", response_model=Task)
async def read_task(
    task_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    task = await TaskDAO.get_user_task(session, task_id, current_user.id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task


@router.put("/{task_id}", response_model=Task)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    task = await TaskDAO.update_user_task(
        session=session,
        task_id=task_id,
        owner_id=current_user.id,
        update_data=task_data.model_dump(exclude_unset=True)
    )
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task


@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    success = await TaskDAO.delete_user_task(
        session=session,
        task_id=task_id,
        owner_id=current_user.id
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return {"message": "Task deleted successfully"}
