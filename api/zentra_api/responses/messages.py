from pydantic import BaseModel, Field, field_validator
from fastapi import status


class HTTPMessage(BaseModel):
    """A model for HTTP messages."""

    code: int = Field(..., description="The HTTP response code.")
    message: str = Field(..., description="The reason the response occured.")
    headers: dict[str, str] | None = Field(
        default=None,
        description="The headers to send with the response (optional).",
        validate_default=True,
    )

    @field_validator("headers")
    def validate_headers(cls, headers: dict[str, str] | None) -> dict:
        if headers is None:
            return {}

        return headers


HTTP_100_MSG = HTTPMessage(
    code=status.HTTP_100_CONTINUE, message="Continue sending the request body."
)

HTTP_101_MSG = HTTPMessage(
    code=status.HTTP_101_SWITCHING_PROTOCOLS,
    message="Switching protocols as requested.",
)

HTTP_102_MSG = HTTPMessage(
    code=status.HTTP_102_PROCESSING, message="Processing request."
)

HTTP_103_MSG = HTTPMessage(
    code=status.HTTP_103_EARLY_HINTS,
    message="Sending early hints.",
)

HTTP_200_MSG = HTTPMessage(
    code=status.HTTP_200_OK, message="Request successful, resource returned."
)

HTTP_201_MSG = HTTPMessage(
    code=status.HTTP_201_CREATED, message="Request successful, new resource created."
)

HTTP_202_MSG = HTTPMessage(
    code=status.HTTP_202_ACCEPTED, message="Request accepted, processing not complete."
)

HTTP_203_MSG = HTTPMessage(
    code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
    message="Request successful, info may be from third-party.",
)

HTTP_204_MSG = HTTPMessage(
    code=status.HTTP_204_NO_CONTENT,
    message="Request successful, no content in response.",
)

HTTP_205_MSG = HTTPMessage(
    code=status.HTTP_205_RESET_CONTENT,
    message="Request successful, reset document view.",
)

HTTP_206_MSG = HTTPMessage(
    code=status.HTTP_206_PARTIAL_CONTENT,
    message="Partial resource delivered due to range header.",
)

HTTP_207_MSG = HTTPMessage(
    code=status.HTTP_207_MULTI_STATUS,
    message="Request successful, multiple statuses in response.",
)

HTTP_208_MSG = HTTPMessage(
    code=status.HTTP_208_ALREADY_REPORTED,
    message="DAV bindings already enumerated in previous response.",
)

HTTP_226_MSG = HTTPMessage(
    code=status.HTTP_226_IM_USED,
    message="GET request fulfilled, instance manipulations applied.",
)

HTTP_300_MSG = HTTPMessage(
    code=status.HTTP_300_MULTIPLE_CHOICES,
    message="Multiple response choices available.",
)

HTTP_301_MSG = HTTPMessage(
    code=status.HTTP_301_MOVED_PERMANENTLY,
    message="Resource moved permanently to a new URI.",
)

HTTP_302_MSG = HTTPMessage(
    code=status.HTTP_302_FOUND, message="Resource found at a different URI temporarily."
)

HTTP_303_MSG = HTTPMessage(
    code=status.HTTP_303_SEE_OTHER, message="Retrieve resource from a different URI."
)

HTTP_304_MSG = HTTPMessage(
    code=status.HTTP_304_NOT_MODIFIED,
    message="Resource not modified, use cached version.",
)

HTTP_305_MSG = HTTPMessage(
    code=status.HTTP_305_USE_PROXY, message="Access resource through specified proxy."
)

HTTP_306_MSG = HTTPMessage(
    code=status.HTTP_306_RESERVED, message="Reserved for future use."
)

HTTP_307_MSG = HTTPMessage(
    code=status.HTTP_307_TEMPORARY_REDIRECT,
    message="Resource temporarily under a different URI.",
)

HTTP_308_MSG = HTTPMessage(
    code=status.HTTP_308_PERMANENT_REDIRECT,
    message="Resource permanently moved to a new URI.",
)

HTTP_400_MSG = HTTPMessage(
    code=status.HTTP_400_BAD_REQUEST, message="Bad request due to malformed syntax."
)

