from pydantic import BaseModel, ConfigDict

from .enums import TokenType


class Token(BaseModel):
    """
    A model for storing token data.

    Parameters:
    - `access_token` (`string`) - the JWT access token
    - `token_type` (`zentra_api.enums.TokenType`) - the token type. Valid options: `['bearer', 'api_key', 'oauth_access', 'oauth_refresh']`
    """

    access_token: str
    token_type: TokenType

    model_config = ConfigDict(use_enum_values=True)
