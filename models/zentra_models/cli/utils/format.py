from enum import Enum
import re


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


def jsx_formatter(code: str, indent_size: int = 2, use_tabs: bool = False):
    "A simple JSX formatter for iterative over lines of code separated by new line (`\\n`) characters."
    indent_char = "\t" if use_tabs else " " * indent_size
    lines = code.split("\n")
    formatted_lines = []
    indent_level = 0

    for line in lines:
        stripped_line = line.strip()

        if not stripped_line:
            formatted_lines.append("")
            continue

        # Adjust indentation based on opening/closing tags
        if stripped_line.startswith("</") or stripped_line.startswith("/>"):
            indent_level -= 1

        formatted_lines.append(f"{indent_char * indent_level}{stripped_line}")

        if (
            stripped_line.startswith("<")
            and not stripped_line.startswith("</")
            and not stripped_line.endswith("/>")
        ):
            indent_level += 1

    return "\n".join(formatted_lines)