HTTP_401_MSG = HTTPMessage(
    code=status.HTTP_401_UNAUTHORIZED, message="Authentication required and failed."
)

HTTP_402_MSG = HTTPMessage(
    code=status.HTTP_402_PAYMENT_REQUIRED, message="Payment required for this resource."
)

HTTP_403_MSG = HTTPMessage(
    code=status.HTTP_403_FORBIDDEN, message="Permission denied for this resource."
)

HTTP_404_MSG = HTTPMessage(
    code=status.HTTP_404_NOT_FOUND, message="Resource not found."
)

HTTP_405_MSG = HTTPMessage(
    code=status.HTTP_405_METHOD_NOT_ALLOWED,
    message="Method not allowed for this resource.",
)

HTTP_406_MSG = HTTPMessage(
    code=status.HTTP_406_NOT_ACCEPTABLE,
    message="Resource not available in acceptable format.",
)

HTTP_407_MSG = HTTPMessage(
    code=status.HTTP_407_PROXY_AUTHENTICATION_REQUIRED,
    message="Proxy authentication required.",
)

HTTP_408_MSG = HTTPMessage(
    code=status.HTTP_408_REQUEST_TIMEOUT, message="Request timeout, try again later."
)

HTTP_409_MSG = HTTPMessage(
    code=status.HTTP_409_CONFLICT, message="Conflict with current resource state."
)

HTTP_410_MSG = HTTPMessage(
    code=status.HTTP_410_GONE, message="Resource permanently removed."
)

HTTP_411_MSG = HTTPMessage(
    code=status.HTTP_411_LENGTH_REQUIRED, message="Content-Length header required."
)

HTTP_412_MSG = HTTPMessage(
    code=status.HTTP_412_PRECONDITION_FAILED, message="Precondition failed."
)

HTTP_413_MSG = HTTPMessage(
    code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, message="Payload too large."
)

HTTP_414_MSG = HTTPMessage(
    code=status.HTTP_414_REQUEST_URI_TOO_LONG, message="URI too long."
)

HTTP_415_MSG = HTTPMessage(
    code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, message="Unsupported media type."
)

HTTP_416_MSG = HTTPMessage(
    code=status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE,
    message="Requested range not satisfiable.",
)

HTTP_417_MSG = HTTPMessage(
    code=status.HTTP_417_EXPECTATION_FAILED, message="Expectation failed."
)

HTTP_418_MSG = HTTPMessage(
    code=status.HTTP_418_IM_A_TEAPOT, message="I'm a teapot, can't brew coffee."
)

HTTP_421_MSG = HTTPMessage(
    code=status.HTTP_421_MISDIRECTED_REQUEST,
    message="Request misdirected to inappropriate server.",
)

HTTP_422_MSG = HTTPMessage(
    code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    message="Unprocessable entity due to semantic errors.",
)

HTTP_423_MSG = HTTPMessage(
    code=status.HTTP_423_LOCKED,
    message="Resource is locked.",
)

HTTP_424_MSG = HTTPMessage(
    code=status.HTTP_424_FAILED_DEPENDENCY,
    message="Failed dependency in previous request.",
)

HTTP_425_MSG = HTTPMessage(
    code=status.HTTP_425_TOO_EARLY, message="Request too early, try again later."
)

HTTP_426_MSG = HTTPMessage(
    code=status.HTTP_426_UPGRADE_REQUIRED, message="Upgrade required."
)

HTTP_428_MSG = HTTPMessage(
    code=status.HTTP_428_PRECONDITION_REQUIRED, message="Precondition required."
)

HTTP_429_MSG = HTTPMessage(
    code=status.HTTP_429_TOO_MANY_REQUESTS,
    message="Too many requests, try again later.",
)

HTTP_431_MSG = HTTPMessage(
    code=status.HTTP_431_REQUEST_HEADER_FIELDS_TOO_LARGE,
    message="Request headers too large.",
)

HTTP_451_MSG = HTTPMessage(
    code=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS,
    message="Resource unavailable due to legal reasons.",
)

