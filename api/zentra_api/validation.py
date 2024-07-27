import re
from pydantic import BaseModel, field_validator
from pydantic_core import PydanticCustomError


ENV_FILE_NAME = r"^\.env(\.[a-zA-Z0-9-]+)*$"


class EnvFilename(BaseModel):
    name: str

    @field_validator("name")
    def validate_filename(cls, name: str) -> str:
        if not re.match(ENV_FILE_NAME, name):
            raise PydanticCustomError(
                "invalid_filename",
                "Invalid filename. Must start with '.env' and contain only letters (a-zA-Z), dots (.) or dashes (-)",
                dict(wrong_value=name),
            )
        return name
