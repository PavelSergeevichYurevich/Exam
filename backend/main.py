from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import uvicorn
from database.database import engine, Base
from models.models import User, Test, Qa
from routes import auth, user, test, start

app = FastAPI(title='Opros')
app.include_router(auth.auth_router)
app.include_router(start.start_router)
app.include_router(user.user_router)
app.include_router(test.test_router)
app.mount("/static", StaticFiles(directory=Path(__file__).parent.absolute() / "static"), name="static")
Base.metadata.create_all(bind=engine)


""" HOST = '0.0.0.0'
if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
    print('Starting server')
    uvicorn.run('main:app', port=8000, host=HOST, reload=True)
    print('Server stopped') """