from datetime import datetime, timedelta, timezone

from zentra_api.config import Settings
from zentra_api.responses.exception import CREDENTIALS_EXCEPTION

import jwt
from pydantic import BaseModel


class SecurityUtils(BaseModel):
    """
    Contains utility methods for managing user authentication.

    Parameters:
    - `settings` (`zentra_api.config.Settings`) - a ZentraAPI settings model
    """

    settings: Settings

    def hash_password(self, password: str) -> str:
        """Uses the `pwd_context` to hash a password."""
        return self.settings.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> str:
        """Uses the `pwd_context` to verify a password."""
        return self.settings.pwd_context.verify(plain_password, hashed_password)

    def encrypt(self, model: BaseModel, attributes: str | list[str]) -> BaseModel:
        """Encrypts a set of data in a model and returns it as a new model."""
        if isinstance(attributes, str):
            attributes = [attributes]

        data = model.model_dump()
        for attr in attributes:
            try:
                hashed_value = self.hash_password(getattr(model, attr))
                data[attr] = hashed_value

            except KeyError:
                raise KeyError(f"'{attr}' does not exist in '{type(model)}'!")

        return type(model)(**data)

    def create_access_token(
        self, data: dict, expires_delta: timedelta | None = None
    ) -> str:
        """Encodes a set of data as a JSON Web Token (JWT) and returns it."""
        payload = data.copy()

        expire_date = datetime.now(timezone.utc)
        expire = (
            expire_date + expires_delta
            if expires_delta
            else expire_date + timedelta(minutes=15)
        )

        payload.update({"exp": expire})
        encoded_jwt = jwt.encode(
            payload,
            key=self.settings.AUTH.SECRET_KEY,
            algorithm=self.settings.AUTH.ALGORITHM,
        )
        return encoded_jwt

    def get_token_data(self, token: str) -> str:
        """Extracts the payload data from the given token and returns it."""
        try:
            payload: dict = jwt.decode(
                token,
                self.settings.AUTH.SECRET_KEY,
                algorithms=[self.settings.AUTH.ALGORITHM],
            )
            token_data: str | None = payload.get("sub")

            if token_data is None:
                raise CREDENTIALS_EXCEPTION

            return token_data

        except jwt.InvalidTokenError:
            raise CREDENTIALS_EXCEPTION
