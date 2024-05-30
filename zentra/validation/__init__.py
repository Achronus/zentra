from pydantic_core import PydanticCustomError
from zentra.core import has_valid_pattern
from zentra.core.constants import VALID_ICON_NAMES
from zentra.core.utils import name_to_pascal_case


def check_kebab_case(name: str) -> str:
    """A helper validation function to check if a string is in kebab-case format."""
    if not has_valid_pattern(pattern=r"^[a-z]+(-[a-z]+)*$", value=name):
        raise PydanticCustomError(
            "invalid_name_format",
            f"'{name}' must be in kebab-case format",
            dict(wrong_value=name),
        )

    return name


def icon_name_validation(name: str) -> str:
    """A helper function for validating the icon name parameter for [Lucide React Icons](https://lucide.dev/icons). Raises an error if invalid. Otherwise, returns the name as PascalCase."""
    name = check_kebab_case(name)

    if name not in set(VALID_ICON_NAMES):
        url = f"https://lucide.dev/icons/{name}"
        raise PydanticCustomError(
            "invalid_icon",
            f"'{name}' at '{url}' does not exist",
            dict(wrong_value=name),
        )

    return name_to_pascal_case(name, char="-")
