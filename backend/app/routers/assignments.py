from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status

from app.core.db import get_db
from app.core.deps import CurrentTeacher, CurrentUser, parse_object_id
from app.routers.classes import get_class_for_member
from app.schemas import AssignmentOut, assignment_out
from app.services import files

router = APIRouter(tags=["assignments"])


async def get_assignment_for_member(assignment_id: str, user: dict) -> tuple[dict, dict]:
    """Return (assignment, class) if the user belongs to the assignment's class."""
    a = await get_db().assignments.find_one(
        {"_id": parse_object_id(assignment_id, "assignment")}
    )
    if a is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "assignment not found")
    cls = await get_class_for_member(str(a["class_id"]), user)
    return a, cls


@router.post(
    "/classes/{class_id}/assignments",
    response_model=AssignmentOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_assignment(
    class_id: str,
    teacher: CurrentTeacher,
    title: Annotated[str, Form(min_length=1, max_length=200)],
    description: Annotated[str, Form()] = "",
    due_date: Annotated[datetime | None, Form()] = None,
    file: Annotated[UploadFile | None, File()] = None,
):
    cls = await get_class_for_member(class_id, teacher)
    if cls["teacher_id"] != teacher["_id"]:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "You do not own this class")

    doc = {
        "class_id": cls["_id"],
        "title": title,
        "description": description,
        "due_date": due_date,
        "attachment_file_id": None,
        "attachment_filename": None,
        "created_by": teacher["_id"],
        "created_at": datetime.now(timezone.utc),
    }
    if file is not None and file.filename:
        doc["attachment_file_id"] = await files.save_upload(
            file, {"kind": "assignment_attachment", "class_id": str(cls["_id"])}
        )
        doc["attachment_filename"] = file.filename
    doc["_id"] = (await get_db().assignments.insert_one(doc)).inserted_id
    return assignment_out(doc)


@router.get("/classes/{class_id}/assignments", response_model=list[AssignmentOut])
async def list_assignments(class_id: str, user: CurrentUser):
    cls = await get_class_for_member(class_id, user)
    cursor = get_db().assignments.find({"class_id": cls["_id"]}).sort("created_at", -1)
    return [assignment_out(a) async for a in cursor]


@router.get("/assignments/{assignment_id}", response_model=AssignmentOut)
async def get_assignment(assignment_id: str, user: CurrentUser):
    a, _ = await get_assignment_for_member(assignment_id, user)
    return assignment_out(a)


@router.get("/assignments/{assignment_id}/attachment")
async def download_attachment(assignment_id: str, user: CurrentUser):
    a, _ = await get_assignment_for_member(assignment_id, user)
    if a.get("attachment_file_id") is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Assignment has no attachment")
    return await files.stream_file(a["attachment_file_id"])
