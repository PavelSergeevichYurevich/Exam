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
    id: int
    field: str
    new_value: str
    user_telegram_id: int

class TaskDeleteSchema(BaseModel):
    id: int
    user_telegram_id: int
