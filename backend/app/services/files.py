from bson import ObjectId
from fastapi import HTTPException, UploadFile, status
from fastapi.responses import StreamingResponse
from gridfs.errors import NoFile

from app.core.config import get_settings
from app.core.db import get_bucket

ALLOWED_CONTENT_TYPES = {
    "application/pdf",
    "text/plain",
    "text/markdown",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.ms-powerpoint",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    "application/zip",
    "image/png",
    "image/jpeg",
}


async def save_upload(file: UploadFile, metadata: dict) -> ObjectId:
    """Stream an upload into GridFS, enforcing type and size limits."""
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            f"File type {file.content_type!r} is not allowed",
        )
    limit = get_settings().max_upload_bytes
    bucket = get_bucket()
    stream = bucket.open_upload_stream(
        file.filename or "upload",
        metadata={**metadata, "content_type": file.content_type},
    )
    size = 0
    try:
        while chunk := await file.read(256 * 1024):
            size += len(chunk)
            if size > limit:
                raise HTTPException(
                    status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    f"File exceeds {limit // (1024 * 1024)} MB limit",
                )
            await stream.write(chunk)
    except BaseException:
        await stream.abort()
        raise
    await stream.close()
    return stream._id


async def delete_file(file_id: ObjectId) -> None:
    try:
        await get_bucket().delete(file_id)
    except NoFile:
        pass


async def stream_file(file_id: ObjectId) -> StreamingResponse:
    bucket = get_bucket()
    try:
        grid_out = await bucket.open_download_stream(file_id)
    except NoFile:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "File not found")
    content_type = (grid_out.metadata or {}).get("content_type", "application/octet-stream")

    async def iterator():
        while chunk := await grid_out.readchunk():
            yield chunk

    return StreamingResponse(
        iterator(),
        media_type=content_type,
        headers={"Content-Disposition": f'attachment; filename="{grid_out.filename}"'},
    )
