from datetime import date as Date
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, EmailStr, Field


class RegisterIn(BaseModel):
    email: EmailStr
    name: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=8, max_length=128)
    role: Literal["teacher", "student"]


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    id: str
    email: str
    name: str
    role: str


class ClassIn(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str = ""


class JoinIn(BaseModel):
    join_code: str


class ClassOut(BaseModel):
    id: str
    name: str
    description: str
    teacher_id: str
    student_count: int
    join_code: str | None = None  # only shown to the owning teacher


class AssignmentOut(BaseModel):
    id: str
    class_id: str
    title: str
    description: str
    due_date: datetime | None
    attachment_filename: str | None
    created_by: str
    created_at: datetime


class SubmissionOut(BaseModel):
    id: str
    assignment_id: str
    class_id: str
    student_id: str
    filename: str
    submitted_at: datetime


def user_out(u: dict) -> UserOut:
    return UserOut(id=str(u["_id"]), email=u["email"], name=u["name"], role=u["role"])


def class_out(c: dict, viewer: dict) -> ClassOut:
    owner = c["teacher_id"] == viewer["_id"]
    return ClassOut(
        id=str(c["_id"]),
        name=c["name"],
        description=c.get("description", ""),
        teacher_id=str(c["teacher_id"]),
        student_count=len(c.get("student_ids", [])),
        join_code=c["join_code"] if owner else None,
    )


def assignment_out(a: dict) -> AssignmentOut:
    return AssignmentOut(
        id=str(a["_id"]),
        class_id=str(a["class_id"]),
        title=a["title"],
        description=a["description"],
        due_date=a.get("due_date"),
        attachment_filename=a.get("attachment_filename"),
        created_by=str(a["created_by"]),
        created_at=a["created_at"],
    )


def submission_out(s: dict) -> SubmissionOut:
    return SubmissionOut(
        id=str(s["_id"]),
        assignment_id=str(s["assignment_id"]),
        class_id=str(s["class_id"]),
        student_id=str(s["student_id"]),
        filename=s["filename"],
        submitted_at=s["submitted_at"],
    )



class TodoIn(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    date: Date
    description: str = ""


class TodoUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    date: Date | None = None
    description: str | None = None
    completed: bool | None = None


class TodoOut(BaseModel):
    id: str
    title: str
    date: Date
    description: str
    completed: bool
    created_at: datetime


class CalendarAssignmentOut(AssignmentOut):
    completed: bool = False  # student has submitted it


class CalendarDayOut(BaseModel):
    date: Date
    todos: list[TodoOut]
    assignments: list[CalendarAssignmentOut]


def todo_out(t: dict) -> TodoOut:
    return TodoOut(
        id=str(t["_id"]),
        title=t["title"],
        date=Date.fromisoformat(t["date"]),
        description=t.get("description", ""),
        completed=t.get("completed", False),
        created_at=t["created_at"],
    )
