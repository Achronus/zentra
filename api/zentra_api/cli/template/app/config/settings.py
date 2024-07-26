from .env import load_dotenv_file

from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


load_dotenv_file(".env.backend")


class DatabaseConfig(BaseModel):
    """A place to store database settings."""

    URL: str

    @property
    def CONNECT_ARGS(self) -> dict | None:
        """Dynamically creates the `connect_args` for the SQL sessionmaker."""
        if self.URL.startswith("sqlite"):
            return {"check_same_thread": False}

        return None


class AuthConfig(BaseModel):
    """Storage container for authentication settings."""

    OAUTH2_TOKEN: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINS: int

    @property
    def oauth2_scheme(self) -> OAuth2PasswordBearer:
        return OAuth2PasswordBearer(tokenUrl=self.OAUTH2_TOKEN)

    @property
    def pwd_context(self) -> CryptContext:
        return CryptContext(schemes=["bcrypt"])


class Settings(BaseSettings):
    """A model for storing all config settings."""

    DB: DatabaseConfig
    AUTH: AuthConfig

    model_config = SettingsConfigDict(
        env_file=".env.backend", env_nested_delimiter="__"
    )


SETTINGS = Settings()
