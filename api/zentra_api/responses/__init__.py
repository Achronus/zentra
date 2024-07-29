from typing import Any, Generic, TypeVar

from fastapi import HTTPException
from fastapi.responses import JSONResponse

from .base import BaseResponse, BaseSuccessResponse
from .messages import HTTP_MSG_MAPPING, HTTPMessage
from .utils import build_response, get_code_status, merge_dicts_list
from zentra_api.utils.package import load_module

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationInfo,
    field_validator,
    validate_call,
)


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
def build_json_response_model(message: HTTPMessage) -> dict[int, dict[str, Any]]:
    """A utility function for building JSON response schemas."""
    response = build_response(message.status_code)
    status = get_code_status(message.status_code)
    title = " ".join(response.split("_")[1:]).title()

    return {
        message.status_code: {
            "model": MessageResponse,
            "description": title,
            "content": {
                "application/json": {
                    "example": {
                        "status": status,
                        "code": message.status_code,
                        "response": response,
                        "message": message.detail,
                        "headers": message.headers,
                    },
                }
            },
        }
    }


class HTTPDetails(BaseModel):
    """The details for HTTP responses."""

    code: int
    msg: str | None = Field(None, validate_default=True)
    headers: dict[str, str] | None = None

    @field_validator("msg", mode="before")
    def validate_msg(cls, msg: str | None, info: ValidationInfo) -> str:
        code = info.data.get("code")
        custom_msg = HTTP_MSG_MAPPING[code]

        response = build_response(code)
        title = " ".join(response.split("_")[1:]).title()

        if msg == title or msg is None:
            return custom_msg.detail

        return msg

    @property
    def response(self) -> MessageResponse:
        """The message response model."""
        msg = HTTP_MSG_MAPPING[self.code]

        return MessageResponse(
            status=msg.status,
            code=msg.status_code,
            message=self.msg,
            headers=self.headers,
        )


@validate_call(validate_return=True, config=ConfigDict(arbitrary_types_allowed=True))
def zentra_json_response(exc: HTTPException) -> JSONResponse:
    """Returns a detailed HTTP response using the `ZentraAPI` package."""
    details = HTTPDetails(code=exc.status_code, msg=exc.detail, headers=exc.headers)
    return JSONResponse(
        details.response.model_dump(),
        status_code=exc.status_code,
        headers=exc.headers,
    )


@validate_call
def response_models(codes: int | list[int]) -> dict[int, dict[str, Any]]:
    """Returns a dictionary of response model schemas given a set of HTTP codes."""

    ROOT_PATH = "zentra_api.responses"

    if isinstance(codes, int):
        codes = [codes]

    models = []
    for code in codes:
        response = build_response(code, no_strip=True).split("_")[:2]
        code_type = get_code_status(code)
        const_name = f"{response[0]}_{code_type}_{str(code)}".upper()

        module = load_module(ROOT_PATH, "models")
        models.append(getattr(module, const_name))

    return merge_dicts_list(models)
