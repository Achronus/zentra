from pathlib import Path
from dotenv import load_dotenv
import os


def finder(target: str) -> Path:
    """
    Searches for the `target` file by traversing up the directory tree from the current directory.

    Returns the path found or an empty string.
    """
    current_dir = Path(os.getcwd())

    while True:
        potential_root = Path(current_dir, target)
        if os.path.isfile(potential_root):
            return potential_root

        # Traverse up parent directory
        parent_dir = Path(os.path.dirname(current_dir))
        if parent_dir == current_dir:
            # Reached root directory without finding
            raise FileNotFoundError(f"'{target}' file missing from project directory!")

        current_dir = parent_dir


def load_dotenv_file(filename: str) -> None:
    """Loads a dotenv file."""
    path = finder(filename)
    load_dotenv(path)
