from bson import ObjectId
from fastapi import APIRouter, HTTPException, Query

from app.core.database import get_database
from app.models import CourseCreate, CourseInDB, CourseResponse
from app.models.common import utc_now

router = APIRouter(prefix="/api/courses", tags=["courses"])


@router.post("", response_model=CourseResponse, status_code=201)
async def create_course(
    course: CourseCreate,
    # Temporary until login exists: the instructor's id is passed in the URL.
    # Once auth is added this will come from the logged-in user instead.
    instructor_id: str = Query(description="Id of the instructor's user document"),
):
    if not ObjectId.is_valid(instructor_id):
        raise HTTPException(status_code=422, detail="instructor_id is not a valid id")

    db = get_database()

    doc = course.model_dump()
    doc["instructor_id"] = ObjectId(instructor_id)
    doc["syllabus"] = None
    doc["syllabus_updated_at"] = None
    doc["created_at"] = utc_now()

    result = await db.courses.insert_one(doc)
    doc["_id"] = result.inserted_id
    saved = CourseInDB(**doc)

    # No users collection is filled yet, so the name may be missing
    instructor = await db.users.find_one({"_id": doc["instructor_id"]}, {"name": 1})
    instructor_name = instructor["name"] if instructor else None

    return CourseResponse(**saved.model_dump(), instructor_name=instructor_name)
