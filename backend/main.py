from fastapi import FastAPI
from app.core.database import connect_to_mongo, close_mongo_connection
from app.routers import courses





#weird stuff
from fastapi.middleware.cors import CORSMiddleware






async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield
    await close_mongo_connection()

app = FastAPI(
    title = "Backend API",
    description = "Testing backend API connection to MongoDB",
    version = "0.1.0",
    lifespan = lifespan
)





#weird stuff

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)







app.include_router(courses.router)

@app.get("/")
def read_root():
    return {"message": "Hello from the backend!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.get("/health")
async def read_health():
    await connect_to_mongo()
    return {"status": "healthy"}
