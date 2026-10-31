from datetime import datetime

from pydantic import BaseModel, Field

from app.models.common import MongoModel, PyObjectId, utc_now


class CourseCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    code: str = Field(min_length=1, max_length=20)  # e.g. "MATH 1431"
    description: str | None = None
    term: str | None = None  # e.g. "Fall 2026"


class CourseUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    code: str | None = Field(default=None, min_length=1, max_length=20)
    description: str | None = None
    term: str | None = None


class CourseInDB(MongoModel):
    name: str
    code: str
    description: str | None = None
    term: str | None = None
    instructor_id: PyObjectId
    # Each course has one syllabus, so it is stored on the course itself
    syllabus: str | None = None
    syllabus_updated_at: datetime | None = None
    created_at: datetime = Field(default_factory=utc_now)


# What the dashboard's CourseCard receives
class CourseResponse(MongoModel):
    name: str
    code: str
    description: str | None = None
    term: str | None = None
    instructor_name: str


class SyllabusUpdate(BaseModel):
    content: str


class SyllabusResponse(BaseModel):
    course_id: PyObjectId
    content: str | None = None
    updated_at: datetime | None = None


# Links a student to a course; only used inside the backend
class EnrollmentInDB(MongoModel):
    user_id: PyObjectId
    course_id: PyObjectId
    enrolled_at: datetime = Field(default_factory=utc_now)
