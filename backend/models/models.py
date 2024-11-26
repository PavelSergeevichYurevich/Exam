from typing import List
from sqlalchemy import ForeignKey
from database.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    telegram_id: Mapped[int] = mapped_column(unique=True)
    username: Mapped[str]
    hashed_password: Mapped[str]
    tasks: Mapped[List["Task"]] = relationship(back_populates='user', cascade='save-update, merge, delete', passive_deletes=True)
        
class Task(Base):
    __tablename__ = "task"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    task: Mapped[str]
    describe: Mapped[str]
    ex_date: Mapped[str]
    status: Mapped[str]
    user_telegram_id: Mapped[int]
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'), index=True)
    user: Mapped["User"] = relationship(back_populates="tasks")

    