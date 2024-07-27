from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    username: str


class CreateUser(UserBase):
    password: str


class GetUser(UserBase):
    email: str | None = None
    full_name: str | None = None
    is_active: bool | None = None


class UserInDB(GetUser):
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
