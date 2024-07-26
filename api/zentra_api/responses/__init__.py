from typing import Any, Generic, TypeVar

from .base import BaseResponse, BaseSuccessResponse
from .messages import HTTP_MSG_MAPPING, HTTPMessage
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
def build_json_response_model(
    message: HTTPMessage, data_model: SuccessResponse | None = None
) -> dict[int, dict[str, Any]]:
    """A utility function for building JSON response schemas."""
    response = build_response(message.status_code)
    status = get_code_status(message.status_code)
    title = " ".join(response.split("_")[1:]).title()

    unique_content = (
        {"message": message.detail}
        if data_model is None
        else {"data": data_model.data.model_dump()}
    )

    return {
        message.status_code: {
            "model": type(data_model) if data_model else MessageResponse,
            "description": title,
            "content": {
                "application/json": {
                    "example": {
                        "status": status,
                        "code": message.status_code,
                        "response": response,
                        **unique_content,
                        "headers": message.headers,
                    },
                }
            },
        }
    }


class HTTPDetails:
    def __init__(
        self,
        code: int,
        msg: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> None:
        """Generates additional information for the HTTP response and stores it as an attribute (`response`)."""
        self.msg = HTTP_MSG_MAPPING[code]

        self.status_code = self.msg.status_code
        self.detail = msg if msg else self.msg.detail
        self.headers = headers

        self.response = MessageResponse(
            status=self.msg.status,
            code=self.msg.status_code,
            message=self.detail,
            headers=self.headers,
        )
