import os
from pathlib import Path
import subprocess
from typing import Callable
import typer

from zentra_api.cli.builder.poetry import PoetryFileBuilder
from zentra_api.cli.conf import ProjectDetails
from zentra_api.cli.constants import (
    CORE_PIP_PACKAGES,
    DEV_PIP_PACKAGES,
    SetupSuccessCodes,
    console,
)
from zentra_api.cli.constants.display import setup_complete_panel
from zentra_api.cli.conf.logger import set_loggers

from rich.progress import track

from zentra_api.cli.constants.message import creation_msg


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

        for task in track(tasks, description="Building..."):
            task()

        console.print(setup_complete_panel(self.details))
        raise typer.Exit(code=SetupSuccessCodes.COMPLETE)


class SetupTasks:
    """Contains the tasks for the `init` command."""

    def __init__(self, details: ProjectDetails, test_logging: bool = False) -> None:
        self.details = details

        self.logger = set_loggers(test_logging)

    def __run_command(self, command: list[str]) -> None:
        """A helper method for running Python commands. Stores output to separate loggers."""
        response = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        self.logger.stdout.debug(response.stdout)
        self.logger.stderr.error(response.stderr)

    def _create_virtual_env(self) -> None:
        """Creates a virtual environment in the project directory."""
        self.__run_command(["python", "-m", "venv", "env"])

    def _make_toml(self) -> None:
        """Updates the `pyproject.toml` file."""
        toml_path = Path(self.details.project_path, "pyproject.toml")
        open(toml_path, "x").close()
        builder = PoetryFileBuilder(
            self.details.project_name,
            self.details.author,
        )
        builder.update(toml_path, CORE_PIP_PACKAGES, DEV_PIP_PACKAGES)

    def get_tasks(self) -> list[Callable]:
        """Gets the tasks to run as a list of methods."""
        os.makedirs(self.details.project_path, exist_ok=True)
        os.chdir(self.details.project_path)

        console.print(
            creation_msg(
                self.details.project_name,
                self.details.project_path,
            )
        )

        return [
            self._make_toml,
            # self._create_virtual_env,
        ]
