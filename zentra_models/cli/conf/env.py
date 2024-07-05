import os
from pathlib import Path


def find_zentra_root(current_dir: Path = None) -> str:
    """
    Searches for the `zentra.root` file by traversing up the directory tree from the current directory.

    Returns the path found or an empty string.
    """
    if not current_dir:
        current_dir = os.getcwd()

    while True:
        potential_root = os.path.join(current_dir, "zentra.root")
        if os.path.isfile(potential_root):
            return os.path.split(potential_root)[0]

        # Traverse up parent directory
        parent_dir = os.path.dirname(current_dir)
        if parent_dir == current_dir:
            # Reached root directory without finding
            return ""

        current_dir = parent_dir


def __dotenv_setter(name: str, value: str) -> None:
    os.environ[name] = value


def set_zentra_root(name: str) -> None:
    """Sets the `zentra` root directory path as an environment variable."""
    __dotenv_setter("ZENTRA_ROOT", name)


def get_zentra_root() -> str:
    """Retrieves the `zentra` root directory path."""
    return os.environ.get("ZENTRA_ROOT")
