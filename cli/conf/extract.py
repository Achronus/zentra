from itertools import chain
import os

from cli.conf.types import FolderFilePair


def get_dirnames(dirpath: str) -> list[str]:
    """Retrieves a list of directory names from a given directory path."""
    return [dir for dir in os.listdir(dirpath)]


def get_filename_dir_pairs(parent_dir: str, sub_dir: str = "") -> list[tuple[str, str]]:
    """Retrieves a list of all filenames in a parent directory and its sub-directory. Outputs them as a list of tuples with: `(parent_dir, filename)`.

    Example output:
    ```python
    ALL_BASE_FILES = get_filename_dir_pairs(parent_dir="components", sub_dir="base")
    -> [
        ("ui", "accordion.tsx"),
        ("ui", "button.tsx"),
        ...
        ("uploadthing", "core.ts"),
        ("uploadthing", "route.ts"),
        ...
       ]
    ```
    """
    all_files = []
    seen_files = set()

    for root, dirs, files in os.walk(parent_dir):
        if os.path.basename(root) == sub_dir:
            p_dir = os.path.basename(os.path.dirname(root))
        else:
            p_dir = os.path.basename(root)

        for file in files:
            file_tuple = (p_dir, file)

            if file_tuple not in seen_files:
                all_files.append(file_tuple)
                seen_files.add(file_tuple)

    return all_files


def extract_file_pairs_from_list(
    file_list: FolderFilePair, target_files: list[str], idx: int = 1
) -> FolderFilePair:
    """Retrieves a set of tuple pairs from a given file list based on a list of filenames.

    Parameters:
    - `file_list` (`FolderFilePair`) - a list of `(folder, filename)` pairs, where the folder name is the component library (e.g., 'ui' or 'uploadthing') and the filename is its react files (e.g., 'accordion.tsx')
    - `target_files` (`list[str]`) - a list of file or folder names to extract from the file list. Can be a single item.
    - `idx` (`int`, `optional`) - the tuple index to target. If `0` targets the folder name, and if `1` targets the filename. Defaults to `1`
    """
    filtered_list = []
    for item in file_list:
        if item[idx] in target_files:
            filtered_list.append(item)
    return filtered_list


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


def get_file_content_lines(filepath: str) -> list[str]:
    """Reads a file and returns its lines as a list of strings."""
    with open(filepath, "r") as f:
        return f.readlines()


def local_path(folder_path: str) -> str:
    """Extracts the last two directories from a `folder_path`."""
    head, tail = os.path.split(folder_path)
    root = os.path.basename(head)
    return "/".join([root, tail])
