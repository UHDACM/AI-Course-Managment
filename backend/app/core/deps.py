from typing import Annotated

import jwt
from bson import ObjectId
from bson.errors import InvalidId
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.core.db import get_db
from app.core.security import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def parse_object_id(value: str, what: str = "id") -> ObjectId:
    try:
        return ObjectId(value)
    except (InvalidId, TypeError):
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"{what} not found")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    cred_error = HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        "Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        user_id = ObjectId(payload["sub"])
    except (jwt.PyJWTError, KeyError, InvalidId):
        raise cred_error
    user = await get_db().users.find_one({"_id": user_id})
    if user is None:
        raise cred_error
    return user


CurrentUser = Annotated[dict, Depends(get_current_user)]


def require_role(role: str):
    async def checker(user: CurrentUser) -> dict:
        if user["role"] != role:
            raise HTTPException(status.HTTP_403_FORBIDDEN, f"{role} role required")
        return user

    return checker


CurrentTeacher = Annotated[dict, Depends(require_role("teacher"))]
CurrentStudent = Annotated[dict, Depends(require_role("student"))]
