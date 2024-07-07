import os

from zentra_models.cli.constants.types import LibraryNamePairs


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
