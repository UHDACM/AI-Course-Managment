from datetime import date, datetime, time, timedelta, timezone

from fastapi import APIRouter, HTTPException, Query, status

from app.core.db import get_db
from app.core.deps import CurrentUser, parse_object_id
from app.schemas import (
    CalendarAssignmentOut,
    CalendarDayOut,
    TodoIn,
    TodoOut,
    TodoUpdate,
    assignment_out,
    todo_out,
)

router = APIRouter(prefix="/calendar", tags=["calendar"])

MAX_DAYS = 366


async def _get_own_todo(todo_id: str, user: dict) -> dict:
    t = await get_db().todos.find_one({"_id": parse_object_id(todo_id, "todo")})
    if t is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "todo not found")
    if t["user_id"] != user["_id"]:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Not your todo")
    return t


@router.post("/todos", response_model=TodoOut, status_code=status.HTTP_201_CREATED)
async def add_todo(body: TodoIn, user: CurrentUser):
    doc = {
        "user_id": user["_id"],
        "title": body.title,
        "description": body.description,
        "date": body.date.isoformat(),  # stored as "YYYY-MM-DD" (no time)
        "completed": False,
        "created_at": datetime.now(timezone.utc),
    }
    doc["_id"] = (await get_db().todos.insert_one(doc)).inserted_id
    return todo_out(doc)


@router.patch("/todos/{todo_id}", response_model=TodoOut)
async def update_todo(todo_id: str, body: TodoUpdate, user: CurrentUser):
    t = await _get_own_todo(todo_id, user)
    changes = body.model_dump(exclude_unset=True)
    if any(changes.get(k, "x") is None for k in ("title", "date", "completed")):
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "field cannot be null")
    if "date" in changes:
        changes["date"] = changes["date"].isoformat()
    if changes:
        await get_db().todos.update_one({"_id": t["_id"]}, {"$set": changes})
        t.update(changes)
    return todo_out(t)


@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_todo(todo_id: str, user: CurrentUser):
    t = await _get_own_todo(todo_id, user)
    await get_db().todos.delete_one({"_id": t["_id"]})


@router.get("", response_model=list[CalendarDayOut])
async def get_calendar(
    user: CurrentUser,
    start: date = Query(...),
    end: date = Query(...),
):
    """Days in [start, end] that have todos or assignments due, sorted by date."""
    if end < start:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "end must not be before start")
    if (end - start).days >= MAX_DAYS:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "range too large (max 366 days)")

    db = get_db()
    days: dict[date, CalendarDayOut] = {}

    def day(d: date) -> CalendarDayOut:
        return days.setdefault(d, CalendarDayOut(date=d, todos=[], assignments=[]))

    cursor = db.todos.find(
        {"user_id": user["_id"], "date": {"$gte": start.isoformat(), "$lte": end.isoformat()}}
    ).sort("created_at", 1)
    async for t in cursor:
        out = todo_out(t)
        day(out.date).todos.append(out)

    field = "teacher_id" if user["role"] == "teacher" else "student_ids"
    class_ids = [c["_id"] async for c in db.classes.find({field: user["_id"]}, {"_id": 1})]
    if class_ids:
        lo = datetime.combine(start, time.min)
        hi = datetime.combine(end + timedelta(days=1), time.min)
        assignments = await db.assignments.find(
            {"class_id": {"$in": class_ids}, "due_date": {"$gte": lo, "$lt": hi}}
        ).sort("due_date", 1).to_list(None)

        # An assignment counts as completed once the student has submitted it.
        done: set = set()
        if user["role"] == "student" and assignments:
            done = {
                s["assignment_id"]
                async for s in db.submissions.find(
                    {
                        "student_id": user["_id"],
                        "assignment_id": {"$in": [a["_id"] for a in assignments]},
                    },
                    {"assignment_id": 1},
                )
            }
        for a in assignments:
            day(a["due_date"].date()).assignments.append(
                CalendarAssignmentOut(
                    **assignment_out(a).model_dump(), completed=a["_id"] in done
                )
            )

    return [days[d] for d in sorted(days)]
