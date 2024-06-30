import shutil

from zentra_models.cli.conf.storage import ConfigExistStorage
from zentra_models.cli.tasks.controllers.base import BaseController, status
from zentra_models.cli.conf.create import make_directories


class SetupController(BaseController):
    """
    A controller for handling tasks for configuring Zentra.

    Parameters:
    - `config_exists` (`storage.ConfigExistStorage`) - a boolean value storage container for config checks
    """

    def __init__(self, config_exists: ConfigExistStorage) -> None:
        self.config_exists = config_exists

        tasks = [
            (
                self.create_missing_files,
                "Creating [yellow]config[/yellow] files",
            ),
            (
                self.create_demo_files,
                "Creating demo files",
            ),
        ]

        super().__init__(tasks)

    def _make_models_dir(self) -> None:
        """Creates the `zentra/models` directory if needed."""
        if not self.config_exists.models_folder_exists:
            make_directories(self.local_paths.MODELS)

    def _make_config_file(self) -> None:
        """Creates the setup file in `zentra/models` if it doesn't exist."""
        if not self.config_exists.config_file_exists:
            shutil.copy(
                self.package_paths.CONF,
                self.local_paths.MODELS,
            )

    @status
    def create_missing_files(self) -> None:
        """Creates the missing zentra files."""
        self._make_models_dir()
        self._make_config_file()

    @status
    def create_demo_files(self) -> None:
        """Creates a demo folder with files to demonstrate how to create Zentra Pages and Components."""
        shutil.copytree(
            self.package_paths.DEMO,
            self.local_paths.DEMO,
            dirs_exist_ok=True,
        )
