from pydantic import BaseModel
from typing import Optional

class UserCreateSchema(BaseModel):
    username: str
    hashed_password: Optional[str] = None
    telegram_id: int
    
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
    username: str
    
class TaskUpdateSchema(BaseModel):
    id: int
    field: str
    new_value: str
    username: str

class TaskDeleteSchema(BaseModel):
    id: int
    username: str
