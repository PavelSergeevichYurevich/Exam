from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session
from models.models import Task
from dependencies.dependency import get_db
from models.models import Task
from schemas.schemas import TaskCreateSchema, TaskUpdateSchema
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
    new_task = Task(
        task = task.task,
        describe = task.describe,
        ex_date = task.ex_date,
        status = task.status,
        user_telegram_id = task.user_telegram_id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    text = f'У вас новая задача!\nЗадача:\t{task.task}\nОписание:\t{task.describe}\nСрок:\t{task.ex_date}\nСтатус:\t{task.status}'
    await bot.send_message(task.user_telegram_id, text)
    return new_task
    # return RedirectResponse(url="/app/login/", status_code=status.HTTP_302_FOUND)

@task_router.delete(path='/delete/')
async def del_task(request:Request, id:int, db: Session = Depends(get_db)):
    stmnt = delete(Task).where(Task.id == id)
    task = db.execute(stmnt)
    db.commit()
    return task

@task_router.put(path='/update/')
async def update_task(request:Request, task_id: int, updating_task: TaskUpdateSchema, db: Session = Depends(get_db)):
    if updating_task.task:
        stmnt = update(Task).where(Task.id == task_id).values(
            task = updating_task.task
        )
        updated_task = db.execute(stmnt)
        db.commit()
        
    if updating_task.describe:
        stmnt = update(Task).where(Task.id == task_id).values(
            describe = updating_task.describe
        )
        updated_task = db.execute(stmnt)
        db.commit()
        
    if updating_task.ex_date:
        stmnt = update(Task).where(Task.id == task_id).values(
            ex_date = updating_task.ex_date
        )
        updated_task = db.execute(stmnt)
        db.commit()
        
    if updating_task.status:
        stmnt = update(Task).where(Task.id == task_id).values(
            status = updating_task.status
        )
        updated_task = db.execute(stmnt)
        db.commit()
        
    if updating_task.user_telegram_id:
        stmnt = update(Task).where(Task.id == task_id).values(
            user_telegram_id = updating_task.user_telegram_id
        )
        updated_task = db.execute(stmnt)
        db.commit()
        
    text = f'У вас изменения в задаче!\nЗадача:\t{updating_task.task}\nОписание:\t{updating_task.describe}\nСрок:\t{updating_task.ex_date}\nСтатус:\t{updating_task.status}'
    await bot.send_message(updating_task.user_telegram_id, text)
    return updated_task







    
