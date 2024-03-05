import re


def name_from_camel_case(name: str) -> str:
    """
    Converts a name from camel case to a lowercase dashed format.

    Example:
    - AspectRatio -> aspect-ratio
    """
    converted_name = re.sub("([a-z0-9])([A-Z])", r"\1-\2", name)
    return converted_name.lower()
