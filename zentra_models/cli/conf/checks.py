import ast
import importlib
import os

import typer
from zentra_models.cli.conf.constants import SetupErrorCodes

from zentra_models.core import Zentra
from zentra_models.cli.conf.logger import zentra_missing_logger


def check_zentra_exists() -> Zentra:
    """Checks if the `Zentra` app has been created by the user."""
    try:
        zentra_module = importlib.import_module("zentra.models.models")
    except ModuleNotFoundError as e:
        zentra_missing_logger.error(e)
        raise typer.Exit(SetupErrorCodes.IMPORT_ERROR)

    if hasattr(zentra_module, "zentra"):
        return zentra_module.zentra


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


def check_models_registered(zentra: Zentra) -> bool:
    """Checks if any models are registered to the `Zentra` app."""
    if len(zentra.models.name_storage.components) > 0:
        return True

    return False


class CheckConfigFileValid(ast.NodeVisitor):
    """
    A utility class for handling the checks to identify if the `zentra/models` config file is valid.

    Checks for the following conditions:
    1. Zentra is imported correctly
    2. Zentra app is initalised
    3. `zentra.models.register()` exists
    """

    def __init__(self) -> None:
        self.zentra_init_exists = False
        self.zentra_register_exists = False
        self.zentra_imported = False

        self.assign_target = "zentra"
        self.register_method = "register"
        self.module_name = "zentra.models.core"
        self.import_name = "Zentra"

    def visit_Assign(self, node: ast.Assign):
        """Visits all `ast.Assign` nodes and checks if `zentra = Zentra()` is present."""
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == self.assign_target:
                self.zentra_init_exists = True

    def visit_Call(self, node: ast.Call):
        """Visits all `ast.Call` nodes and validates `zentra.models.register()`."""
        if hasattr(node.func, "attr") and node.func.attr == self.register_method:
            self.zentra_register_exists = True

    def visit_ImportFrom(self, node: ast.ImportFrom):
        """Checks if `from zentra.models.core import Zentra` is present."""
        if node.module == self.module_name:
            for alias in node.names:
                if alias.name == self.import_name:
                    self.zentra_imported = True

    def is_valid(self) -> bool:
        """Accesses the stored checks attributes and checks they are all True. Returns True is valid, else False."""
        checks = [
            self.zentra_init_exists,
            self.zentra_register_exists,
            self.zentra_imported,
        ]
        return all(checks)
