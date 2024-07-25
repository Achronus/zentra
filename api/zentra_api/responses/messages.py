from pydantic import BaseModel, Field, field_validator
from fastapi import status


class HTTPMessage(BaseModel):
    """A model for HTTP messages."""

    status_code: int = Field(..., description="The HTTP response code.")
    detail: str = Field(..., description="The reason the response occured.")
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
    status_code=status.HTTP_100_CONTINUE, detail="Continue sending the request body."
)

HTTP_101_MSG = HTTPMessage(
    status_code=status.HTTP_101_SWITCHING_PROTOCOLS,
    detail="Switching protocols as requested.",
)

HTTP_102_MSG = HTTPMessage(
    status_code=status.HTTP_102_PROCESSING, detail="Processing request."
)

HTTP_103_MSG = HTTPMessage(
    status_code=status.HTTP_103_EARLY_HINTS,
    detail="Sending early hints.",
)

HTTP_200_MSG = HTTPMessage(
    status_code=status.HTTP_200_OK, detail="Request successful, resource returned."
)

HTTP_201_MSG = HTTPMessage(
    status_code=status.HTTP_201_CREATED,
    detail="Request successful, new resource created.",
)

HTTP_202_MSG = HTTPMessage(
    status_code=status.HTTP_202_ACCEPTED,
    detail="Request accepted, processing not complete.",
)

HTTP_203_MSG = HTTPMessage(
    status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
    detail="Request successful, info may be from third-party.",
)

HTTP_204_MSG = HTTPMessage(
    status_code=status.HTTP_204_NO_CONTENT,
    detail="Request successful, no content in response.",
)

HTTP_205_MSG = HTTPMessage(
    status_code=status.HTTP_205_RESET_CONTENT,
    detail="Request successful, reset document view.",
)

HTTP_206_MSG = HTTPMessage(
    status_code=status.HTTP_206_PARTIAL_CONTENT,
    detail="Partial resource delivered due to range header.",
)

HTTP_207_MSG = HTTPMessage(
    status_code=status.HTTP_207_MULTI_STATUS,
    detail="Request successful, multiple statuses in response.",
)

HTTP_208_MSG = HTTPMessage(
    status_code=status.HTTP_208_ALREADY_REPORTED,
    detail="DAV bindings already enumerated in previous response.",
)

HTTP_226_MSG = HTTPMessage(
    status_code=status.HTTP_226_IM_USED,
    detail="GET request fulfilled, instance manipulations applied.",
)

HTTP_300_MSG = HTTPMessage(
    status_code=status.HTTP_300_MULTIPLE_CHOICES,
    detail="Multiple response choices available.",
)

HTTP_301_MSG = HTTPMessage(
    status_code=status.HTTP_301_MOVED_PERMANENTLY,
    detail="Resource moved permanently to a new URI.",
)

HTTP_302_MSG = HTTPMessage(
    status_code=status.HTTP_302_FOUND,
    detail="Resource found at a different URI temporarily.",
)

HTTP_303_MSG = HTTPMessage(
    status_code=status.HTTP_303_SEE_OTHER,
    detail="Retrieve resource from a different URI.",
)

HTTP_304_MSG = HTTPMessage(
    status_code=status.HTTP_304_NOT_MODIFIED,
    detail="Resource not modified, use cached version.",
)

HTTP_305_MSG = HTTPMessage(
    status_code=status.HTTP_305_USE_PROXY,
    detail="Access resource through specified proxy.",
)

HTTP_306_MSG = HTTPMessage(
    status_code=status.HTTP_306_RESERVED, detail="Reserved for future use."
)

HTTP_307_MSG = HTTPMessage(
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    detail="Resource temporarily under a different URI.",
)

HTTP_308_MSG = HTTPMessage(
    status_code=status.HTTP_308_PERMANENT_REDIRECT,
    detail="Resource permanently moved to a new URI.",
)

HTTP_400_MSG = HTTPMessage(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Bad request due to malformed syntax.",
)

HTTP_401_MSG = HTTPMessage(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Authentication required and failed.",
)

HTTP_402_MSG = HTTPMessage(
    status_code=status.HTTP_402_PAYMENT_REQUIRED,
    detail="Payment required for this resource.",
)

HTTP_403_MSG = HTTPMessage(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Permission denied for this resource.",
)

HTTP_404_MSG = HTTPMessage(
    status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found."
)

HTTP_405_MSG = HTTPMessage(
    status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
    detail="Method not allowed for this resource.",
)

HTTP_406_MSG = HTTPMessage(
    status_code=status.HTTP_406_NOT_ACCEPTABLE,
    detail="Resource not available in acceptable format.",
)

