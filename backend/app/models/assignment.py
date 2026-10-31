from datetime import datetime

from pydantic import BaseModel, Field

from app.models.common import MongoModel, PyObjectId, utc_now


class AssignmentCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    due_date: datetime
    points: int | None = Field(default=None, ge=0)


class AssignmentUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    due_date: datetime | None = None
    points: int | None = Field(default=None, ge=0)


class AssignmentInDB(MongoModel):
    course_id: PyObjectId
    title: str
    description: str | None = None
    due_date: datetime
    points: int | None = None
    created_at: datetime = Field(default_factory=utc_now)


class AssignmentResponse(AssignmentInDB):
    pass
