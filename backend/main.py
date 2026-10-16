from fastapi import FastAPI
from database import Base, SessionLocal, engine
import models  # must be imported so Base knows about the Class table

app = FastAPI()


Base.metadata.create_all(bind=engine)  # creates blog.db and the classes table
