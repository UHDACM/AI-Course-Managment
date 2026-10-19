from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core import database

async def lifespan(app: FastAPI):
    await core.database.connect_to_mongo()
    yield
    await core.database.close_mongo_connection()

app = FastAPI(
    title = "Backend API",
    description = "Testing backend API connection to MongoDB",
    version = "0.1.0",
    lifespan = lifespan
)

@app.get("/")
def read_root():
    return {"message": "Hello from the backend!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.get("/health")
def read_health():
    connect_to_mongo()
    return {"status": "healthy"}