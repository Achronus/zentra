import requests
from pathlib import Path

import toml

from zentra_api.cli.conf.logger import task_error_logger, task_test_logger

from pydantic import BaseModel, field_validator

from zentra_api.cli.constants import PYTHON_VERSION, pypi_url


class Description(BaseModel):
    """A model for storing the poetry description."""

    name: str
    version: str = "0.1.0"
    description: str = "A FastAPI backend for processing API data."
    authors: list[str] = ["Placeholder <placeholder@email.com>"]
    readme: str = "README.md"


class Script(BaseModel):
    """A model for storing poetry scripts."""

    name: str
    command: str


class PipPackage(BaseModel):
    """Represents a single pip package."""

    name: str
    version: str

    @field_validator("version")
    def validate_version(cls, version: str) -> str:
        parts = version.split(".")

        if len(parts) >= 2:
            return f"^{parts[0]}.{parts[1]}"

        return f"^{version}"


class PoetryFile(BaseModel):
    """A model representation of a poetry file."""

    desc: Description
    scripts: list[Script]
    core_deps: list[PipPackage]
    dev_deps: list[PipPackage]

    @property
    def build_system(self) -> dict:
        return {
            "requires": ["poetry-core"],
            "build-backend": "poetry.core.masonry.api",
        }

    @field_validator("core_deps")
    def validate_core_deps(cls, core_deps: list[PipPackage]) -> list[PipPackage]:
        python_dep = PipPackage(name="python", version=PYTHON_VERSION)
        return [python_dep] + core_deps

    @staticmethod
    def _deps_to_dict(deps: list[PipPackage]) -> dict:
        return {package.name: package.version for package in deps}

    def _scripts_to_dict(self) -> dict:
        return {script.name: script.command for script in self.scripts}

    def to_dict(self) -> dict:
        return {
            "tool": {
                "poetry": self.desc.model_dump(),
                "scripts": self._scripts_to_dict(),
                "dependencies": self._deps_to_dict(self.core_deps),
                "group": {
                    "dev": {
                        "dependencies": self._deps_to_dict(self.dev_deps),
                    }
                },
            },
            "build-system": self.build_system,
        }


class PoetryFileBuilder:
    """A builder for creating the `pyproject.toml`."""

    def __init__(self, project_name: str, test_logging: bool = False) -> None:
        self.logger = task_test_logger if test_logging else task_error_logger

        self.description = Description(name=project_name)
        self.scripts = [
            Script(name="run-dev", command="app.run:development"),
            Script(name="run-prod", command="app.run:production"),
        ]

    def build(self, core_deps: list[str], dev_deps: list[str]) -> PoetryFile:
        """Builds the poetry file."""
        return PoetryFile(
            desc=self.description,
            scripts=self.scripts,
            core_deps=self.get_packages(core_deps),
            dev_deps=self.get_packages(dev_deps),
        )

    def get_packages(self, packages: list[str]) -> list[PipPackage]:
        """Gets the dependency package versions for the project."""
        dependencies = []

        for package in packages:
            try:
                response = requests.get(pypi_url(package))
                response.raise_for_status()
                data = response.json()

                version = data["info"]["version"]
                dependencies.append(PipPackage(name=package, version=version))

            except (requests.HTTPError, requests.RequestException):
                self.logger.error(f"{package} doesn't exist in 'pypi' directory.")
                continue

        return dependencies

    def update(self, filepath: Path, core_deps: list[str], dev_deps: list[str]) -> None:
        """Updates an existing toml file."""
        file = self.build(core_deps, dev_deps)
        new_content = file.to_dict()

        with open(filepath, "w") as f:
            toml.dump(new_content, f)
