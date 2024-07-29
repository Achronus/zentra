from typing import Annotated


from app.auth.schema import CreateUser, GetUser, Token, UserInDB
from app.config import (
    db_dependency,
    oauth2_dependency,
    oauth2_form_dependency,
    security,
)
from app.models import CONNECT

from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session

from zentra_api.responses import get_response_models
from zentra_api.responses.exc import CREDENTIALS_EXCEPTION, USER_EXCEPTION


router = APIRouter(prefix="/auth", tags=["Authentication"])


def authenticate_user(db: Session, username: str, password: str) -> dict | bool:
    """Authenticates the user based on its password, assuming it exists and the password is valid. If not, returns `False`."""
    user: dict | None = CONNECT.user.get_by_username(db, username)

    if not user:
        return False

    if not security.verify_password(password, user.password):
        return False

    return user


async def get_current_user(token: oauth2_dependency, db: db_dependency) -> GetUser:
    """Gets the current user based on the given token."""
    username = security.get_token_data(token)
    user: dict | None = CONNECT.user.get_by_username(db, username)

    if user is None:
        raise CREDENTIALS_EXCEPTION

    return GetUser(**user)


async def get_current_active_user(
    current_user: Annotated[GetUser, Depends(get_current_user)],
) -> GetUser:
    if not current_user.is_active:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Inactive user.")

    return current_user


@router.get(
    "/users/me",
    status_code=status.HTTP_200_OK,
    responses=get_response_models(401),
)
async def get_user(current_user: Annotated[GetUser, Depends(get_current_active_user)]):
    return current_user


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    responses=get_response_models(400),
)
async def register_user(user: CreateUser, db: db_dependency):
    exists = CONNECT.user.get_by_username(db, user.username)

    if exists:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, detail="User already registered."
        )

    encrypted_user = security.encrypt(user, "password")
    CONNECT.user.create(db, encrypted_user.model_dump())

    return {"User": user}


@router.post(
    "/token",
    status_code=status.HTTP_202_ACCEPTED,
    responses=get_response_models(401),
    response_model=Token,
)
async def login_for_access_token(form_data: oauth2_form_dependency, db: db_dependency):
    user = authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise USER_EXCEPTION

    access_token = security.create_access_token({"sub": user.username})
    return Token(access_token=access_token, token_type="bearer")


@router.post(
    "/verify-token/{token}",
    status_code=status.HTTP_200_OK,
    responses=get_response_models(403),
)
async def verify_user_token(token: oauth2_dependency):
    security.verify_token(token)
    return {"message": "Token is valid"}
