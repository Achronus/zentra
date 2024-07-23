import shutil

from zentra_models.cli.constants.filepaths import LOCAL_PATHS, PACKAGE_PATHS

from zentra_models.cli.commands.base import status
from zentra_models.cli.commands.base.controller import BaseController

from zentra_models.cli.local.storage import ConfigExistStorage
from zentra_models.cli.local.files import make_directories


class SetupController(BaseController):
    """
    A controller for handling tasks for configuring Zentra.

    Parameters:
    - `config_exists` (`storage.ConfigExistStorage`) - a boolean value storage container for config checks
    """

    def __init__(
        self, config_exists: ConfigExistStorage, reset_config: bool = False
    ) -> None:
        self.config_exists = config_exists

        tasks = [
            (self.create_missing_files, "Creating [yellow]config[/yellow] files"),
            (self.create_demo_files, "Creating demo files"),
        ]

        if reset_config:
            tasks = [
                (self.reset_config, "Resetting [yellow]config[/yellow] file"),
            ]

        super().__init__(tasks)

    def _make_models_dir(self) -> None:
        """Creates the `zentra/models` directory if needed."""
        if not self.config_exists.models_folder_exists:
            make_directories(LOCAL_PATHS.MODELS)

    def _make_config_file(self) -> None:
        """Creates the setup file in `zentra/models` if it doesn't exist."""
        if not self.config_exists.config_file_exists:
            shutil.copy(
                PACKAGE_PATHS.CONF,
                LOCAL_PATHS.MODELS,
            )

    def _make_root_file(self) -> None:
        """Creates the `zentra.root` file in `zentra/models` if it doesn't exist."""
        if not self.config_exists.root_exists:
            open(LOCAL_PATHS.ZENTRA_ROOT, "x").close()

    @status
    def create_missing_files(self) -> None:
        """Creates the missing zentra files."""
        self._make_models_dir()
        self._make_config_file()
        self._make_root_file()

    @status
    def create_demo_files(self) -> None:
        """Creates a demo folder with files to demonstrate how to create Zentra Pages and Components."""
        shutil.copytree(
            PACKAGE_PATHS.DEMO,
            LOCAL_PATHS.DEMO,
            dirs_exist_ok=True,
        )

    @status
    def reset_config(self) -> None:
        """Forcefully recreates the config file."""
        shutil.copy(
            PACKAGE_PATHS.CONF,
            LOCAL_PATHS.MODELS,
        )
