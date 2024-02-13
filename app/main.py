from fastapi import FastAPI

from app import models
from app.database import engine
from app.routers import login, users

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(login.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
