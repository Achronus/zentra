import pytest
from pydantic import ValidationError

from zentra_api.schema import Token
from zentra_api.enums import TokenType


class TestToken:
    @staticmethod
    def test_init():
        token = Token(
            access_token="valid_access_token",
            token_type=TokenType.BEARER,
        )

        assert isinstance(token, Token)
        assert token.access_token == "valid_access_token"
        assert token.token_type == "bearer"

    @staticmethod
    def test_invalid_access_token():
        with pytest.raises(ValidationError):
            Token(access_token=None, token_type=TokenType.BEARER)

    @staticmethod
    def test_invalid_token_type():
        with pytest.raises(ValidationError):
            Token(access_token="valid_access_token", token_type="invalid_token_type")

    @staticmethod
    def test_model_dump_valid():
        token = Token(access_token="valid_access_token", token_type=TokenType.BEARER)

        token_dict = token.model_dump()

        assert token_dict == {
            "access_token": "valid_access_token",
            "token_type": "bearer",
        }
