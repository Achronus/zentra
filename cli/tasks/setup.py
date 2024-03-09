import ast
import os

import typer
from cli.conf.checks import (
    CheckConfigFileValid,
    check_file_exists,
    check_models_registered,
)

from cli.conf.checks import check_folder_exists
from cli.conf.extract import get_file_content
from cli.conf.storage import ConfigExistStorage, PathStorage
from cli.utils.printables import configuration_complete_panel
from .controllers.setup import SetupController
from cli.conf.constants import GETTING_STARTED_URL, SetupSuccessCodes, ZentaFilepaths
from zentra.core import Zentra

from rich.console import Console


console = Console()


class Setup:
    """
    A class for handling the `zentra init` command.

    Parameters:
    - zentra (zentra.core.Zentra) - the Zentra application containing components to generate
    """

    def __init__(self, zentra: Zentra) -> None:
        self.zentra = zentra
        self.paths = PathStorage(
            config=os.path.join(ZentaFilepaths.MODELS, ZentaFilepaths.SETUP_FILENAME),
            models=ZentaFilepaths.MODELS,
        )

        self.config_storage = ConfigExistStorage()

    def init_app(self) -> None:
        """Performs configuration to initialise application with Zentra."""
        # Check app setup
        self.check_config()

        if self.config_storage.app_configured():
            raise typer.Exit(code=SetupSuccessCodes.CONFIGURED)

        # Create missing items
        controller = SetupController(paths=self.paths, config=self.config_storage)
        controller.run()

        # Setup complete
        console.print(
            configuration_complete_panel(self.paths.models, link=GETTING_STARTED_URL)
        )

    def check_config(self) -> None:
        """Checks if the config files are already setup."""
        # Check models file exists
        if check_folder_exists(self.paths.models):
            self.config_storage.set_true("models_folder_exists")

        # Check config file exists
        if check_file_exists(self.paths.config):
            self.config_storage.set_true("config_file_exists")

        # Check config file content is valid
        check_config = CheckConfigFileValid()
        file_content_tree = ast.parse(get_file_content(self.paths.config))
        check_config.visit(file_content_tree)

        self.config_storage.set_true("config_file_valid")

        # Checks models are registered
        if check_models_registered(self.zentra):
            self.config_storage.set_true("models_registered")
