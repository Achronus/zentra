import os
from cli.conf.move import copy_dir_files, copy_file
from cli.conf.storage import ConfigExistStorage, SetupPathStorage
from cli.tasks.controllers.base import BaseController, status
from cli.conf.create import make_directories
from cli.conf.extract import local_path


class SetupController(BaseController):
    """
    A controller for handling tasks for configuring Zentra.

    Parameters:
    - paths (storage.SetupPathStorage) - a path storage container with filepaths specific to the controller
    - config_storage (storage.ConfigExistStorage) - a boolean value storage container for config checks
    """

    def __init__(
        self, paths: SetupPathStorage, config_storage: ConfigExistStorage
    ) -> None:
        self.paths = paths
        self.config_storage = config_storage

        demo_folder_str = (
            f"{local_path(self.paths.models)}/{os.path.basename(self.paths.demo)}"
        )
        highlighted_path = f"[magenta]{demo_folder_str}[/magenta]"

        tasks = [
            (
                self.create_missing_files,
                "Creating [yellow]configuration[/yellow] files",
            ),
            (
                self.create_demo_files,
                f"Creating demo files in {highlighted_path}",
            ),
        ]

        super().__init__(tasks)

    def _make_models_dir(self) -> None:
        """Creates the `zentra/models` directory if needed."""
        if not self.config_storage.models_folder_exists:
            make_directories(self.paths.models)

    def _make_config_file(self) -> None:
        """Moves the config file from `zentra_config` to `zentra/models` if doesn't exist."""
        if not self.config_storage.config_file_exists:
            copy_file(self.paths.local_config, self.paths.models)

    @status
    def create_missing_files(self) -> None:
        """Creates the missing zentra files."""
        self._make_models_dir()
        self._make_config_file()

    @status
    def create_demo_files(self) -> None:
        """Creates a demo folder with files to demonstrate how to create Zentra Pages and Components."""
        copy_dir_files(self.paths.demo, self.paths.models)
