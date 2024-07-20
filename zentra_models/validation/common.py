import re
from typing import Any
from pydantic_core import PydanticCustomError

from .constants import PARAMETER_PREFIX

from zentra_models.custom import CustomUrl


def has_valid_pattern(*, pattern: str, value: str) -> bool:
    match = re.match(pattern, value)
    return bool(match)


def check_kebab_case(name: str) -> str:
    """A helper validation function to check if a string is in kebab-case format."""
    if not has_valid_pattern(pattern=r"^[a-z]+(-[a-z]+)*$", value=name):
        raise PydanticCustomError(
            "invalid_name_format",
            f"'{name}' must be in kebab-case format",
            dict(wrong_value=name),
        )

    return name


def check_pattern_match(pattern: str, text: str, err_msg: str) -> str:
    """A helper validation method for checking if a set of text matches a given pattern."""
    result = has_valid_pattern(pattern=pattern, value=text)

    if not result:
        raise PydanticCustomError(
            "string_pattern_mismatch",
            err_msg,
            dict(wrong_value=text, pattern=pattern),
        )

    return text


def key_attr_validation(key: str) -> str:
    """A helper validation function that ensures the `key` attribute value is a valid parameter value."""
    if key and not key.startswith(PARAMETER_PREFIX):
        raise PydanticCustomError(
            "key_must_be_a_parameter",
            f"'{key}' != '{PARAMETER_PREFIX}{key}'! Must start with a '{PARAMETER_PREFIX}' to set as a parameter\n",
            dict(wrong_value=key),
        )
    return key


def pathname_validation(name: str) -> str:
    """A helper validation function that validates the `UrlQuery` pathname attribute."""
    if not name.startswith("/"):
        raise PydanticCustomError(
            "invalid_string",
            "must start with a '/'",
            dict(wrong_value=name),
        )
    return name


def url_validation(url: Any, is_param: bool = False) -> Any:
    """A helper validation function for verifying the `src`, `href`, and `url` attribute values."""
    if isinstance(url, str):
        CustomUrl(url=url, is_param=is_param).validate_url()

    return url


def local_url_validation(url: str) -> str:
    """A helper validation function that validates if a `url` value is starts with a `/`."""
    if not url.startswith("/"):
        raise PydanticCustomError(
            "invalid_url",
            "must be a local URL and start with a '/'!",
            dict(wrong_value=url),
        )

    return url
