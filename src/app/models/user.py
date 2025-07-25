from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import List, Optional

from src.app.database.base import BaseModel


class User(BaseModel):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[Optional[str]] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now()
    )
    
    tasks: Mapped[List["Task"]] = relationship(
        back_populates="owner", 
        cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r})"
