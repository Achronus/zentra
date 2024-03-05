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
    types_list = []

    for key, value in page_schema.items():
        if key == "type":
            types_list.append(value)
        elif isinstance(value, dict):
            types_list.extend(extract_component_names(value))
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    types_list.extend(extract_component_names(item))

    return types_list