HTTP_407_MSG = HTTPMessage(
    status_code=status.HTTP_407_PROXY_AUTHENTICATION_REQUIRED,
    detail="Proxy authentication required.",
)

HTTP_408_MSG = HTTPMessage(
    status_code=status.HTTP_408_REQUEST_TIMEOUT,
    detail="Request timeout, try again later.",
)

HTTP_409_MSG = HTTPMessage(
    status_code=status.HTTP_409_CONFLICT,
    detail="Conflict with current resource state.",
)

HTTP_410_MSG = HTTPMessage(
    status_code=status.HTTP_410_GONE, detail="Resource permanently removed."
)

HTTP_411_MSG = HTTPMessage(
    status_code=status.HTTP_411_LENGTH_REQUIRED,
    detail="Content-Length header required.",
)

HTTP_412_MSG = HTTPMessage(
    status_code=status.HTTP_412_PRECONDITION_FAILED, detail="Precondition failed."
)

HTTP_413_MSG = HTTPMessage(
    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="Payload too large."
)

HTTP_414_MSG = HTTPMessage(
    status_code=status.HTTP_414_REQUEST_URI_TOO_LONG, detail="URI too long."
)

HTTP_415_MSG = HTTPMessage(
    status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
    detail="Unsupported media type.",
)

HTTP_416_MSG = HTTPMessage(
    status_code=status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE,
    detail="Requested range not satisfiable.",
)

HTTP_417_MSG = HTTPMessage(
    status_code=status.HTTP_417_EXPECTATION_FAILED, detail="Expectation failed."
)

HTTP_418_MSG = HTTPMessage(
    status_code=status.HTTP_418_IM_A_TEAPOT, detail="I'm a teapot, can't brew coffee."
)

HTTP_421_MSG = HTTPMessage(
    status_code=status.HTTP_421_MISDIRECTED_REQUEST,
    detail="Request misdirected to inappropriate server.",
)

HTTP_422_MSG = HTTPMessage(
    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    detail="Unprocessable entity due to semantic errors.",
)

HTTP_423_MSG = HTTPMessage(
    status_code=status.HTTP_423_LOCKED,
    detail="Resource is locked.",
)

HTTP_424_MSG = HTTPMessage(
    status_code=status.HTTP_424_FAILED_DEPENDENCY,
    detail="Failed dependency in previous request.",
)

HTTP_425_MSG = HTTPMessage(
    status_code=status.HTTP_425_TOO_EARLY, detail="Request too early, try again later."
)

HTTP_426_MSG = HTTPMessage(
    status_code=status.HTTP_426_UPGRADE_REQUIRED, detail="Upgrade required."
)

HTTP_428_MSG = HTTPMessage(
    status_code=status.HTTP_428_PRECONDITION_REQUIRED, detail="Precondition required."
)

HTTP_429_MSG = HTTPMessage(
    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
    detail="Too many requests, try again later.",
)

HTTP_431_MSG = HTTPMessage(
    status_code=status.HTTP_431_REQUEST_HEADER_FIELDS_TOO_LARGE,
    detail="Request headers too large.",
)

HTTP_451_MSG = HTTPMessage(
    status_code=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS,
    detail="Resource unavailable due to legal reasons.",
)

HTTP_500_MSG = HTTPMessage(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Internal server error, try again later.",
)

HTTP_501_MSG = HTTPMessage(
    status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented."
)

HTTP_502_MSG = HTTPMessage(
    status_code=status.HTTP_502_BAD_GATEWAY, detail="Bad gateway, try again later."
)

HTTP_503_MSG = HTTPMessage(
    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
    detail="Service unavailable, try again later.",
)

HTTP_504_MSG = HTTPMessage(
    status_code=status.HTTP_504_GATEWAY_TIMEOUT,
    detail="Gateway timeout, try again later.",
)

HTTP_505_MSG = HTTPMessage(
    status_code=status.HTTP_505_HTTP_VERSION_NOT_SUPPORTED,
    detail="HTTP version not supported.",
)

HTTP_506_MSG = HTTPMessage(
    status_code=status.HTTP_506_VARIANT_ALSO_NEGOTIATES,
    detail="Variant negotiation error.",
)

HTTP_507_MSG = HTTPMessage(
    status_code=status.HTTP_507_INSUFFICIENT_STORAGE, detail="Insufficient storage."
)

HTTP_508_MSG = HTTPMessage(
    status_code=status.HTTP_508_LOOP_DETECTED, detail="Infinite loop detected."
)

HTTP_510_MSG = HTTPMessage(
    status_code=status.HTTP_510_NOT_EXTENDED,
    detail="Request requires further extensions.",
)

HTTP_511_MSG = HTTPMessage(
    status_code=status.HTTP_511_NETWORK_AUTHENTICATION_REQUIRED,
    detail="Network authentication required.",
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
