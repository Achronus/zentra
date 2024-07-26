from enum import Enum


class JWTAlgorithm(Enum):
    HS256 = 256
    HS384 = 384
    HS512 = 512
