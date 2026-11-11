from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core import db
from app.routers import assignments, auth, classes, courses, submissions



@asynccontextmanager
async def lifespan(app: FastAPI):
    db.connect()
    await db.create_indexes()
    yield
    db.disconnect()


app = FastAPI(title="AI Course Management", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(courses.router)
app.include_router(classes.router)
app.include_router(assignments.router)
app.include_router(submissions.router)


@app.get("/health", tags=["meta"])
def health():
    return {"status": "ok"}
