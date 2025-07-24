from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.database.base import get_async_session
from src.app.dao.user import UserDAO
from src.app.schemas.user import UserCreate, UserInDB
from src.app.core.security import (
    authenticate_user,
    create_access_token,
    get_current_user,
)


router = APIRouter(tags=["auth"])


@router.post("/register", response_model=UserInDB)
async def register(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_async_session)
):
    existing_user = await UserDAO.get_by_username(session, user_data.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    if user_data.email:
        existing_email = await UserDAO.get_by_email(session, user_data.email)
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    user = await UserDAO.create_user(session, user_data.model_dump())
    return user


@router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_async_session)
):
    user = await authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserInDB)
async def read_users_me(
    current_user: UserInDB = Depends(get_current_user)
):
    return current_user
