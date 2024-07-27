from datetime import timedelta
from typing import Annotated


from app.auth.schema import CreateUser, GetUser, Token, UserInDB
from app.config import get_db, SETTINGS
from app.models import CONNECT

from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session

from zentra_api.auth.security import SecurityUtils
from zentra_api.responses.models import HTTP_ERROR_400, HTTP_ERROR_401, HTTP_ERROR_403
from zentra_api.responses.exception import CREDENTIALS_EXCEPTION, USER_EXCEPTION


router = APIRouter(prefix="/auth", tags=["Authentication"])

security = SecurityUtils(settings=SETTINGS)


def authenticate_user(db: Session, username: str, password: str) -> dict | bool:
    """Authenticates the user based on its password, assuming it exists and the password is valid. If not, returns `False`."""
    user: dict | None = CONNECT.user.get_by_username(db, username)

    if not user:
        return False

    if not security.verify_password(password, user.password):
        return False

    return user


async def get_current_user(
    token: Annotated[str, Depends(SETTINGS.oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
) -> GetUser:
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
    responses=HTTP_ERROR_401,
)
async def get_user(current_user: Annotated[GetUser, Depends(get_current_active_user)]):
    return current_user


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    responses=HTTP_ERROR_400,
)
async def register_user(user: CreateUser, db: Annotated[Session, Depends(get_db)]):
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
    responses=HTTP_ERROR_401,
    response_model=Token,
)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
):
    user = authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise USER_EXCEPTION

    expire_mins = timedelta(minutes=SETTINGS.AUTH.ACCESS_TOKEN_EXPIRE_MINS)
    access_token = security.create_access_token(
        {"sub": user.username}, expires_delta=expire_mins
    )
    return Token(access_token=access_token, token_type="bearer")


@router.post(
    "/verify-token/{token}",
    status_code=status.HTTP_200_OK,
    responses=HTTP_ERROR_403,
)
async def verify_user_token(token: Annotated[str, Depends(SETTINGS.oauth2_scheme)]):
    security.verify_token(token)
    return {"message": "Token is valid"}
