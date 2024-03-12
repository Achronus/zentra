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
from cli.conf.storage import (
    ConfigExistStorage,
    CorePaths,
    LocalZentraConfigPaths,
    SetupPathStorage,
)
from .controllers.setup import SetupController
from cli.conf.constants import (
    CommonErrorCodes,
    SetupErrorCodes,
    SetupSuccessCodes,
    ZentaFilepaths,
    ZentraConfigFilepaths,
)

from rich.console import Console


console = Console()


class Setup:
    """A class for handling the `zentra init` command."""

    def __init__(self) -> None:
        self.paths = SetupPathStorage(
            core=CorePaths(
                config=os.path.join(
                    ZentaFilepaths.MODELS, ZentaFilepaths.SETUP_FILENAME
                ),
                models=ZentaFilepaths.MODELS,
                demo=ZentaFilepaths.DEMO_FOLDER,
            ),
            local=LocalZentraConfigPaths(
                zentra=ZentraConfigFilepaths.ROOT, demo=ZentraConfigFilepaths.DEMO
            ),
        )

        self.config_storage = ConfigExistStorage()

    def init_app(self) -> None:
        """Performs configuration to initialise application with Zentra."""
        self.check_config()

        if self.config_storage.app_configured():
            zentra = check_zentra_exists()

            if len(zentra.component_names) == 0:
                raise typer.Exit(code=SetupErrorCodes.NO_COMPONENTS)
            else:
                raise typer.Exit(code=SetupSuccessCodes.ALREADY_CONFIGURED)

        # Create config files
        console.print()
        controller = SetupController(self.paths, self.config_storage)
        controller.run()

        # Setup complete
        raise typer.Exit(code=SetupSuccessCodes.COMPLETE)

    def check_config(self) -> None:
        """Checks if the config files are already setup."""
        # Check models file exists
        if check_folder_exists(self.paths.core.models):
            self.config_storage.models_folder_exists = True

        # Check config file exists
        if check_file_exists(self.paths.core.config):
            self.config_storage.config_file_exists = True

            # Check config file content is valid
            check_config = CheckConfigFileValid()
            file_content_tree = ast.parse(get_file_content(self.paths.core.config))
            check_config.visit(file_content_tree)

            if check_config.is_valid():
                self.config_storage.config_file_valid = True
            else:
                raise typer.Exit(code=CommonErrorCodes.INVALID_CONFIG)
