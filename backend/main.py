from fastapi import FastAPI
from database import Base, SessionLocal, engine
import models  # must be imported so Base knows about the Class table

app = FastAPI()


Base.metadata.create_all(bind=engine)  # creates blog.db and the classes table

with SessionLocal() as db:
    new_class = models.Class(classname="CS 1402", assignment1="Make a program")
    db.add(new_class)
    db.commit()
    db.refresh(new_class)  # loads the generated class_id
    print(new_class.class_id)