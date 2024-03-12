import os

import typer
from cli.conf.constants import (
    CommonErrorCodes,
    GenerateErrorCodes,
)
from cli.conf.format import name_from_camel_case
from cli.conf.move import copy_list_of_files
from cli.conf.storage import ModelStorage, PathStorage
from cli.tasks.controllers.base import BaseController, status

from zentra.core import Zentra


class GenerateController(BaseController):
    """
    A controller for handling tasks that generate the Zentra components.

    Parameters:
    - zentra (zentra.core.Zentra) - the Zentra application containing components to generate
    - paths (storage.PathStorage) - a path storage container with filepaths specific to the controller
    """

    def __init__(self, zentra: Zentra, paths: PathStorage) -> None:
        react_str = "[cyan]React[/cyan]"
        zentra_str = "[magenta]Zentra[/magenta]"

        tasks = [
            (self.extract_models, f"Retrieving {zentra_str} models"),
            (self.create_files, f"Creating {react_str} component files"),
            (self.update_template_files, f"Configuring {react_str} components"),
        ]

        super().__init__(tasks)

        self.storage = ModelStorage()
        self.paths = paths
        self.zentra = zentra

    @status
    def extract_models(self) -> None:
        """Extracts the Zentra models and prepares them for file generation."""
        formatted_names = [
            f"{name_from_camel_case(name)}.tsx" for name in self.zentra.component_names
        ]

        self.storage.UT_TO_GENERATE = list(
            set(formatted_names) - set(self.storage.UI_BASE)
        )

        self.storage.UI_TO_GENERATE = list(
            set(formatted_names) - set(self.storage.UT_TO_GENERATE)
        )

    def _make_needed_dirs(self) -> None:
        """Makes the needed directories in the `zentra` folder."""
        os.makedirs(self.paths.generated_ui_base, exist_ok=True)

    def _copy_base_ui(self) -> None:
        """Copies a list of `zentra/model` files from one location to another."""
        copy_list_of_files(
            self.paths.local_ui_base,
            self.paths.generated_ui_base,
            CommonErrorCodes.SRC_DIR_MISSING,
            GenerateErrorCodes.GENERATE_DIR_MISSING,
            self.storage.UI_TO_GENERATE,
        )

    @status
    def create_files(self) -> None:
        """Creates the React components based on the extracting models."""
        self._make_needed_dirs()
        self._copy_base_ui()

    @status
    def update_template_files(self) -> None:
        """Updates the React components based on the Zentra model attributes."""
        pass
        # Steps 6 to 8
