from pydantic import BaseModel
from typing import Optional

class UserCreateSchema(BaseModel):
    telegram_id: int
    username: str
    hashed_password: Optional[str] = None
    
class UserCreateTlgSchema(BaseModel):
    telegram_id: int
    username: str
    password: str
    
class UserChangeSchema(BaseModel):
    telegram_id: Optional[int] = None
    username: Optional[str] = None
    password: Optional[str] = None
    
class TaskCreateSchema(BaseModel):
    task: str
    describe: str
    ex_date: str
    status: str = 'Active'
    user_telegram_id: int
    
class TaskUpdateSchema(BaseModel):
    task: Optional[str] = None
    describe: Optional[str] = None
    ex_date: Optional[str] = None
    status: Optional[str] = 'Active'
    user_id: Optional[int] = None

class TaskDeleteSchema(BaseModel):
    id: int
    user_telegram_id: int
