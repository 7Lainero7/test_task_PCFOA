from typing import List
from datetime import datetime
from sqlalchemy import String, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from src.app.database import BaseModel

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
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