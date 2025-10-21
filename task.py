from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import database
from sql.create_sql_table import *

@asynccontextmanager
async def lifespan(app:FastAPI):
    await database.connect() 
    await create_tables(database)
    yield
    await database.disconnect()

app = FastAPI(title="Todoapp", lifespan=lifespan)

