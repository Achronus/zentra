import os


def check_folder_exists(dirpath: str) -> bool:
    """Checks if a directory exists in the current working directory."""
    if os.path.exists(dirpath) and os.path.isdir(dirpath):
        return True

    return False


def check_in_correct_folder() -> bool:
    """Checks if the user is in the correct folder before using the tool."""
    current_directory = os.getcwd()
    zentra_folder_path = os.path.join(current_directory, "zentra")

    if os.path.exists(zentra_folder_path) and os.path.isdir(zentra_folder_path):
        return True

    return False
