import re
from pydantic import BaseModel, Field
from pydantic_core import PydanticCustomError

from zentra.base.library import CustomModel
from zentra.core.constants import PARAMETER_PREFIX

VALID_URL_SCHEMES = (
    "/",
    "./",
    "../",
    "ftp://",
    "file://",
    "mailto:",
    "tel:",
    "http://",
    "https://",
)


class CustomUrl(BaseModel, CustomModel):
    """A custom Url model for handling the `href` and `src` attributes in Zentra models.

    Parameters:
    - `url` (`string`) - can start with any of the following:
    `['/', './' '../', 'ftp://', 'file://', 'mailto:', 'tel:', 'http://', 'https://']`
    - `is_param` (`boolean, optional`) - a flag to include the `url` as a parameter (starting with a `$.`). `False` by default
    """

    url: str = Field(max_length=2083)
    is_param: bool = False

    def validate_url(self) -> None:
        valid_schemes = (
            VALID_URL_SCHEMES + (PARAMETER_PREFIX,)
            if self.is_param
            else VALID_URL_SCHEMES
        )

        if not self.url.startswith(valid_schemes):
            raise PydanticCustomError(
                "invalid_url_start",
                f"must start with one of the following: '{list(valid_schemes)}'\n",
                dict(wrong_value=self.url),
            )

        if bool(re.search(r"\s", self.url)):
            raise PydanticCustomError(
                "invalid_url",
                "cannot contain whitespace",
                dict(wrong_value=self.url),
            )
