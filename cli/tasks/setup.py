import typer

from cli.conf.checks import check_folder_exists
from cli.utils.printables import path_exists_table, configuration_complete_panel
from .controllers.setup import SetupController
from cli.conf.constants import ZentaFilepaths, SetupSuccessCodes, DOCS_URL

from rich.console import Console


console = Console()


class Setup:
    """A class for handling the `zentra init` command."""

    def __init__(self) -> None:
        self.folder_path = ZentaFilepaths.MODELS
        self.path_exists = check_folder_exists(self.folder_path)

    def init_app(self) -> None:
        """Performs configuration to initialise application with Zentra."""
        console.print()
        console.print(path_exists_table(self.folder_path, self.path_exists))

        if self.path_exists:
            raise typer.Exit(code=SetupSuccessCodes.CONFIGURED)

        controller = SetupController()
        controller.run()

        console.print()
        console.print(configuration_complete_panel(self.folder_path, link=DOCS_URL))
        console.print()
