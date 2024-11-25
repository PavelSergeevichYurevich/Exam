from pydantic import BaseModel
from typing import Optional

class UserCreateSchema(BaseModel):
    telegram_id: int
    hashed_password: Optional[str] = None
    
class UserChangeSchema(BaseModel):
    telegram_id: Optional[int] = None
    password: Optional[str] = None
    
class TaskCreateSchema(BaseModel):
    task: str
    describe: str
    ex_date: str
    user_telegram_id: int
    
class TaskUpdateSchema(BaseModel):
    task: Optional[str] = None
    describe: Optional[str] = None
    ex_date: Optional[str] = None
    user_telegram_id: Optional[int] = None

class TaskDeleteSchema(BaseModel):
    id: int
    user_telegram_id: int
