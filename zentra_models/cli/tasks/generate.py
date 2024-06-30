import ast
import typer

from zentra_models.cli.conf.checks import (
    CheckConfigFileValid,
    check_file_exists,
    check_folder_exists,
    check_zentra_exists,
)

from zentra_models.cli.conf.constants import (
    CommonErrorCodes,
    GenerateErrorCodes,
    GenerateSuccessCodes,
    ZentraLocalFilepaths,
)
from zentra_models.cli.conf.extract import get_file_content, get_file_content_lines
from zentra_models.cli.tasks.controllers.generate import GenerateController
from zentra_models.cli.utils.printables import generate_complete_panel

from rich.console import Console

console = Console()


class Generate:
    """A class for handling the logic for the `zentra generate` command."""

    def __init__(self) -> None:
        self.local_paths = ZentraLocalFilepaths()

        self.config = self.local_paths.CONF

    def init_checks(self) -> None:
        """Performs various checks to immediately provide feedback to the user regarding missing files."""
        if not check_folder_exists(self.local_paths.MODELS):
            raise typer.Exit(code=CommonErrorCodes.MODELS_DIR_MISSING)

        if not check_file_exists(self.config):
            raise typer.Exit(code=CommonErrorCodes.CONFIG_MISSING)

        if len(get_file_content_lines(self.config)) == 0:
            raise typer.Exit(code=CommonErrorCodes.CONFIG_EMPTY)

    def check_config_valid(self) -> None:
        """Checks if the config file is valid. Raises an error if False."""
        check_config = CheckConfigFileValid()
        file_content_tree = ast.parse(get_file_content(self.config))
        check_config.visit(file_content_tree)

        valid_content = check_config.is_valid()

        if not valid_content:
            raise typer.Exit(code=CommonErrorCodes.INVALID_CONFIG)

    def create_components(self) -> None:
        """Generates the react components based on the `zentra/models` folder."""
        self.check_config_valid()
        zentra = check_zentra_exists(self.local_paths.MODELS)

        if not zentra:
            raise typer.Exit(CommonErrorCodes.MODELS_DIR_MISSING)

        if len(zentra.name_storage.components) == 0:
            raise typer.Exit(code=GenerateErrorCodes.NO_COMPONENTS)

        console.print()
        controller = GenerateController(zentra)
        controller.run()

        console.print(generate_complete_panel(controller.storage))
        raise typer.Exit(GenerateSuccessCodes.COMPLETE)
