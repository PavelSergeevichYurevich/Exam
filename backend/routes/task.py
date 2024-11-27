from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, Request
from starlette import status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session
from models.models import Task
from dependencies.dependency import get_db
from models.models import Task, User
from schemas.schemas import TaskCreateSchema, TaskUpdateSchema, TaskDeleteSchema
import sys
sys.path.append('../')
from bot.bot import bot


task_router = APIRouter(
    prefix='/task',
    tags=['Tasks']
)
templates = Jinja2Templates(directory="templates")

@task_router.get("/show/{user_telegram_id}")
async def get_tasks(request:Request, user_telegram_id:int, db: Session = Depends(get_db)):
    stmnt = select(Task).where(Task.user_telegram_id == user_telegram_id)
    tasks:list = db.scalars(stmnt).all()
    return tasks

@task_router.get("/showactive/{user_telegram_id}")
async def get_tasks(request:Request, user_telegram_id:int, db: Session = Depends(get_db)):
    stmnt = select(Task).where(Task.user_telegram_id == user_telegram_id).where(Task.status == 'Active')
    tasks:list = db.scalars(stmnt).all()
    return tasks

@task_router.get("/showclosed/{user_telegram_id}")
async def get_tasks(request:Request, user_telegram_id:int, db: Session = Depends(get_db)):
    stmnt = select(Task).where(Task.user_telegram_id == user_telegram_id).where(Task.status == 'Closed')
    tasks:list = db.scalars(stmnt).all()
    return tasks

@task_router.post("/add/")
async def add_task(request:Request, task: TaskCreateSchema, db: Session = Depends(get_db)):
    username = task.username
    stmnt = select(User).where(User.username == username)
    user = db.execute(stmnt).one()
    user_id = user[0].id
    user_telegram_id = user[0].telegram_id
    status = 'Active'
    new_task = Task(
        task = task.task,
        describe = task.describe,
        ex_date = task.ex_date,
        status = status,
        user_telegram_id = user_telegram_id,
        user_id = user_id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    text = f'У вас новая задача!\nЗадача:\t{task.task}\nОписание:\t{task.describe}\nСрок:\t{task.ex_date}\nСтатус:\t{status}'
    await bot.send_message(user_telegram_id, text)
    return RedirectResponse(url=f"/tasks/{username}")


@task_router.delete('/delete/')
async def del_task(request:Request, task: TaskDeleteSchema, db: Session = Depends(get_db)):
    username = task.username
    stmnt = select(User).where(User.username == username)
    user = db.execute(stmnt).one()
    user_telegram_id = user[0].telegram_id
    stmnt = select(Task).where(Task.id == task.id)
    task = db.execute(stmnt).one()[0]
    text = f'Удалена задача.\nЗадача:\t{task.task}\nОписание:\t{task.describe}\nСрок:\t{task.ex_date}'
    await bot.send_message(user_telegram_id, text)
    stmnt = delete(Task).where(Task.id == task.id)
    task = db.execute(stmnt)
    db.commit()
    return RedirectResponse(url=f"/tasks/{username}", status_code=status.HTTP_302_FOUND)


@task_router.put('/update/')
async def update_task(request:Request, updating_task: TaskUpdateSchema, db: Session = Depends(get_db)):
    field = updating_task.field
    match field:
        case 'task':
            stmnt = update(Task).where(Task.id == updating_task.id).values(
                task = updating_task.new_value
            )
            updated_task = db.execute(stmnt)
            db.commit()
        case 'describe':
            stmnt = update(Task).where(Task.id == updating_task.id).values(
                describe = updating_task.new_value
            )
            updated_task = db.execute(stmnt)
            db.commit()
        case 'ex_date':
            stmnt = update(Task).where(Task.id == updating_task.id).values(
                ex_date = updating_task.new_value
            )
            updated_task = db.execute(stmnt)
            db.commit()
        case 'status':
            stmnt = update(Task).where(Task.id == updating_task.id).values(
                status = updating_task.new_value
            )
            updated_task = db.execute(stmnt)
            db.commit()
    stmnt = select(User).where(User.username == updating_task.username)
    user = db.execute(stmnt).one()
    user_telegram_id = user[0].telegram_id
    stmnt = select(Task).where(Task.id == updating_task.id)
    task = db.execute(stmnt).one()
    text = f'У вас изменения в задаче {task[0].describe}\n{updating_task.field}:\t{updating_task.new_value}'
    await bot.send_message(user_telegram_id, text)
    return updated_task







    
