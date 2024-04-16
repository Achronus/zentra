from enum import Enum, IntEnum
from typing import Any

from pydantic import BaseModel, Field, field_validator
from pydantic_core import PydanticCustomError

from zentra.core import LOWER_CAMELCASE_SINGLE_WORD, has_valid_pattern


class LibraryType(str, Enum):
    SHADCNUI = "ui"
    UPLOADTHING = "uploadthing"


class ButtonVariant(str, Enum):
    DEFAULT = "default"
    SECONDARY = "secondary"
    DESTRUCTIVE = "destructive"
    OUTLINE = "outline"
    GHOST = "ghost"
    LINK = "link"


class ButtonSize(str, Enum):
    DEFAULT = "default"
    SM = "sm"
    LG = "lg"


class IconButtonSize(str, Enum):
    DEFAULT = "default"
    SM = "sm"
    LG = "lg"
    ICON = "icon"


class ButtonIconPosition(str, Enum):
    START = "start"
    END = "end"


class FormFieldLayout(IntEnum):
    DUO = 2
    TRIPLE = 3


class InputTypes(str, Enum):
    TEXT = "text"
    EMAIL = "email"
    PASSWORD = "password"
    NUMBER = "number"
    FILE = "file"
    TEL = "tel"
    SEARCH = "search"
    URL = "url"
    COLOR = "colour"


class InputOTPPatterns(str, Enum):
    REGEXP_ONLY_DIGITS = "digits_only"
    REGEXP_ONLY_CHARS = "chars_only"
    REGEXP_ONLY_DIGITS_AND_CHARS = "digits_n_chars_only"


class ScrollType(str, Enum):
    VERTICAL = "vertical"
    HORIZONTAL = "horizontal"


class ScrollAreaData(BaseModel):
    """
    A storage container for the `ScrollArea` data attribute.

    Parameters:
    - `name` (`string`) - the name of the `data` object. E.g., 'works'. Must be `lowercase` or `camelCase` and a maximum of `30` characters
    - `parameter` (`string`) - The map `parameter` name. E.g., 'artwork'. Must be `lowercase` or `camelCase` and a maximum of `30` characters
    - `data` (`list[dict[string, Any]]`) - A list of dictionaries containing information to pass into the `ScrollArea` component that is iterated over using a `map` function. Each dictionary must have the same key values and values of the same type
    """

    name: str = Field(min_length=1, max_length=30)
    parameter: str = Field(min_length=1, max_length=30)
    data: list[dict[str, Any]]

    @field_validator("data")
    def validate_data(cls, data: list[dict[str, Any]]) -> list[dict[str, Any]]:
        if len(data) == 0 or len(data[0]) == 0:
            raise PydanticCustomError(
                "missing_data",
                "No data exists in the list",
                dict(wrong_value=data),
            )

        reference_dict = data[0]
        for idx, d in enumerate(data[1:], start=1):
            if set(d.keys()) != set(reference_dict.keys()):
                raise PydanticCustomError(
                    "invalid_dictionary_keys",
                    f"position: 2.{idx} -> '{d.keys()} != {reference_dict.keys()}'\n",
                    dict(wrong_value=d, full_data=data),
                )

            for key, value in reference_dict.items():
                if type(d[key]) != type(value):
                    raise PydanticCustomError(
                        "invalid_value_type",
                        f"position: 2.{idx} -> '{type(d[key])} ({d[key]}) != {type(value)} ({value})'\n",
                        dict(wrong_value=d, full_data=data),
                    )

        return data

    @field_validator("name", "parameter")
    def validate_name_parameter(cls, v: str) -> str:
        result = has_valid_pattern(pattern=LOWER_CAMELCASE_SINGLE_WORD, value=v)

        if not result:
            raise PydanticCustomError(
                "string_pattern_mismatch",
                f"'{v}'. Must be 'lowercase' or 'camelCase', a single word and a maximum of '30' characters\n",
                dict(wrong_value=v, pattern=LOWER_CAMELCASE_SINGLE_WORD),
            )

        return v
