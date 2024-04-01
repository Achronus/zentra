import ast
import os

import typer

from cli.conf.checks import (
    CheckConfigFileValid,
    check_file_exists,
    check_folder_exists,
    check_zentra_exists,
)
from cli.conf.extract import get_file_content
from cli.conf.storage import ConfigExistStorage, SetupPathStorage
from cli.utils.printables import setup_complete_panel, setup_first_run_panel
from .controllers.setup import SetupController
from cli.conf.constants import (
    GITHUB_INIT_ASSETS_DIR,
    CommonErrorCodes,
    SetupErrorCodes,
    SetupSuccessCodes,
    ZentaFilepaths,
)

from rich.console import Console


console = Console()


class Setup:
    """A class for handling the `zentra init` command."""

    def __init__(self) -> None:
        self.paths = SetupPathStorage(
            config=os.path.join(ZentaFilepaths.MODELS, ZentaFilepaths.SETUP_FILENAME),
            models=ZentaFilepaths.MODELS,
            demo=ZentaFilepaths.DEMO,
        )

        self.config_exists = ConfigExistStorage()

    def init_app(self) -> None:
        """Performs configuration to initialise application with Zentra."""
        self.check_config()

        if self.config_exists.app_configured():
            zentra = check_zentra_exists()
            if len(zentra.name_storage.components) == 0:
                raise typer.Exit(code=SetupErrorCodes.NO_COMPONENTS)
            else:
                console.print(setup_complete_panel())
                raise typer.Exit(code=SetupSuccessCodes.ALREADY_CONFIGURED)

        # Create config files
        console.print()
        controller = SetupController(
            url=GITHUB_INIT_ASSETS_DIR,
            paths=self.paths,
            config_exists=self.config_exists,
        )
        controller.run()

        zentra = check_zentra_exists()
        if len(zentra.name_storage.components) == 0:
            console.print(setup_first_run_panel())
            raise typer.Exit(code=SetupSuccessCodes.COMPLETE)

    def check_config(self) -> None:
        """Checks if the config files are already setup."""
        # Check models file exists
        if check_folder_exists(self.paths.models):
            self.config_exists.models_folder_exists = True

        # Check config file exists
        if check_file_exists(self.paths.config):
            self.config_exists.config_file_exists = True

            # Check config file content is valid
            check_config = CheckConfigFileValid()
            file_content_tree = ast.parse(get_file_content(self.paths.config))
            check_config.visit(file_content_tree)

            if check_config.is_valid():
                self.config_exists.config_file_valid = True
            else:
                raise typer.Exit(code=CommonErrorCodes.INVALID_CONFIG)
