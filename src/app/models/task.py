from typing import Optional
from datetime import datetime
from sqlalchemy import ForeignKey, String, Text, Enum, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.app.database import BaseModel
from src.app.schemas.tasks import TaskStatus

class Task(BaseModel):
    __tablename__ = "tasks"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), index=True)
    description: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus), 
        default=TaskStatus.pending
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now()
    )
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    
    owner: Mapped["User"] = relationship(back_populates="tasks")
    
    def __repr__(self) -> str:
        return (
            f"Task(id={self.id!r}, title={self.title!r}, "
            f"status={self.status!r}, owner_id={self.owner_id!r})"
        )