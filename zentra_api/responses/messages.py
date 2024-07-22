from pydantic import BaseModel, Field, field_validator
from fastapi import status


class HTTPMessage(BaseModel):
    """A model for HTTP messages."""

    code: int = Field(..., description="The HTTP response code.")
    message: str = Field(..., description="The reason the response occured.")
    headers: dict[str, str] | None = Field(
        default=None, description="The headers to send with the response (optional)."
    )

    @field_validator("headers")
    def validate_headers(cls, headers: dict[str, str] | None) -> dict:
        if headers is None:
            return {}

        return headers


class HTTPSuccess(BaseModel):
    pass


HTTP_100_MSG = HTTPMessage(
    code=status.HTTP_100_CONTINUE,
    message="The server has received the request headers and the client should proceed to send the request body.",
)

HTTP_101_MSG = HTTPMessage(
    code=status.HTTP_101_SWITCHING_PROTOCOLS,
    message="The requester has asked the server to switch protocols and the server has agreed to do so.",
)

HTTP_102_MSG = HTTPMessage(
    code=status.HTTP_102_PROCESSING,
    message="The server has received and is processing the request, but no response is available yet.",
)

HTTP_103_MSG = HTTPMessage(
    code=status.HTTP_103_EARLY_HINTS,
    message="The server is sending some hints before the final HTTP message.",
)

HTTP_300_MSG = HTTPMessage(
    code=status.HTTP_300_MULTIPLE_CHOICES,
    message="The request has more than one possible response. The user or agent should choose one of them.",
)

HTTP_301_MSG = HTTPMessage(
    code=status.HTTP_301_MOVED_PERMANENTLY,
    message="The requested resource has been permanently moved to a new URI. The new URI should be provided in the response.",
)

HTTP_302_MSG = HTTPMessage(
    code=status.HTTP_302_FOUND,
    message="The requested resource resides temporarily under a different URI. The client should continue to use the original URI for future requests.",
)

HTTP_303_MSG = HTTPMessage(
    code=status.HTTP_303_SEE_OTHER,
    message="The response to the request can be found under a different URI using the GET method. The client should retrieve the resource from the new URI.",
)

HTTP_304_MSG = HTTPMessage(
    code=status.HTTP_304_NOT_MODIFIED,
    message="The requested resource has not been modified since the last request. The client can use the cached version of the resource.",
)

HTTP_305_MSG = HTTPMessage(
    code=status.HTTP_305_USE_PROXY,
    message="The requested resource must be accessed through the proxy given by the `Location` header. The client should follow the proxy instructions.",
)

HTTP_306_MSG = HTTPMessage(
    code=status.HTTP_306_RESERVED,
    message="This status code was used in a previous version of the HTTP specification. It is no longer used, and the code is reserved for future use.",
)

HTTP_307_MSG = HTTPMessage(
    code=status.HTTP_307_TEMPORARY_REDIRECT,
    message="The requested resource resides temporarily under a different URI. The client should continue to use the original URI for future requests.",
)

HTTP_308_MSG = HTTPMessage(
    code=status.HTTP_308_PERMANENT_REDIRECT,
    message="The requested resource has been permanently moved to a new URI. The new URI should be provided in the response, and the client should use the new URI for future requests.",
)

HTTP_400_MSG = HTTPMessage(
    code=status.HTTP_400_BAD_REQUEST,
    message="The request could not be understood by the server due to malformed syntax. Please check your request and try again.",
)

HTTP_401_MSG = HTTPMessage(
    code=status.HTTP_401_UNAUTHORIZED,
    message="Authentication is required and has failed or has not yet been provided. Please ensure your API key or login credentials are correct.",
)

HTTP_402_MSG = HTTPMessage(
    code=status.HTTP_402_PAYMENT_REQUIRED,
    message="Payment is required to access this resource. Please ensure your payment details are correct or update your subscription.",
)

HTTP_403_MSG = HTTPMessage(
    code=status.HTTP_403_FORBIDDEN,
    message="You do not have permission to access this resource. Please check your credentials and access rights.",
)

HTTP_404_MSG = HTTPMessage(
    code=status.HTTP_404_NOT_FOUND,
    message="The requested resource could not be found. Please check the endpoint URL and try again.",
)

HTTP_405_MSG = HTTPMessage(
    code=status.HTTP_405_METHOD_NOT_ALLOWED,
    message="The requested method is not allowed for the specified resource. Please check the API documentation for the correct method.",
)

HTTP_406_MSG = HTTPMessage(
    code=status.HTTP_406_NOT_ACCEPTABLE,
    message="The requested resource is not available in a format that would be acceptable to the client. Please check the request headers and acceptable formats.",
)

HTTP_407_MSG = HTTPMessage(
    code=status.HTTP_407_PROXY_AUTHENTICATION_REQUIRED,
    message="Authentication with the proxy server is required. Please ensure your proxy credentials are correct.",
)

HTTP_408_MSG = HTTPMessage(
    code=status.HTTP_408_REQUEST_TIMEOUT,
    message="The server timed out waiting for the request. Please try again later.",
)

HTTP_409_MSG = HTTPMessage(
    code=status.HTTP_409_CONFLICT,
    message="There is a conflict with the current state of the resource. Please review your request for any conflicts and try again.",
)

HTTP_410_MSG = HTTPMessage(
    code=status.HTTP_410_GONE,
    message="The requested resource is no longer available and has been permanently removed. Please update your request to use a different resource.",
)

HTTP_411_MSG = HTTPMessage(
    code=status.HTTP_411_LENGTH_REQUIRED,
    message="The server requires the Content-Length header field in the request. Please include this header and try again.",
)

