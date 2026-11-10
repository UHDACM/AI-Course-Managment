from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pymongo.errors import DuplicateKeyError

from app.core.db import get_db
from app.core.deps import CurrentUser
from app.core.security import create_access_token, hash_password, verify_password
from app.schemas import RegisterIn, TokenOut, UserOut, user_out

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(body: RegisterIn):
    doc = {
        "email": body.email.lower(),
        "name": body.name,
        "password_hash": hash_password(body.password),
        "role": body.role,
    }
    try:
        res = await get_db().users.insert_one(doc)
    except DuplicateKeyError:
        raise HTTPException(status.HTTP_409_CONFLICT, "Email already registered")
    doc["_id"] = res.inserted_id
    return user_out(doc)


@router.post("/login", response_model=TokenOut)
async def login(form: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await get_db().users.find_one({"email": form.username.lower()})
    if user is None or not verify_password(form.password, user["password_hash"]):
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return TokenOut(access_token=create_access_token(str(user["_id"]), user["role"]))


@router.get("/me", response_model=UserOut)
async def me(user: CurrentUser):
    return user_out(user)
