import os

from zentra_models.cli.constants.types import LibraryNamePairs


def get_filename_dir_pairs(parent_dir: str, sub_dir: str = "") -> LibraryNamePairs:
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

    if os.path.exists(parent_dir):
        search_dirs = [folder for folder in os.listdir(parent_dir)]

        for folder in search_dirs:
            search_path = os.path.join(parent_dir, folder, sub_dir)
            for file in os.listdir(search_path):
                file_tuple = (folder, file)

                if file_tuple not in seen_files:
                    all_files.append(file_tuple)
                    seen_files.add(file_tuple)

    return all_files


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


def make_directories(dirpath: str) -> None:
    """Creates a set of directories, if they don't exist yet."""
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)


def make_file(filepath: str, content: str) -> None:
    """Creates a new file in a given filepath with the given content."""
    with open(filepath, "w") as f:
        f.write(content)


def remove_files(
    pairs: LibraryNamePairs, dirpath: str, ignore_pair_folder: bool = False
) -> None:
    """Removes a set of `(library_name, filename)` pairs from a directory."""
    for folder, filename in pairs:
        if not ignore_pair_folder:
            dirpath = os.path.join(dirpath, folder)

        filepath = os.path.join(dirpath, filename)
        os.remove(filepath)

        if len(os.listdir(dirpath)) == 0:
            os.removedirs(dirpath)
