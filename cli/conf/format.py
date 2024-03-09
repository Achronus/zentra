import re

from zentra.core import Zentra


def name_from_camel_case(name: str) -> str:
    """
    Converts a name from camel case to a lowercase dashed format.

    Example:
    - AspectRatio -> aspect-ratio
    """
    converted_name = re.sub("([a-z0-9])([A-Z])", r"\1-\2", name)
    return converted_name.lower()


def set_colour(text: str, colour: str) -> str:
    """A helper function for colouring text."""
    return f"[{colour}]{text}[/{colour}]"


def component_count_str(zentra: Zentra) -> str:
    """Returns a string with the count of the number of Zentra pages and components to create."""
    page_count = len(zentra.pages)
    component_count = len(zentra.component_names)

    page_name = set_colour(
        plural_name_formatter("Page", page_count),
        "yellow",
    )
    component_name = set_colour(
        plural_name_formatter("Component", component_count),
        "yellow",
    )

    page_count = set_colour(page_count, "green")
    component_count = set_colour(component_count, "green")

    return f"{page_count} {page_name} and {component_count} {component_name}"


def plural_name_formatter(name: str, count: int) -> str:
    """Converts a name to a plural version if the count is greater than 1."""
    return name if count == 1 else f"{name}s"
