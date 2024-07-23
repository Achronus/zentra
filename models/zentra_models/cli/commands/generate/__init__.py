import typer

from zentra_models.cli.conf.checks import (
    check_file_exists,
    check_folder_exists,
    check_zentra_exists,
)

from zentra_models.cli.constants import CommonErrorCodes, GenerateSuccessCodes
from zentra_models.cli.constants.filepaths import LOCAL_PATHS
from zentra_models.cli.local.files import get_file_content_lines

from zentra_models.cli.commands.generate.generate import GenerateController
from zentra_models.cli.display.printables import generate_complete_panel

from rich.console import Console

console = Console()


class Generate:
    """A class for handling the logic for the `zentra generate` command."""

    def __init__(self) -> None:
        self.local_paths = LOCAL_PATHS
        self.config = self.local_paths.CONF

    def init_checks(self) -> None:
        """Performs various checks to immediately provide feedback to the user regarding missing files."""
        zentra = check_zentra_exists(self.config)

        if not check_folder_exists(self.local_paths.MODELS):
            raise typer.Exit(code=CommonErrorCodes.MODELS_DIR_MISSING)

        if not check_file_exists(self.config):
            raise typer.Exit(code=CommonErrorCodes.CONFIG_MISSING)

        if len(get_file_content_lines(self.config)) == 0:
            raise typer.Exit(code=CommonErrorCodes.CONFIG_EMPTY)

        if not zentra:
            raise typer.Exit(code=CommonErrorCodes.ZENTRA_MISSING)

    def create_components(self) -> None:
        """Generates the react components based on the `zentra/models` folder."""
        zentra = check_zentra_exists(self.config)

        if not zentra:
            raise typer.Exit(CommonErrorCodes.MODELS_DIR_MISSING)

        if zentra.storage.count("components") == 0:
            raise typer.Exit(code=CommonErrorCodes.NO_COMPONENTS)

        console.print()
        controller = GenerateController(zentra)
        controller.run()

        console.print(generate_complete_panel(controller.counts))
        raise typer.Exit(GenerateSuccessCodes.COMPLETE)
