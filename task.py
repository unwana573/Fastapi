from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import database

@asynccontextmanager
async def lifespan(app:FastAPI):
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(title="Todoapp", lifespan=lifespan)
