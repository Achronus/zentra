from typing import Annotated

from zentra_api.auth.security import SecurityUtils
from zentra_api.config import SQLConfig, Settings
from zentra_api.config.env import load_dotenv_file

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


load_dotenv_file(".env.backend")


class DatabaseConfig(BaseModel):
    """Storage container for database settings."""

    URL: str


class EnvVariables(BaseSettings):
    """A settings class for extracting the environment variables from the `.env.backend` file."""

    DB: DatabaseConfig

    model_config = SettingsConfigDict(
        env_file=".env.backend", env_nested_delimiter="__"
    )


env_vars = EnvVariables()
SETTINGS = Settings(SQL=SQLConfig(db_url=env_vars.DB.URL))


def get_db():
    """Dependency for retrieving a database session."""
    db = SETTINGS.SQL.SessionLocal
    try:
        yield db
    finally:
        db.close()


security = SecurityUtils(settings=SETTINGS)

db_dependency = Annotated[Session, Depends(get_db)]
oauth2_dependency = Annotated[str, Depends(SETTINGS.oauth2_scheme)]
oauth2_form_dependency = Annotated[OAuth2PasswordRequestForm, Depends()]
