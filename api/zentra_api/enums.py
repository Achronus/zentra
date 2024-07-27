from enum import StrEnum


class TokenType(StrEnum):
    BEARER = "bearer"
    API_KEY = "api_key"
    OAUTH_ACCESS = "oauth_access"
    OAUTH_REFRESH = "oauth_refresh"
