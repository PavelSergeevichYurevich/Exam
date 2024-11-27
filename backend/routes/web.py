from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import select
from models.models import User


from dependencies.dependency import get_db


web_router = APIRouter()
templates = Jinja2Templates(directory="templates")

@web_router.get('/')
async def index(request: Request):
    return templates.TemplateResponse(request=request, name='index.html')

@web_router.get("/login/")
async def login(request:Request):
    return templates.TemplateResponse(request=request, name="login.html")

@web_router.get("/users/", response_class = HTMLResponse)
async def get_users_page(request:Request, db: Session = Depends(get_db)):
    stmnt = select(User)
    users:list = db.scalars(stmnt).all()
    context:dict = {}
    i:int = 1
    for user in users:
        new_el = {str(i): user.username}
        context.update(new_el)
        i += 1
    return templates.TemplateResponse("users.html", {"request": request, "context": context})

@web_router.get("/register/")
async def login(request:Request):
    return templates.TemplateResponse(request=request, name="register.html")

@web_router.get("/tasks/{username}")
async def get_tasks_page(request:Request, username:str, db: Session = Depends(get_db)):
    stmnt = select(User).where(User.username == username)
    context = db.scalars(stmnt).one()
    return templates.TemplateResponse("tasks.html", {"request": request, "context": context})




