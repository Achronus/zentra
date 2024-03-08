from itertools import chain
import os


def get_filenames_in_subdir(filepath: str) -> list[str]:
    """Retrieves a list of all filenames in a `filepath`. Ignores folder subdirectories."""
    filenames = []
    for root, dirs, files in os.walk(filepath):
        for file in files:
            filenames.append(file)
    return filenames


def extract_component_names(page_schema: dict[str, str]) -> list[str]:
    """Recursively extracts the `Component` names from a `Page` schema."""
    component_type = [page_schema.get("type")]

    nested_types = [
        extract_component_names(item)
        for value in page_schema.values()
        if isinstance(value, list)
        for item in value
        if isinstance(item, dict)
    ]

    # Compress to single list
    flattened_types = list(chain.from_iterable(nested_types))

    return component_type + flattened_types


def get_file_content(filepath: str) -> str:
    """Reads a file and returns it as a string."""
    with open(filepath, "r") as f:
        return f.read()
