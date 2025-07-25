from __future__ import annotations
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.app.database.base import BaseModel
from src.app.schemas.task import TaskStatus


class Task(BaseModel):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), index=True)
    description: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default=TaskStatus.pending.value
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    owner: Mapped["User"] = relationship(back_populates="tasks")

    def __repr__(self) -> str:
        return (
            f"Task(id={self.id!r}, title={self.title!r}, "
            f"status={self.status!r}, owner_id={self.owner_id!r})"
        )
