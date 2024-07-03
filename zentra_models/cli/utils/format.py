from enum import Enum
import re

from zentra_models.cli.constants.types import LibraryNamePairs


def name_from_camel_case(name: str) -> str:
    """
    Converts a name from camel case to a lowercase dashed format.

    Example:
    - AspectRatio -> aspect-ratio
    """
    converted_name = re.sub("([a-z0-9])([A-Z])", r"\1-\2", name)
    return converted_name.lower()


def name_to_camel_case(name: str) -> str:
    """
    Converts a name from the lowercase dashed format to camel case.

    Example:
    - aspect-ratio.tsx -> AspectRatio
    """
    components = name.split(".")[0].split("-")
    camel_case_name = components[0].title() + "".join(x.title() for x in components[1:])
    return camel_case_name


def set_colour(text: str, colour: str) -> str:
    """A helper function for colouring text."""
    return f"[{colour}]{text}[/{colour}]"


def name_to_plural(name: str, count: int) -> str:
    """Converts a name to a plural version if the count is greater than 1."""
    return name if count == 1 else f"{name}s"


def format_item_list(items: LibraryNamePairs) -> list[str]:
    """Formats model filenames into camel case."""
    return [(folder, name_to_camel_case(file)) for folder, file in items]


def to_cc_from_pairs(pairs: LibraryNamePairs) -> list[str]:
    """Converts a set of Zentra model filename pairs back into their basenames."""
    result = []
    formatted_pairs = format_item_list(pairs)

    for _, file in formatted_pairs:
        result.append(file)

    result = list(set(result))
    result.sort()
    return result


def list_to_str(items: list[str], action: Enum, items_per_line: int = 4) -> str:
    """Converts a list of `items` into a single readable string separated by commas. Items are passed onto new lines when `items_per_line` is reached."""
    symbol, colour = action.value
    symbol = set_colour(symbol, colour)
    combined_string = f"  {symbol} "
    items.sort()

    if len(items) > 0:
        # Split items equally across lines up to desired value
        num_lines = -(-len(items) // items_per_line)
        items_per_line = -(-len(items) // num_lines)

        for i, item in enumerate(items):
            end_str = (i + 1) == len(items)
            start_newline = (i + 1) % items_per_line == 0 and len(items) != 1
            combined_string += item
            combined_string += (
                f"\n  {symbol} " if start_newline and not end_str else ", "
            )

        return combined_string.rstrip(", ")
    return ""
