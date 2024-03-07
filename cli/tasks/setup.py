import typer

from cli.conf.checks import check_folder_exists
from cli.tasks.controllers import run_tasks
from cli.utils.printables import path_exists_table, configuration_complete_panel
from .controllers.path import FolderDoesNotExistController
from cli.conf.constants import ZentaFilepaths, StatusCode, PARTY, DOCS_URL

from rich.console import Console


console = Console()
root_path_msg = "Configuring [magenta]Zentra[/magenta] project..."

PATH_NOT_EXIST_TASKS = [
    (FolderDoesNotExistController, root_path_msg),
]


class Setup:
    """A class for handling the `zentra init` command."""

    def __init__(self) -> None:
        self.folder_path = ZentaFilepaths.MODELS

        self.path_exists = check_folder_exists(self.folder_path)

    def init_app(self) -> None:
        """Performs configuration to initialise application with Zentra."""
        console.print(path_exists_table(self.folder_path, self.path_exists))

        if self.path_exists:
            console.print(
                f"\n{PARTY} Application already configured with components! Use [green]zentra generate[/green] to create them! {PARTY}\n"
            )
            typer.Exit(code=StatusCode.CONFIGURED)

        else:
            run_tasks(PATH_NOT_EXIST_TASKS)

            console.print()
            console.print(configuration_complete_panel(self.folder_path, link=DOCS_URL))
            console.print()
