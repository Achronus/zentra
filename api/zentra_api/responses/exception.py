from fastapi import HTTPException

from .messages import HTTP_MSG_MAPPING, HTTPMessage


class BaseCustomHTTPException(HTTPException):
    def __init__(
        self,
        msg: HTTPMessage,
        detail: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> None:
        self.msg = msg

        self.status_code = self.msg.status_code
        self.detail = detail if detail else self.msg.detail
        self.headers = headers if headers else self.msg.headers


class HTTP100Exception(BaseCustomHTTPException):
    def __init__(
        self, message: str | None = None, headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(HTTP_MSG_MAPPING[100], message, headers)


class HTTP101Exception(BaseCustomHTTPException):
    def __init__(
        self, message: str | None = None, headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(HTTP_MSG_MAPPING[101], message, headers)


class HTTP102Exception(BaseCustomHTTPException):
    def __init__(
        self, message: str | None = None, headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(HTTP_MSG_MAPPING[102], message, headers)


class HTTP103Exception(BaseCustomHTTPException):
    def __init__(
        self, message: str | None = None, headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(HTTP_MSG_MAPPING[103], message, headers)


class HTTP300Exception(BaseCustomHTTPException):
    def __init__(
        self, message: str | None = None, headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(HTTP_MSG_MAPPING[300], message, headers)


class HTTP301Exception(BaseCustomHTTPException):
    def __init__(
        self, message: str | None = None, headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(HTTP_MSG_MAPPING[301], message, headers)


class HTTP302Exception(BaseCustomHTTPException):
    def __init__(
        self, message: str | None = None, headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(HTTP_MSG_MAPPING[302], message, headers)


class HTTP303Exception(BaseCustomHTTPException):
    def __init__(
        self, message: str | None = None, headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(HTTP_MSG_MAPPING[303], message, headers)


class HTTP304Exception(BaseCustomHTTPException):
    def __init__(
        self, message: str | None = None, headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(HTTP_MSG_MAPPING[304], message, headers)


class HTTP305Exception(BaseCustomHTTPException):
    def __init__(
        self, message: str | None = None, headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(HTTP_MSG_MAPPING[305], message, headers)


class HTTP306Exception(BaseCustomHTTPException):
    def __init__(
        self, message: str | None = None, headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(HTTP_MSG_MAPPING[306], message, headers)


class HTTP307Exception(BaseCustomHTTPException):
    def __init__(
        self, message: str | None = None, headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(HTTP_MSG_MAPPING[307], message, headers)


class HTTP308Exception(BaseCustomHTTPException):
    def __init__(
        self, message: str | None = None, headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(HTTP_MSG_MAPPING[308], message, headers)


class HTTP400Exception(BaseCustomHTTPException):
    def __init__(
        self, message: str | None = None, headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(HTTP_MSG_MAPPING[400], message, headers)


class HTTP401Exception(BaseCustomHTTPException):
    def __init__(
        self, message: str | None = None, headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(HTTP_MSG_MAPPING[401], message, headers)


class HTTP402Exception(BaseCustomHTTPException):
    def __init__(
        self, message: str | None = None, headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(HTTP_MSG_MAPPING[402], message, headers)


class HTTP403Exception(BaseCustomHTTPException):
    def __init__(
        self, message: str | None = None, headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(HTTP_MSG_MAPPING[403], message, headers)


class HTTP404Exception(BaseCustomHTTPException):
    def __init__(
        self, message: str | None = None, headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(HTTP_MSG_MAPPING[404], message, headers)


class HTTP405Exception(BaseCustomHTTPException):
    def __init__(
        self, message: str | None = None, headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(HTTP_MSG_MAPPING[405], message, headers)


class HTTP406Exception(BaseCustomHTTPException):
    def __init__(
        self, message: str | None = None, headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(HTTP_MSG_MAPPING[406], message, headers)


class HTTP407Exception(BaseCustomHTTPException):
    def __init__(
        self, message: str | None = None, headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(HTTP_MSG_MAPPING[407], message, headers)


class HTTP408Exception(BaseCustomHTTPException):
    def __init__(
        self, message: str | None = None, headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(HTTP_MSG_MAPPING[408], message, headers)


class HTTP409Exception(BaseCustomHTTPException):
    def __init__(
        self, message: str | None = None, headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(HTTP_MSG_MAPPING[409], message, headers)


class HTTP410Exception(BaseCustomHTTPException):
    def __init__(
        self, message: str | None = None, headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(HTTP_MSG_MAPPING[410], message, headers)


class HTTP411Exception(BaseCustomHTTPException):
    def __init__(
        self, message: str | None = None, headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(HTTP_MSG_MAPPING[411], message, headers)


class HTTP412Exception(BaseCustomHTTPException):
    def __init__(
        self, message: str | None = None, headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(HTTP_MSG_MAPPING[412], message, headers)


class HTTP413Exception(BaseCustomHTTPException):
    def __init__(
        self, message: str | None = None, headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(HTTP_MSG_MAPPING[413], message, headers)


class HTTP414Exception(BaseCustomHTTPException):
    def __init__(
        self, message: str | None = None, headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(HTTP_MSG_MAPPING[414], message, headers)


class HTTP415Exception(BaseCustomHTTPException):
    def __init__(
        self, message: str | None = None, headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(HTTP_MSG_MAPPING[415], message, headers)


class HTTP416Exception(BaseCustomHTTPException):
    def __init__(
        self, message: str | None = None, headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(HTTP_MSG_MAPPING[416], message, headers)


class HTTP417Exception(BaseCustomHTTPException):
    def __init__(
        self, message: str | None = None, headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(HTTP_MSG_MAPPING[417], message, headers)


class HTTP418Exception(BaseCustomHTTPException):
    def __init__(
        self, message: str | None = None, headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(HTTP_MSG_MAPPING[418], message, headers)


class HTTP421Exception(BaseCustomHTTPException):
    def __init__(
        self, message: str | None = None, headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(HTTP_MSG_MAPPING[421], message, headers)


class HTTP422Exception(BaseCustomHTTPException):
    def __init__(
        self, message: str | None = None, headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(HTTP_MSG_MAPPING[422], message, headers)


class HTTP423Exception(BaseCustomHTTPException):
    def __init__(
        self, message: str | None = None, headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(HTTP_MSG_MAPPING[423], message, headers)


class HTTP424Exception(BaseCustomHTTPException):
    def __init__(
        self, message: str | None = None, headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(HTTP_MSG_MAPPING[424], message, headers)


class HTTP425Exception(BaseCustomHTTPException):
    def __init__(
        self, message: str | None = None, headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(HTTP_MSG_MAPPING[425], message, headers)


class HTTP426Exception(BaseCustomHTTPException):
    def __init__(
        self, message: str | None = None, headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(HTTP_MSG_MAPPING[426], message, headers)


class HTTP428Exception(BaseCustomHTTPException):
    def __init__(
        self, message: str | None = None, headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(HTTP_MSG_MAPPING[428], message, headers)


class HTTP429Exception(BaseCustomHTTPException):
    def __init__(
        self, message: str | None = None, headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(HTTP_MSG_MAPPING[429], message, headers)


class HTTP431Exception(BaseCustomHTTPException):
    def __init__(
        self, message: str | None = None, headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(HTTP_MSG_MAPPING[431], message, headers)


class HTTP451Exception(BaseCustomHTTPException):
    def __init__(
        self, message: str | None = None, headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(HTTP_MSG_MAPPING[451], message, headers)


class HTTP500Exception(BaseCustomHTTPException):
    def __init__(
        self, message: str | None = None, headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(HTTP_MSG_MAPPING[500], message, headers)


class HTTP501Exception(BaseCustomHTTPException):
    def __init__(
        self, message: str | None = None, headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(HTTP_MSG_MAPPING[501], message, headers)


class HTTP502Exception(BaseCustomHTTPException):
    def __init__(
        self, message: str | None = None, headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(HTTP_MSG_MAPPING[502], message, headers)


class HTTP503Exception(BaseCustomHTTPException):
    def __init__(
        self, message: str | None = None, headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(HTTP_MSG_MAPPING[503], message, headers)


class HTTP504Exception(BaseCustomHTTPException):
    def __init__(
        self, message: str | None = None, headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(HTTP_MSG_MAPPING[504], message, headers)


class HTTP505Exception(BaseCustomHTTPException):
    def __init__(
        self, message: str | None = None, headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(HTTP_MSG_MAPPING[505], message, headers)


class HTTP506Exception(BaseCustomHTTPException):
    def __init__(
        self, message: str | None = None, headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(HTTP_MSG_MAPPING[506], message, headers)


class HTTP507Exception(BaseCustomHTTPException):
    def __init__(
        self, message: str | None = None, headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(HTTP_MSG_MAPPING[507], message, headers)


class HTTP508Exception(BaseCustomHTTPException):
    def __init__(
        self, message: str | None = None, headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(HTTP_MSG_MAPPING[508], message, headers)


class HTTP510Exception(BaseCustomHTTPException):
    def __init__(
        self, message: str | None = None, headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(HTTP_MSG_MAPPING[510], message, headers)


class HTTP511Exception(BaseCustomHTTPException):
    def __init__(
        self, message: str | None = None, headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(HTTP_MSG_MAPPING[511], message, headers)
