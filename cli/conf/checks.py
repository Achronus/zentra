import os


def check_folder_exists(dirpath: str) -> bool:
    """Checks if a directory exists in the current working directory."""
    if os.path.exists(dirpath) and os.path.isdir(dirpath):
        return True

    return False
