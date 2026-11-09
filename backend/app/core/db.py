from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorDatabase,
    AsyncIOMotorGridFSBucket,
)

from app.core.config import get_settings

_client: AsyncIOMotorClient | None = None


def connect() -> None:
    global _client
    _client = AsyncIOMotorClient(get_settings().mongodb_url)


def disconnect() -> None:
    global _client
    if _client is not None:
        _client.close()
        _client = None


def get_db() -> AsyncIOMotorDatabase:
    if _client is None:
        connect()
    return _client[get_settings().mongodb_database]


def get_bucket() -> AsyncIOMotorGridFSBucket:
    return AsyncIOMotorGridFSBucket(get_db())


async def create_indexes() -> None:
    db = get_db()
    await db.users.create_index("email", unique=True)
    await db.classes.create_index("join_code", unique=True)
    await db.classes.create_index("teacher_id")
    await db.classes.create_index("student_ids")
    await db.assignments.create_index("class_id")
    await db.submissions.create_index(
        [("assignment_id", 1), ("student_id", 1)], unique=True
    )
