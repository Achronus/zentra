import ast
import os

import typer

from zentra_models.cli.conf.checks import (
    CheckConfigFileValid,
    check_file_exists,
    check_folder_exists,
    check_zentra_exists,
)
from zentra_models.cli.conf.extract import get_file_content, local_path
from zentra_models.cli.conf.storage import ConfigExistStorage
from zentra_models.cli.utils.printables import (
    setup_complete_panel,
    setup_first_run_panel,
)
from .controllers.setup import SetupController
from zentra_models.cli.conf.constants import (
    LOCAL_PATHS,
    CommonErrorCodes,
    SetupErrorCodes,
    SetupSuccessCodes,
)

from rich.console import Console


console = Console()


def confirm_project_init() -> None:
    """Handles the input for confirming project initialisation. Terminates if `N` provided."""
    zentra_name = typer.style("Zentra", typer.colors.MAGENTA)
    root, dir = local_path(os.getcwd()).split("/")

    dir_name = typer.style(dir, typer.colors.MAGENTA)
    root_name = typer.style(root, typer.colors.YELLOW)
    full_path = typer.style(os.getcwd(), typer.colors.YELLOW)
    result = typer.confirm(
        f"Make {dir_name} directory in {root_name} ({full_path}) a {zentra_name} project?"
    )

    if not result:
        raise typer.Abort()


class Setup:
    """A class for handling the `zentra init` command."""

    def __init__(self) -> None:
        self.config_exists = ConfigExistStorage()

    def init_app(self, force: bool, reset_config: bool) -> None:
        """Performs configuration to initialise application with Zentra."""
        self.check_config()

        if not force and not self.config_exists.app_configured():
            confirm_project_init()

        zentra = check_zentra_exists(LOCAL_PATHS.MODELS)

        # Already exists
        if (zentra and self.config_exists.app_configured()) and not reset_config:
            if len(zentra.name_storage.components) == 0:
                raise typer.Exit(code=SetupErrorCodes.NO_COMPONENTS)

            console.print(setup_complete_panel(zentra))
            raise typer.Exit(code=SetupSuccessCodes.ALREADY_CONFIGURED)

        # Otherwise, create config files
        console.print()
        controller = SetupController(
            self.config_exists,
            reset_config=reset_config,
        )
        controller.run()

        console.print(setup_first_run_panel())
        raise typer.Exit(code=SetupSuccessCodes.COMPLETE)

    def check_config(self) -> None:
        """Checks if the config files are already setup."""
        # Check models directory exists
        if check_folder_exists(LOCAL_PATHS.MODELS):
            self.config_exists.models_folder_exists = True

        # Check config file exists
        if check_file_exists(LOCAL_PATHS.CONF):
            self.config_exists.config_file_exists = True

            # Check config file content is valid
            check_config = CheckConfigFileValid()
            file_content_tree = ast.parse(get_file_content(LOCAL_PATHS.CONF))
            check_config.visit(file_content_tree)

            if check_config.is_valid():
                self.config_exists.config_file_valid = True
            else:
                raise typer.Exit(code=CommonErrorCodes.INVALID_CONFIG)

        # Check root file exists
        if check_file_exists(LOCAL_PATHS.ZENTRA_ROOT):
            self.config_exists.root_exists = True
