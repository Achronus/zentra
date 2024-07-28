from fastapi import HTTPException
import pytest
import string

from datetime import datetime, timedelta, timezone
from pydantic import BaseModel
import jwt

from zentra_api.config import AuthConfig
from zentra_api.auth.enums import JWTSize
from zentra_api.auth.security import SecurityUtils
from zentra_api.auth.utils import generate_secret_key


class TestGenerateJWTSecretKey:
    @staticmethod
    def test_key_length_for_algorithms():
        algorithms = {
            JWTSize.HS256: 256 // 8,
            JWTSize.HS384: 384 // 8,
            JWTSize.HS512: 512 // 8,
        }

        for algo, expected_length in algorithms.items():
            key = generate_secret_key(algo)
            assert len(key) == expected_length

    @staticmethod
    def test_key_character_set():
        valid_chars = string.ascii_letters + string.digits + "-_"

        for algo in JWTSize:
            key = generate_secret_key(algo)
            assert all(c in valid_chars for c in key)

    @staticmethod
    def test_default_algorithm():
        key = generate_secret_key()
        expected_length = 256 // 8
        assert len(key) == expected_length

    @staticmethod
    def test_invalid_algorithm():
        invalid_algorithms = [128, 1024, "string", None]

        for algo in invalid_algorithms:
            with pytest.raises(ValueError):
                generate_secret_key(algo)


class TestSecurityUtils:
    @pytest.fixture
    def security_utils(self) -> SecurityUtils:
        return SecurityUtils(auth=AuthConfig())

    @staticmethod
    def test_hash_password(security_utils: SecurityUtils):
        password = "testpassword"
        hashed_password = security_utils.hash_password(password)
        assert security_utils.auth.pwd_context.verify(password, hashed_password)

    @staticmethod
    def test_verify_password(security_utils: SecurityUtils):
        password = "testpassword"
        hashed_password = security_utils.hash_password(password)
        assert security_utils.verify_password(password, hashed_password)
        assert not security_utils.verify_password("wrongpassword", hashed_password)

    @staticmethod
    def test_expiration_with_value(security_utils: SecurityUtils):
        expires_delta = timedelta(minutes=5)
        expire_time = security_utils.expiration(expires_delta)
        assert expire_time == datetime.now(timezone.utc) + expires_delta

    @staticmethod
    def test_expiration_default(security_utils: SecurityUtils):
        expire_time = security_utils.expiration()
        assert expire_time == datetime.now(timezone.utc) + security_utils.expire_mins()

    @staticmethod
    def test_encrypt(security_utils: SecurityUtils):
        class TestModel(BaseModel):
            password: str

        model = TestModel(password="testpassword")
        encrypted_model = security_utils.encrypt(model, "password")
        assert security_utils.auth.pwd_context.verify(
            "testpassword", encrypted_model.password
        )

    @staticmethod
    def test_encrypt_key_error(security_utils: SecurityUtils):
        class TestModel(BaseModel):
            password: str

        model = TestModel(password="testpassword")

        with pytest.raises(AttributeError):
            security_utils.encrypt(model, "email")

    @staticmethod
    def test_create_access_token(security_utils: SecurityUtils):
        data = {"sub": "testuser"}
        token = security_utils.create_access_token(data)
        decoded_data = jwt.decode(
            token,
            key=security_utils.auth.SECRET_KEY,
            algorithms=[security_utils.auth.ALGORITHM],
        )
        assert decoded_data["sub"] == "testuser", (token, decoded_data)

    @staticmethod
    def test_get_token_data(security_utils: SecurityUtils):
        data = {"sub": "testuser"}
        token = security_utils.create_access_token(data)
        token_data = security_utils.get_token_data(token)
        assert token_data == "testuser"

    @staticmethod
    def test_get_token_data_invalid_token(security_utils: SecurityUtils):
        with pytest.raises(HTTPException):
            security_utils.get_token_data("invalidtoken")

    @staticmethod
    def test_empty_token_data(security_utils: SecurityUtils):
        data = {"sub": None}
        token = security_utils.create_access_token(data)

        with pytest.raises(HTTPException):
            security_utils.get_token_data(token)
