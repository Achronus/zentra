import os

from cli.conf.constants import ZentaFilepaths
from zentra.core import Zentra


def check_file_exists(filepath: str) -> bool:
    """Checks if a file exists based on the given filepath."""
    if os.path.exists(filepath) and os.path.isfile(filepath):
        return True

    return False


def check_folder_exists(dirpath: str) -> bool:
    """Checks if a directory exists based on the given directory path."""
    if os.path.exists(dirpath) and os.path.isdir(dirpath):
        return True

    return False


def check_in_correct_folder() -> bool:
    """Checks if the user is in the correct folder before using the tool."""
    return check_folder_exists(ZentaFilepaths.ROOT)


def check_zentra_models_exist() -> bool:
    """Checks if the `zentra/models` folder exists."""
    return check_folder_exists(ZentaFilepaths.MODELS)


def check_models_registered(zentra: Zentra) -> bool:
    """Checks if any models are registered to the `Zentra` app."""
    if len(zentra.component_names) > 0:
        return True

    return False
