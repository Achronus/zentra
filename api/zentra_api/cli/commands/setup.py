import typer

from rich.console import Console
from rich.progress import track

from zentra_api.cli.constants import SetupSuccessCodes
from zentra_api.cli.constants.display import setup_complete_panel


class Setup:
    """Performs project creation for the `init` command."""

    def __init__(self, project_name: str, console: Console) -> None:
        self.project_name = project_name
        self.console = console

    def build(self) -> None:
        """Builds the project."""
        tasks = [
            "Test 1",
            "test 2",
            "test 3",
        ]

        for task in track(tasks, description="Building Project"):
            # task()
            pass

        self.console.print(setup_complete_panel())
        raise typer.Exit(code=SetupSuccessCodes.COMPLETE)


class SetupTasks:
    """Contains the tasks for the `init` command."""

    pass
