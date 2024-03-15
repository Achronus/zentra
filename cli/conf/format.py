import re


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


def name_to_plural(name: str, count: int) -> str:
    """Converts a name to a plural version if the count is greater than 1."""
    return name if count == 1 else f"{name}s"
