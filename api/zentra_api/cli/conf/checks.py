import os
from pathlib import Path

from pydantic import validate_call


@validate_call(validate_return=True)
def zentra_root_path() -> Path | None:
    """
    Searches for the `zentra.root` file by traversing up the directory tree from the current directory.

    If found, returns its `Path`. Otherwise, `None`.
    """
    current_dir = Path(os.getcwd())

    while True:
        potential_root = Path(current_dir, "zentra.root")
        if potential_root.is_file():
            return potential_root

        # Traverse up parent directory
        parent_dir = Path(os.path.dirname(current_dir))
        if parent_dir == current_dir:
            # Reached root directory without finding
            return None

        print(parent_dir)
        current_dir = parent_dir


@validate_call(validate_return=True)
def check_file_exists(filepath: Path) -> bool:
    """Checks if a file exists based on the given filepath."""
    if os.path.exists(filepath) and os.path.isfile(filepath):
        return True

    return False


@validate_call(validate_return=True)
def check_folder_exists(dirpath: Path) -> bool:
    """Checks if a directory exists based on the given directory path."""
    if os.path.exists(dirpath) and os.path.isdir(dirpath):
        return True

    return False
