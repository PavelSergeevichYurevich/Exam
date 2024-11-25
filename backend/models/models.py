from typing import List
from sqlalchemy import ForeignKey
from database.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(unique=True)
    username: Mapped[str]
    hashed_password: Mapped[str]
    tasks: Mapped[List["Task"]] = relationship(back_populates='user', cascade='save-update, merge, delete')
        
class Task(Base):
    __tablename__ = "task"
    id: Mapped[int] = mapped_column(primary_key=True)
    task: Mapped[str]
    describe: Mapped[str]
    ex_date: Mapped[str]
    user_telegram_id: Mapped[str] = mapped_column(ForeignKey('user.telegram_id'))
    user: Mapped["User"] = relationship(back_populates="tasks")

    
    
    
    
    
    
    
    
    