HTTP_500_MSG = HTTPMessage(
    code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    message="Internal server error, try again later.",
)

HTTP_501_MSG = HTTPMessage(
    code=status.HTTP_501_NOT_IMPLEMENTED, message="Not implemented."
)

HTTP_502_MSG = HTTPMessage(
    code=status.HTTP_502_BAD_GATEWAY, message="Bad gateway, try again later."
)

HTTP_503_MSG = HTTPMessage(
    code=status.HTTP_503_SERVICE_UNAVAILABLE,
    message="Service unavailable, try again later.",
)

HTTP_504_MSG = HTTPMessage(
    code=status.HTTP_504_GATEWAY_TIMEOUT, message="Gateway timeout, try again later."
)

HTTP_505_MSG = HTTPMessage(
    code=status.HTTP_505_HTTP_VERSION_NOT_SUPPORTED,
    message="HTTP version not supported.",
)

HTTP_506_MSG = HTTPMessage(
    code=status.HTTP_506_VARIANT_ALSO_NEGOTIATES, message="Variant negotiation error."
)

HTTP_507_MSG = HTTPMessage(
    code=status.HTTP_507_INSUFFICIENT_STORAGE, message="Insufficient storage."
)

HTTP_508_MSG = HTTPMessage(
    code=status.HTTP_508_LOOP_DETECTED, message="Infinite loop detected."
)

HTTP_510_MSG = HTTPMessage(
    code=status.HTTP_510_NOT_EXTENDED, message="Request requires further extensions."
)

HTTP_511_MSG = HTTPMessage(
    code=status.HTTP_511_NETWORK_AUTHENTICATION_REQUIRED,
    message="Network authentication required.",
)

HTTP_MSG_MAPPING = {
    100: HTTP_100_MSG,
    101: HTTP_101_MSG,
    102: HTTP_102_MSG,
    103: HTTP_103_MSG,
    200: HTTP_200_MSG,
    201: HTTP_201_MSG,
    202: HTTP_202_MSG,
    203: HTTP_203_MSG,
    204: HTTP_204_MSG,
    205: HTTP_205_MSG,
    206: HTTP_206_MSG,
    207: HTTP_207_MSG,
    208: HTTP_208_MSG,
    226: HTTP_226_MSG,
    300: HTTP_300_MSG,
    301: HTTP_301_MSG,
    302: HTTP_302_MSG,
    303: HTTP_303_MSG,
    304: HTTP_304_MSG,
    305: HTTP_305_MSG,
    306: HTTP_306_MSG,
    307: HTTP_307_MSG,
    308: HTTP_308_MSG,
    400: HTTP_400_MSG,
    401: HTTP_401_MSG,
    402: HTTP_402_MSG,
    403: HTTP_403_MSG,
    404: HTTP_404_MSG,
    405: HTTP_405_MSG,
    406: HTTP_406_MSG,
    407: HTTP_407_MSG,
    408: HTTP_408_MSG,
    409: HTTP_409_MSG,
    410: HTTP_410_MSG,
    411: HTTP_411_MSG,
    412: HTTP_412_MSG,
    413: HTTP_413_MSG,
    414: HTTP_414_MSG,
    415: HTTP_415_MSG,
    416: HTTP_416_MSG,
    417: HTTP_417_MSG,
    418: HTTP_418_MSG,
    421: HTTP_421_MSG,
    422: HTTP_422_MSG,
    423: HTTP_423_MSG,
    424: HTTP_424_MSG,
    425: HTTP_425_MSG,
    426: HTTP_426_MSG,
    428: HTTP_428_MSG,
    429: HTTP_429_MSG,
    431: HTTP_431_MSG,
    451: HTTP_451_MSG,
    500: HTTP_500_MSG,
    501: HTTP_501_MSG,
    502: HTTP_502_MSG,
    503: HTTP_503_MSG,
    504: HTTP_504_MSG,
    505: HTTP_505_MSG,
    506: HTTP_506_MSG,
    507: HTTP_507_MSG,
    508: HTTP_508_MSG,
    510: HTTP_510_MSG,
    511: HTTP_511_MSG,
}
