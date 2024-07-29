from datetime import datetime, timedelta, timezone

from zentra_api.config import AuthConfig
from zentra_api.responses.exc import CREDENTIALS_EXCEPTION

import jwt
from pydantic import BaseModel


class SecurityUtils(BaseModel):
    """
    Contains utility methods for managing user authentication.

    Parameters:
    - `auth` (`zentra_api.config.AuthConfig`) - a ZentraAPI `AuthConfig` model
    """

    auth: AuthConfig

    def hash_password(self, password: str) -> str:
        """Uses the `pwd_context` to hash a password."""
        return self.auth.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> str:
        """Uses the `pwd_context` to verify a password."""
        return self.auth.pwd_context.verify(plain_password, hashed_password)

    def expiration(self, expires_delta: timedelta | None = None) -> datetime:
        """Creates an expiration `datetime` given a `timedelta`. If `None`, applies the `settings.AUTH.ACCESS_TOKEN_EXPIRE_MINS` automatically."""
        if expires_delta:
            return datetime.now(timezone.utc) + expires_delta

        return datetime.now(timezone.utc) + self.expire_mins()

    def expire_mins(self) -> timedelta:
        """Returns the access token expire minutes as a timedelta."""
        return timedelta(minutes=self.auth.ACCESS_TOKEN_EXPIRE_MINS)

    def encrypt(self, model: BaseModel, attributes: str | list[str]) -> BaseModel:
        """Encrypts a set of data in a model and returns it as a new model."""
        if isinstance(attributes, str):
            attributes = [attributes]

        data = model.model_dump()
        for attr in attributes:
            try:
                hashed_value = self.hash_password(getattr(model, attr))
                data[attr] = hashed_value

            except AttributeError:
                raise AttributeError(f"'{attr}' does not exist in '{type(model)}'!")

        return type(model)(**data)

    def create_access_token(
        self, data: dict, expires_delta: timedelta | None = None
    ) -> str:
        """Encodes a set of data as a JSON Web Token (JWT) and returns it."""
        payload = data.copy()
        expire = self.expiration(expires_delta)

        payload.update({"exp": expire})
        encoded_jwt = jwt.encode(
            payload,
            key=self.auth.SECRET_KEY,
            algorithm=self.auth.ALGORITHM,
        )
        return encoded_jwt

    def get_token_data(self, token: str) -> str:
        """Extracts the payload data from the given token and returns it."""
        try:
            payload: dict = jwt.decode(
                token,
                key=self.auth.SECRET_KEY,
                algorithms=[self.auth.ALGORITHM],
            )
            token_data: str | None = payload.get("sub")

            if token_data is None:
                raise CREDENTIALS_EXCEPTION

            return token_data

        except jwt.InvalidTokenError:
            raise CREDENTIALS_EXCEPTION
