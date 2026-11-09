import secrets

from fastapi import APIRouter, HTTPException, status
from pymongo.errors import DuplicateKeyError

from app.core.db import get_db
from app.core.deps import CurrentStudent, CurrentTeacher, CurrentUser, parse_object_id
from app.schemas import ClassIn, ClassOut, JoinIn, class_out

router = APIRouter(prefix="/classes", tags=["classes"])


async def get_class_for_member(class_id: str, user: dict) -> dict:
    """Return the class if `user` owns it (teacher) or is enrolled (student)."""
    cls = await get_db().classes.find_one({"_id": parse_object_id(class_id, "class")})
    if cls is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "class not found")
    if user["_id"] != cls["teacher_id"] and user["_id"] not in cls.get("student_ids", []):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Not a member of this class")
    return cls


@router.post("", response_model=ClassOut, status_code=status.HTTP_201_CREATED)
async def create_class(body: ClassIn, teacher: CurrentTeacher):
    db = get_db()
    for _ in range(5):  # retry on the (unlikely) join-code collision
        doc = {
            "name": body.name,
            "description": body.description,
            "teacher_id": teacher["_id"],
            "student_ids": [],
            "join_code": secrets.token_urlsafe(6),
        }
        try:
            doc["_id"] = (await db.classes.insert_one(doc)).inserted_id
            return class_out(doc, teacher)
        except DuplicateKeyError:
            continue
    raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Could not create class")


@router.get("", response_model=list[ClassOut])
async def list_classes(user: CurrentUser):
    field = "teacher_id" if user["role"] == "teacher" else "student_ids"
    cursor = get_db().classes.find({field: user["_id"]})
    return [class_out(c, user) async for c in cursor]


@router.post("/join", response_model=ClassOut)
async def join_class(body: JoinIn, student: CurrentStudent):
    cls = await get_db().classes.find_one_and_update(
        {"join_code": body.join_code},
        {"$addToSet": {"student_ids": student["_id"]}},
        return_document=True,
    )
    if cls is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Invalid join code")
    return class_out(cls, student)


@router.get("/{class_id}", response_model=ClassOut)
async def get_class(class_id: str, user: CurrentUser):
    return class_out(await get_class_for_member(class_id, user), user)
