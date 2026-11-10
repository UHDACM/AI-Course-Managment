from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.core.db import get_db
from app.core.deps import CurrentStudent, CurrentUser, parse_object_id
from app.routers.assignments import get_assignment_for_member
from app.schemas import SubmissionOut, submission_out
from app.services import files

router = APIRouter(tags=["submissions"])


@router.post(
    "/assignments/{assignment_id}/submissions",
    response_model=SubmissionOut,
    status_code=status.HTTP_201_CREATED,
)
async def submit(
    assignment_id: str,
    student: CurrentStudent,
    file: Annotated[UploadFile, File()],
):
    a, cls = await get_assignment_for_member(assignment_id, student)
    db = get_db()

    file_id = await files.save_upload(
        file,
        {
            "kind": "submission",
            "assignment_id": str(a["_id"]),
            "student_id": str(student["_id"]),
        },
    )
    now = datetime.now(timezone.utc)
    # Upsert: a resubmission replaces the previous file.
    old = await db.submissions.find_one_and_update(
        {"assignment_id": a["_id"], "student_id": student["_id"]},
        {
            "$set": {
                "class_id": cls["_id"],
                "file_id": file_id,
                "filename": file.filename,
                "submitted_at": now,
            }
        },
        upsert=True,
        return_document=False,  # returns the pre-update document (None if new)
    )
    if old is not None:
        await files.delete_file(old["file_id"])

    sub = await db.submissions.find_one(
        {"assignment_id": a["_id"], "student_id": student["_id"]}
    )
    return submission_out(sub)


@router.get("/assignments/{assignment_id}/submissions", response_model=list[SubmissionOut])
async def list_submissions(assignment_id: str, user: CurrentUser):
    a, cls = await get_assignment_for_member(assignment_id, user)
    query = {"assignment_id": a["_id"]}
    if user["_id"] != cls["teacher_id"]:  # students only see their own
        query["student_id"] = user["_id"]
    cursor = get_db().submissions.find(query).sort("submitted_at", -1)
    return [submission_out(s) async for s in cursor]


@router.get("/submissions/{submission_id}/file")
async def download_submission(submission_id: str, user: CurrentUser):
    sub = await get_db().submissions.find_one(
        {"_id": parse_object_id(submission_id, "submission")}
    )
    if sub is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "submission not found")
    cls = await get_db().classes.find_one({"_id": sub["class_id"]})
    allowed = user["_id"] == sub["student_id"] or (
        cls is not None and user["_id"] == cls["teacher_id"]
    )
    if not allowed:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Not allowed to view this submission")
    return await files.stream_file(sub["file_id"])
