import os
from pathlib import Path
import subprocess
import shutil
from typing import Callable

from zentra_sdk.cli.builder.docker import DockerBuilder
from zentra_sdk.cli.conf.logger import set_loggers
from zentra_sdk.cli.constants import (
    DOCKER_FRONTEND_DETAILS,
    CommonErrorCodes,
    SetupSuccessCodes,
    ProjectPaths,
    console,
)
from zentra_sdk.cli.constants.display import (
    already_configured_panel,
    setup_complete_panel,
)
from zentra_sdk.cli.constants.message import creation_msg

import typer
from rich.progress import track
import docker
from docker.errors import DockerException


class Setup:
    """Performs project creation for the `init` command."""

    def __init__(self, root: Path = Path(os.getcwd())) -> None:
        if not self.docker_installed():
            raise typer.Exit(code=CommonErrorCodes.DOCKER_NOT_INSTALLED)

        self.paths = ProjectPaths(root)
        self.setup_tasks = SetupTasks(paths=self.paths)

    def project_exists(self) -> bool:
        """Checks if a project has already been created."""

        def dir_exists_not_empty(path: Path) -> bool:
            if path.is_dir():
                if not os.listdir(path):
                    shutil.rmtree(path)
                    return False

                return True

            return False

        backend_exists = dir_exists_not_empty(self.paths.BACKEND_PATH)
        frontend_exists = dir_exists_not_empty(self.paths.FRONTEND_PATH)
        return backend_exists or frontend_exists

    def docker_installed(self) -> bool:
        """Checks if Docker is installed."""
        try:
            client = docker.from_env()
            client.ping()
            return True
        except DockerException:
            return False

    def build(self) -> None:
        """Builds the project."""
        if self.project_exists():
            console.print(already_configured_panel())
            raise typer.Exit(code=SetupSuccessCodes.ALREADY_CONFIGURED)

        tasks = self.setup_tasks.get_tasks()

        for task in track(tasks, description="Building..."):
            task()

        console.print(setup_complete_panel())
        raise typer.Exit(code=SetupSuccessCodes.COMPLETE)


class SetupTasks:
    """Contains the tasks for the `init` command."""

    def __init__(self, paths: ProjectPaths, test_logging: bool = False) -> None:
        self.logger = set_loggers(test_logging)
        self.docker_frontend = DockerBuilder(**DOCKER_FRONTEND_DETAILS)
        self.paths = paths

    def _build_frontend(self) -> None:
        """Builds the frontend from a docker container."""
        self.docker_frontend.use(path=self.paths.FRONTEND_PATH)

    def _build_backend(self) -> None:
        """Builds the backend using the `API` package."""
        subprocess.run(["zentra-api", "init", "backend"])

    def get_tasks(self) -> list[Callable]:
        """Gets the tasks to run as a list of methods."""
        console.print(creation_msg())

        return [
            self._build_backend,
            self._build_frontend,
        ]
