import re


def name_to_pascal_case(name: str, char: str = "_") -> str:
    """
    Converts a name to pascal case based on a given `name` and `character` to split the name on.

    Example:
    - dropdown_menu -> DropdownMenu
    """
    components = name.split(char)
    return "".join(item.title() for item in components)


def name_from_pascal_case(name: str) -> str:
    """
    Converts a name from pascal case to a lowercase dashed format.

    Example:
    - AspectRatio -> aspect-ratio
    """
    converted_name = re.sub("([a-z0-9])([A-Z])", r"\1-\2", name)
    return converted_name.lower()


def compress(values: list[str], chars: str = "\n") -> str:
    """Compresses values into a string."""
    return chars.join(values)


def str_to_list(content: str, sep: str = "\n") -> list[str]:
    """Converts a string into a list of strings based on a given separator."""
    return content.split(sep=sep)
