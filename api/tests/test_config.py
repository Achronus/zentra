import pytest

from sqlalchemy import Engine, create_engine, make_url
from sqlalchemy.orm import sessionmaker, DeclarativeMeta

from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from passlib.context import CryptContext

from zentra_api.config import SQLConfig, AuthConfig, Settings


@pytest.fixture
def valid_sql_url(tmp_path) -> str:
    db_path = tmp_path / "test.db"
    return f"sqlite:///{db_path}"


@pytest.fixture
def invalid_sql_url() -> str:
    return "invalid-url"


class TestSQLConfig:
    @staticmethod
    def test_creation(valid_sql_url: str):
        config = SQLConfig(db_url=valid_sql_url)
        assert config.db_url == make_url(valid_sql_url)
        assert config.db_url.drivername.startswith("sqlite")
        assert isinstance(config.engine, Engine)
        assert isinstance(config.SessionLocal, sessionmaker)
        assert isinstance(config.Base, DeclarativeMeta)

    @staticmethod
    def test_invalid_url(invalid_sql_url: str):
        with pytest.raises(ValidationError):
            SQLConfig(db_url=invalid_sql_url)

    @staticmethod
    def test_create_all_valid(valid_sql_url: str):
        config = SQLConfig(db_url=valid_sql_url)
        config.create_all()

    @staticmethod
    def test_engine_custom_db_url():
        config = SQLConfig(db_url="postgresql://user:password@postgresserver/db")
        assert config.db_url.drivername.startswith("postgresql")
        assert isinstance(config.engine, Engine)

    @staticmethod
    def test_custom_engine():
        url = "postgresql://user:password@postgresserver/db"
        config = SQLConfig(db_url=url, sql_engine=create_engine(url))
        assert isinstance(config.engine, Engine)

    @staticmethod
    def test_custom_sessionmaker():
        url = "postgresql://user:password@postgresserver/db"
        engine = create_engine(url)
        session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        config = SQLConfig(db_url=url, sql_engine=engine, sql_session=session)
        assert isinstance(config.SessionLocal, sessionmaker)


class TestAuthConfig:
    @staticmethod
    def test_default_values():
        config = AuthConfig()
        assert config.ALGORITHM == "HS512"
        assert config.ACCESS_TOKEN_EXPIRE_MINS == 30

    @staticmethod
    def test_secret_key():
        config = AuthConfig()
        secret_key = config.SECRET_KEY
        assert isinstance(secret_key, str)
        assert len(secret_key) > 0

    @staticmethod
    def test_min_length_validation():
        with pytest.raises(ValidationError):
            AuthConfig(ACCESS_TOKEN_EXPIRE_MINS=10)


class TestSettings:
    @staticmethod
    def test_init(valid_sql_url: str):
        sql_config = SQLConfig(db_url=valid_sql_url)
        settings = Settings(SQL=sql_config)
        assert settings.SQL == sql_config
        assert isinstance(settings.AUTH, AuthConfig)

    @staticmethod
    def test_pwd_context(valid_sql_url: str):
        sql_config = SQLConfig(db_url=valid_sql_url)
        settings = Settings(SQL=sql_config)
        assert isinstance(settings.AUTH.pwd_context, CryptContext)

    @staticmethod
    def test_oauth2_scheme(valid_sql_url: str):
        sql_config = SQLConfig(db_url=valid_sql_url)
        settings = Settings(SQL=sql_config)
        assert isinstance(settings.AUTH.oauth2_scheme, OAuth2PasswordBearer)
