import re

from cli.conf.types import FolderFilePair


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


def format_item_list(items: FolderFilePair) -> list[str]:
    """Formats model filenames into camel case."""
    return [(folder, name_to_camel_case(file)) for folder, file in items]


def to_cc_from_pairs(pairs: FolderFilePair) -> list[str]:
    """Converts a set of Zentra model filename pairs back into their basenames."""
    result = []
    formatted_pairs = format_item_list(pairs)

    for folder, file in formatted_pairs:
        if folder == "uploadthing":
            result.append("FileUpload")
        else:
            result.append(file)

    result = list(set(result))
    result.sort()
    return result