HTTP_412_MSG = HTTPMessage(
    code=status.HTTP_412_PRECONDITION_FAILED,
    message="One or more preconditions given in the request header fields evaluated to false. Please review your request headers and try again.",
)

HTTP_413_MSG = HTTPMessage(
    code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
    message="The request payload is too large for the server to process. Please reduce the size of your request and try again.",
)

HTTP_414_MSG = HTTPMessage(
    code=status.HTTP_414_REQUEST_URI_TOO_LONG,
    message="The URI provided was too long for the server to process. Please shorten the URI and try again.",
)

HTTP_415_MSG = HTTPMessage(
    code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
    message="The media type of the request is not supported by the server. Please check the API documentation for supported media types.",
)

HTTP_416_MSG = HTTPMessage(
    code=status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE,
    message="The range specified in the request is not satisfiable. Please check the requested range and try again.",
)

HTTP_417_MSG = HTTPMessage(
    code=status.HTTP_417_EXPECTATION_FAILED,
    message="The server could not meet the expectation given in the request header. Please review your request headers and try again.",
)

HTTP_418_MSG = HTTPMessage(
    code=status.HTTP_418_IM_A_TEAPOT,
    message="The server refuses the attempt to brew coffee with a teapot. Please check your request and try again.",
)

HTTP_422_MSG = HTTPMessage(
    code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    message="The request was well-formed but was unable to be followed due to semantic errors. Please check your request data and try again.",
)

HTTP_423_MSG = HTTPMessage(
    code=status.HTTP_423_LOCKED,
    message="The resource that is being accessed is locked. Please check the status of the resource and try again later.",
)

HTTP_424_MSG = HTTPMessage(
    code=status.HTTP_424_FAILED_DEPENDENCY,
    message="The request failed due to failure of a previous request. Please ensure all dependencies are met and try again.",
)

HTTP_426_MSG = HTTPMessage(
    code=status.HTTP_426_UPGRADE_REQUIRED,
    message="The client should switch to a different protocol. Please check the API documentation for the required protocol.",
)

HTTP_428_MSG = HTTPMessage(
    code=status.HTTP_428_PRECONDITION_REQUIRED,
    message="The server requires the request to be conditional. Please include the necessary preconditions and try again.",
)

HTTP_429_MSG = HTTPMessage(
    code=status.HTTP_429_TOO_MANY_REQUESTS,
    message="You have sent too many requests in a given amount of time. Please try again later.",
)

HTTP_431_MSG = HTTPMessage(
    code=status.HTTP_431_REQUEST_HEADER_FIELDS_TOO_LARGE,
    message="The server is unwilling to process the request because its header fields are too large. Please reduce the size of the request headers and try again.",
)

HTTP_451_MSG = HTTPMessage(
    code=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS,
    message="The requested resource is unavailable due to legal reasons. Please check the legal constraints and try again.",
)

HTTP_500_MSG = HTTPMessage(
    code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    message="The server encountered an internal error and was unable to complete your request. Please try again later.",
)

HTTP_501_MSG = HTTPMessage(
    code=status.HTTP_501_NOT_IMPLEMENTED,
    message="The server does not support the functionality required to fulfill the request. Please check the API documentation for supported functionality.",
)

HTTP_502_MSG = HTTPMessage(
    code=status.HTTP_502_BAD_GATEWAY,
    message="The server received an invalid response from the upstream server while trying to fulfill the request. Please try again later.",
)

HTTP_503_MSG = HTTPMessage(
    code=status.HTTP_503_SERVICE_UNAVAILABLE,
    message="The server is currently unable to handle the request due to a temporary overload or scheduled maintenance. Please try again later.",
)

HTTP_504_MSG = HTTPMessage(
    code=status.HTTP_504_GATEWAY_TIMEOUT,
    message="The server, while acting as a gateway or proxy, did not receive a timely response from the upstream server. Please try again later.",
)

HTTP_505_MSG = HTTPMessage(
    code=status.HTTP_505_HTTP_VERSION_NOT_SUPPORTED,
    message="The server does not support the HTTP protocol version used in the request. Please check the API documentation for supported HTTP versions.",
)

HTTP_506_MSG = HTTPMessage(
    code=status.HTTP_506_VARIANT_ALSO_NEGOTIATES,
    message="The server has an internal configuration error: transparent content negotiation for the request results in a circular reference. Please contact support.",
)

HTTP_507_MSG = HTTPMessage(
    code=status.HTTP_507_INSUFFICIENT_STORAGE,
    message="The server is unable to store the representation needed to complete the request. Please try again later.",
)

HTTP_508_MSG = HTTPMessage(
    code=status.HTTP_508_LOOP_DETECTED,
    message="The server detected an infinite loop while processing the request. Please check your request for any recursive references.",
)

HTTP_510_MSG = HTTPMessage(
    code=status.HTTP_510_NOT_EXTENDED,
    message="Further extensions to the request are required for the server to fulfill it. Please check the API documentation for required extensions.",
)

HTTP_511_MSG = HTTPMessage(
    code=status.HTTP_511_NETWORK_AUTHENTICATION_REQUIRED,
    message="The client needs to authenticate to gain network access. Please ensure your network credentials are correct and try again.",
)


HTTP_MSG_MAPPING = {
    100: HTTP_100_MSG,
    101: HTTP_101_MSG,
    102: HTTP_102_MSG,
    103: HTTP_103_MSG,
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
    422: HTTP_422_MSG,
    423: HTTP_423_MSG,
    424: HTTP_424_MSG,
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
