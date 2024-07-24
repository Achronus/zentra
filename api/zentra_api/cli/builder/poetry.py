from pathlib import Path
from pydantic import BaseModel, field_validator


def toml_str(key: str, value: str | list[str]) -> str:
    """Converts a key-value pair into a string format suitable for `toml` files."""
    if isinstance(value, list):
        value_str = ", ".join([v for v in value])
        return f'{key} = ["{value_str}"]\n'

    return f'{key} = "{value}"\n'


class PoetryDescription(BaseModel):
    """A model for storing the poetry description."""

    name: str
    version: str = "0.1.0"
    description: str = "A FastAPI backend for processing API data."
    authors: list[str]
    readme: str = "README.md"

    def as_str(self) -> list[str]:
        """Returns the description as a list of strings."""
        attrs_dict = self.model_dump()
        return [toml_str(key, value) for key, value in attrs_dict.items()]


class PoetryScript(BaseModel):
    """A model for storing poetry scripts."""

    name: str
    command: str

    def as_str(self) -> str:
        """Returns the script as a string."""
        return toml_str(self.name, self.command)


class PipPackage(BaseModel):
    """Represents a single pip package."""

    name: str
    version: str

    @field_validator("version")
    def validate_version(cls, version: str) -> str:
        parts = version.split(".")

        if len(parts) >= 2:
            return f"{parts[0]}.{parts[1]}"

        return version

    def as_str(self) -> str:
        """Returns the package as a string."""
        return toml_str(self.name, f"^{self.version}")


class Dependencies(BaseModel):
    """Represents a list of pip packages."""

    packages: list[PipPackage]
    group: str | None = None

    @field_validator("group")
    def validate_group(cls, group: str | None) -> str:
        if group:
            return f"[tool.poetry.group.{group}.dependencies]\n"

        return "[tool.poetry.dependencies]\n"

    def as_str(self) -> str:
        """Returns the dependencies as a string."""
        return "\n".join(
            self.group,
            *[package.as_str() for package in self.packages],
        )


class PoetryFileBuilder:
    """A builder for creating the `pyproject.toml`."""

    def __init__(self, project_name: str, author: str) -> None:
        self.description = PoetryDescription(name=project_name, authors=[author])
        self.scripts = [
            PoetryScript(name="run-dev", command="app.run:development"),
            PoetryScript(name="run-prod", command="app.run:production"),
        ]
        self.coverage = toml_str(
            "addopts",
            f"--cov-report term-missing --cov={project_name} tests/",
        )
        self.threshold = "[tool.poetry.dependencies]"

    def build_details(self) -> str:
        """A helper function to builds the details as a string."""
        return "".join(
            [
                "[tool.poetry]\n",
                *self.description.as_str(),
                "\n[tool.poetry.scripts]\n",
                *[script.as_str() for script in self.scripts],
            ]
        )

    def get_other_content(self, filepath: Path) -> str:
        """A helper function for getting the other content of the toml file."""
        with open(filepath, "r") as f:
            file_content = f.read()

        other_idx = file_content.index(self.threshold)
        return file_content[other_idx:]

    def build_new_content(self, filepath: Path) -> str:
        """Creates the new content for the file."""
        details = self.build_details()
        other_content = self.get_other_content(filepath)
        return f"{details}\n{other_content}"

    def update(self, filepath: Path) -> None:
        """Updates an existing toml file with a new description and scripts."""
        new_content = self.build_new_content(filepath)

        with open(filepath, "w") as f:
            f.write(new_content)
