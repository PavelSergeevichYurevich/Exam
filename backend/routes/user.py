from datetime import datetime
from typing import Annotated, List
from fastapi import APIRouter, Depends, Request, status, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session
from routes.auth import hashing_pass
from dependencies.dependency import get_db
from models.models import User
from schemas.schemas import UserChangeSchema, UserCreateSchema, UserCreateTlgSchema

user_router = APIRouter(
    prefix='/user',
    tags=['Users']
)
templates = Jinja2Templates(directory="templates")

# вывести пользoвателей
@user_router.get("/show/", response_model=List[UserCreateSchema])
async def get_customers(request:Request, db: Session = Depends(get_db)):
    stmnt = select(User)
    users:list = db.scalars(stmnt).all()
    return users

# создать пользователя
@user_router.post("/add/")
async def add_user(request:Request, username: Annotated[str, Form()], password: Annotated[str, Form()], telegram_id: Annotated[int, Form()], db: Session = Depends(get_db)):
    hashed_password = hashing_pass(password)
    new_user = User(
        telegram_id = telegram_id,
        username = username,
        hashed_password = hashed_password,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return RedirectResponse(url="/login/", status_code=status.HTTP_302_FOUND)

@user_router.post("/add_tlg/")
async def add_user(request:Request, user: UserCreateTlgSchema, db: Session = Depends(get_db)):
    hashed_password = hashing_pass(user.password)
    new_user = User(
        telegram_id = user.telegram_id,
        username = user.username,
        hashed_password = hashed_password,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# изменить пользователя
@user_router.put(path='/update/')
async def change_user(request:Request, user_id:int, user_upd: UserChangeSchema, db: Session = Depends(get_db)):
    if user_upd.telegram_id:
        stmnt = update(User).where(User.id == user_id).values(
            telegram_id = user_upd.telegram_id
        )
        user = db.execute(stmnt)
        db.commit()
    if user_upd.username:
        stmnt = update(User).where(User.id == user_id).values(
            username = user_upd.username
        )
        user = db.execute(stmnt)
        db.commit()
    if user_upd.password:
        hashed_password = hashing_pass(user_upd.password)
        stmnt = update(User).where(User.id == user_id).values(
            hashed_password = hashed_password
        )
        user = db.execute(stmnt)
        db.commit()
    return user

# удалить пользователя
@user_router.delete(path='/delete/')
async def del_user(request:Request, id:int, db: Session = Depends(get_db)):
    stmnt = delete(User).where(User.id == id)
    user = db.execute(stmnt)
    db.commit()
    return user