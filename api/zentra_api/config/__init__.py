from zentra_api.auth.enums import JWTAlgorithm, JWTSize
from zentra_api.auth.utils import generate_secret_key

from sqlalchemy import URL, Engine, create_engine, make_url
from sqlalchemy.orm import sessionmaker, declarative_base, DeclarativeMeta
from sqlalchemy.exc import ArgumentError

from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, Field, PrivateAttr, field_validator, ConfigDict
from pydantic_core import PydanticCustomError


class SQLConfig(BaseModel):
    """
    A model for storing SQL configuration settings. Automatically creates a SQL `engine`, `SessionLocal` and `Base` based on a given `db_url`.

    Parameters:
    - `db_url` - (`sqlalchemy.URL | string`) - the SQL database URL
    - `sql_engine` (`sqlalchemy.Engine | None, optional`) - a custom SQLAlchemy engine instance created using `create_engine()`. When `None`, creates one automatically. `None` by default
    - `sql_session` (`sqlalchemy.sessionmaker | None, optional`) - a custom SQLAlchemy session instance created using `sessionmaker`. When `None`, creates one automatically -> `sessionmaker(autocommit=False, autoflush=False, bind=engine)`. `None` by default
    - `sql_base` (`sqlalchemy.orm.DeclarativeBase | None`) - a custom SQLAlchemy Base instance created using `declarative_base()`. When `None` creates one automatically -> `declarative_base()`. `None` by default
    """

    db_url: URL | str = Field(
        ...,
        description="The SQL database URL.",
    )
    sql_engine: Engine | None = Field(
        None,
        description="A SQLAlchemy engine instance created using `create_engine()`.",
    )
    sql_session: sessionmaker | None = Field(
        None,
        description="a custom SQLAlchemy session instance created using `sessionmaker`.",
    )
    sql_base: DeclarativeMeta | None = Field(
        None,
        description="a custom SQLAlchemy Base instance created using `declarative_base()`.",
    )

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @field_validator("db_url")
    def validate_db_url(cls, db_url: URL | str) -> URL:
        if isinstance(db_url, str):
            try:
                db_url = make_url(db_url)
            except ArgumentError:
                raise PydanticCustomError(
                    "invalid_url",
                    f"'{db_url}' is not a valid database URL.",
                    dict(wrong_value=db_url),
                )

        return db_url

    @property
    def engine(self) -> Engine:
        """The SQLAlchemy engine."""
        if self.sql_engine:
            return self.sql_engine

        if self.db_url.drivername.startswith("sqlite"):
            return create_engine(
                self.db_url,
                connect_args={"check_same_thread": False},
            )

        return create_engine(self.db_url)

    @property
    def SessionLocal(self) -> sessionmaker:
        """The SQLAlchemy local session."""
        if self.sql_session:
            return self.sql_session

        return sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    @property
    def Base(self) -> DeclarativeMeta:
        """The SQLAlchemy `declarative_base()` instance."""
        return self.sql_base if self.sql_base else declarative_base()

    def create_all(self) -> None:
        """Creates all the database tables in the `Base` instance."""
        self.Base.metadata.create_all(bind=self.engine)


class AuthConfig(BaseModel):
    """
    A storage container for authentication settings. Automatically creates tokens and secret keys using the given algorithm.

    Parameters:
    - `ALGORITHM` (`zentra_api.auth.enums.JWTAlgorithm, optional`) - the encryption algorithm for the OAUTH2 token and secret key. `HS512` by default
    - `ACCESS_TOKEN_EXPIRE_MINS` (`integer, optional`) - the expire length for access tokens in minutes. Must be a minimum of `15`. `30` by default
    """

    ALGORITHM: JWTAlgorithm = Field(
        default=JWTAlgorithm.HS512,
        description="The encryption algorithm for the OAUTH2 token and secret key.",
        validate_default=True,
    )
    ACCESS_TOKEN_EXPIRE_MINS: int = Field(
        default=30,
        ge=15,
        description="The expire length for the access token in minutes.",
    )

    _secret_key = PrivateAttr(default=None)
    model_config = ConfigDict(use_enum_values=True)

    def model_post_init(self, __context):
        self._secret_key = generate_secret_key(JWTSize[self.ALGORITHM])

    @property
    def SECRET_KEY(self) -> str:
        return self._secret_key

    @property
    def pwd_context(self) -> CryptContext:
        """The authentication password context."""
        return CryptContext(schemes=["bcrypt"], deprecated="auto")

    @property
    def oauth2_scheme(self) -> OAuth2PasswordBearer:
        """The OAUTH2 dependency flow. Uses authentication using a bearer token obtained with a password with `tokenUrl="auth/token"`."""
        return OAuth2PasswordBearer(tokenUrl="auth/token")


class Settings(BaseModel):
    """
    A model for storing all config settings.

    Parameters:
    - `SQL` (`zentra_api.config.SQLConfig`) - a ZentraAPI `SQLConfig` model containing a database URL
    - `AUTH` (`zentra_api.config.AuthConfig, optional`) - an optional ZentraAPI `AuthConfig` model with custom configuration settings. Otherwise, created automatically
    """

    SQL: SQLConfig
    AUTH: AuthConfig = AuthConfig()

    model_config = ConfigDict(use_enum_values=True)
