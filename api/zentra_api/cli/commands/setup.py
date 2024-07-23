import os
from pathlib import Path
import subprocess
from typing import Callable
import typer

from zentra_api.cli.builder.poetry import PoetryFile
from zentra_api.cli.conf import ProjectDetails
from zentra_api.cli.constants import MAGIC, SetupSuccessCodes, console
from zentra_api.cli.constants.display import setup_complete_panel
from zentra_api.cli.conf.logger import task_output_logger, task_error_logger

from rich.progress import track


class Setup:
    """Performs project creation for the `init` command."""

    def __init__(self, project_name: str, root: Path = Path(os.getcwd())) -> None:
        self.project_name = project_name

        self.details = ProjectDetails(project_name=project_name, root=root)
        self.setup_tasks = SetupTasks(self.details)

    def project_exists(self) -> bool:
        """A helper method to check if a project with the `project_name` exists."""
        if self.details.project_path.exists():
            dirs = list(self.details.project_path.iterdir())
            if len(dirs) > 0:
                return True

        return False

    def build(self) -> None:
        """Builds the project."""
        if self.project_exists():
            raise typer.Exit(code=SetupSuccessCodes.ALREADY_CONFIGURED)

        tasks = self.setup_tasks.get_tasks()

        os.makedirs(self.details.project_path, exist_ok=True)
        os.chdir(self.details.project_path)
        console.print(
            f"\n{MAGIC} Creating new [green]FastAPI[/green] project called: [magenta]{self.project_name}[/magenta] -> [yellow]{self.details.project_path}[/yellow] {MAGIC}\n"
        )

        for task in track(tasks, description="Building..."):
            # task()
            pass

        console.print(setup_complete_panel(self.details))
        raise typer.Exit(code=SetupSuccessCodes.COMPLETE)


class SetupTasks:
    """Contains the tasks for the `init` command."""

    def __init__(self, details: ProjectDetails) -> None:
        self.details = details

    def _create_virtual_env(self) -> None:
        """Creates a virtual environment in the project directory."""
        response = subprocess.run(
            ["python", "-m", "venv", "env"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        task_output_logger.debug(response.stderr)
        task_error_logger.error(response.stdout)

    def _update_toml(self) -> None:
        """Updates the `pyproject.toml` file."""
        toml_path = Path(self.details.project_path, "pyproject.toml")
        builder = PoetryFile(
            self.details.project_name,
            self.details.author,
        )
        builder.update(toml_path)

    def get_tasks(self) -> list[Callable]:
        """Gets the tasks to run as a list of methods."""
        return [
            self._create_virtual_env,
            # self._update_toml
        ]
