from datetime import datetime

from pydantic import BaseModel, Field

from app.models.common import MongoModel, PyObjectId, utc_now


class AnnouncementCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    body: str = Field(min_length=1)


class AnnouncementUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    body: str | None = Field(default=None, min_length=1)


class AnnouncementInDB(MongoModel):
    course_id: PyObjectId
    author_id: PyObjectId
    title: str
    body: str
    created_at: datetime = Field(default_factory=utc_now)


class AnnouncementResponse(AnnouncementInDB):
    author_name: str
