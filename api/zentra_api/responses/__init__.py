from typing import Generic, TypeVar

from .base import BaseResponse, BaseSuccessResponse
from .messages import HTTPMessage
from .utils import build_response, get_code_status

from pydantic import BaseModel, Field, validate_call


T = TypeVar("T", bound=BaseModel)


class MessageResponse(BaseResponse):
    """A message response model for API responses. Intended for client responses."""

    message: str = Field(..., description="The reason the response occured.")
    headers: dict[str, str] | None = Field(
        default=None, description="The headers to send with the response (optional)."
    )


class ErrorResponse(MessageResponse):
    """An error response model. Intended for client responses."""

    status: str = Field(
        default="error",
        frozen=True,
        description="The status of the response. Cannot be changed.",
    )


class SuccessResponse(BaseSuccessResponse, Generic[T]):
    """A success response model. Intended for client responses. Uses generics to change the data model."""

    data: T


@validate_call
def build_json_response_model(message: HTTPMessage, model: BaseResponse = None) -> dict:
    """A utility function for building JSON response schemas."""
    response = build_response(message.code)
    status = get_code_status(message.code)

    unique_content = (
        {"message": message.message}
        if model is None
        else {"data": model.data.model_dump()}
    )

    return {
        message.code: {
            "model": type(model),
            "description": message.message,
            "content": {
                "application/json": {
                    "example": {
                        "status": status,
                        "code": message.code,
                        "response": response,
                        **unique_content,
                        "headers": message.headers,
                    },
                }
            },
        }
    }
