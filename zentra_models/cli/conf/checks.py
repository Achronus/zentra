import importlib
import os

import typer
from zentra_models.cli.constants import SetupErrorCodes

from zentra_models.cli.local.extractor import ZentraExtractor
from zentra_models.core import Zentra
from zentra_models.cli.conf.logger import zentra_missing_logger


def check_zentra_exists(path: str) -> Zentra | None:
    """Checks if the `Zentra` app has been created by the user."""
    if not os.path.exists(path):
        return None

    try:
        extractor = ZentraExtractor(path)
        name = extractor.zentra.targets[0].id

        module = importlib.import_module("zentra.models")
        zentra: Zentra = getattr(module, name)
        return zentra

    except (AttributeError, ModuleNotFoundError) as e:
        zentra_missing_logger.error(e)
        raise typer.Exit(SetupErrorCodes.IMPORT_ERROR)


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
