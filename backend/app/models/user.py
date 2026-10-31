from datetime import datetime
from enum import Enum

from pydantic import BaseModel, EmailStr, Field

from app.models.common import MongoModel, utc_now


class Role(str, Enum):
    student = "student"
    instructor = "instructor"


class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    role: Role = Role.student


class UserUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    email: EmailStr | None = None


class UserInDB(MongoModel):
    name: str
    email: EmailStr
    role: Role
    hashed_password: str
    created_at: datetime = Field(default_factory=utc_now)


# Never includes the password hash
class UserResponse(MongoModel):
    name: str
    email: EmailStr
    role: Role


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
