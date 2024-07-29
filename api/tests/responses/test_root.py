import json
import pytest

from zentra_api.responses import (
    MessageResponse,
    ErrorResponse,
    SuccessResponse,
    build_json_response_model,
    HTTPDetails,
    zentra_json_response,
)

from fastapi import HTTPException
from pydantic import BaseModel, ValidationError
from zentra_api.responses.models import HTTP_MSG_MAPPING


class TestMessageResponse:
    @staticmethod
    def test_init():
        result = MessageResponse(status="test", code=100, message="Test message")
        target = {
            "status": "test",
            "code": 100,
            "response": "100_CONTINUE",
            "message": "Test message",
            "headers": None,
        }
        assert result.model_dump() == target

    @staticmethod
    def test_with_headers():
        result = MessageResponse(
            status="test",
            code=100,
            message="Test message",
            headers={"test": "value"},
        )
        target = {
            "status": "test",
            "code": 100,
            "response": "100_CONTINUE",
            "message": "Test message",
            "headers": {"test": "value"},
        }
        assert result.model_dump() == target

    @staticmethod
    def test_invalid_code():
        with pytest.raises(ValueError):
            MessageResponse(status="test", code=6, message="Test message")


class TestErrorResponse:
    @staticmethod
    def test_init():
        result = ErrorResponse(code=404, message="Test message")

        target = {
            "status": "error",
            "code": 404,
            "response": "404_NOT_FOUND",
            "message": "Test message",
            "headers": None,
        }
        assert result.model_dump() == target

    @staticmethod
    def test_status_overwrite():
        with pytest.raises(ValidationError):
            ErrorResponse(message="Test message", status="test")

    @staticmethod
    def test_invalid_code():
        with pytest.raises(ValueError):
            ErrorResponse(code=6, message="Test message")


class TestSuccessResponse:
    @staticmethod
    def test_init():
        class DataModel(BaseModel):
            id: int
            name: str

        data = DataModel(id=200, name="Test")
        result = SuccessResponse(code=200, data=data)

        target = {
            "status": "success",
            "code": 200,
            "response": "200_OK",
            "data": {"id": 200, "name": "Test"},
            "headers": None,
        }
        assert result.model_dump() == target

    @staticmethod
    def test_invalid_code():
        with pytest.raises(ValueError):
            SuccessResponse(code=6, data={"name": "test"})


class TestBuildJsonResponseModel:
    @staticmethod
    def test_valid():
        result = build_json_response_model(HTTP_MSG_MAPPING[100])

        target = {
            100: {
                "model": MessageResponse,
                "description": "Continue",
                "content": {
                    "application/json": {
                        "example": {
                            "status": "info",
                            "code": 100,
                            "response": "100_CONTINUE",
                            "message": "Continue sending the request body.",
                            "headers": {},
                        }
                    }
                },
            }
        }
        assert target == result

    @staticmethod
    def test_invalid_input():
        with pytest.raises(ValidationError):
            build_json_response_model("test")


class TestHTTPDetails:
    @staticmethod
    def test_init():
        result = HTTPDetails(code=200)
        target = {
            "status": "success",
            "code": 200,
            "response": "200_OK",
            "message": "Request successful, resource returned.",
            "headers": None,
        }
        assert result.response.model_dump() == target

    @staticmethod
    def test_custom_inputs():
        result = HTTPDetails(
            code=200,
            msg="Custom message",
            headers={"X-Test": "Header"},
        )
        target = {
            "status": "success",
            "code": 200,
            "response": "200_OK",
            "message": "Custom message",
            "headers": {"X-Test": "Header"},
        }
        assert result.response.model_dump() == target


class TestZentraJsonResponse:
    @staticmethod
    def test_simple_exception():
        exc = HTTPException(404)

        result = zentra_json_response(exc)
        target_body = {
            "status": "error",
            "code": 404,
            "response": "404_NOT_FOUND",
            "message": "Resource not found.",
            "headers": None,
        }

        result_body = json.loads(result.body.decode("utf-8"))

        assert result.status_code == 404
        assert len(result.headers.keys()) == 2
        assert result_body == target_body

    @staticmethod
    def test_complete_exception():
        exc = HTTPException(
            status_code=404, detail="Custom message", headers={"X-Test": "Header"}
        )

        result = zentra_json_response(exc)
        target_body = {
            "status": "error",
            "code": 404,
            "response": "404_NOT_FOUND",
            "message": "Custom message",
            "headers": {"X-Test": "Header"},
        }
        result_body = json.loads(result.body.decode("utf-8"))

        assert result.status_code == 404
        assert len(result.headers.keys()) == 3
        assert result.headers["X-test"] == "Header"
        assert result_body == target_body
