from enum import Enum, StrEnum


class JWTAlgorithm(StrEnum):
    HS256 = "HS256"
    HS384 = "HS384"
    HS512 = "HS512"


class JWTSize(Enum):
    HS256 = 256
    HS384 = 384
    HS512 = 512
