import re


def name_to_pascal_case(name: str) -> str:
    """
    Converts a name from lowercase underscored format to pascal case.

    Example:
    - dropdown_menu -> DropdownMenu
    """
    components = name.split("_")
    return "".join(item.title() for item in components)


def name_from_pascal_case(name: str) -> str:
    """
    Converts a name from pascal case to a lowercase dashed format.

    Example:
    - AspectRatio -> aspect-ratio
    """
    converted_name = re.sub("([a-z0-9])([A-Z])", r"\1-\2", name)
    return converted_name.lower()
