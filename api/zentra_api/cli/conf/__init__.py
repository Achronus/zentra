import os
from pathlib import Path


from pydantic import BaseModel, Field, field_validator


class ProjectDetails(BaseModel):
    """Stores useful information relevant to the project."""

    project_name: str
    author_name: str = "Placeholder Name"
    author_email: str = "placeholder@email.com"
    root: Path = Path(os.getcwd())
    app_name: str = Field("app", frozen=True)

    @property
    def project_path(self) -> Path:
        return Path(self.root, self.project_name)

    @property
    def project_dir(self) -> str:
        return "/".join(self.project_path.parts[-2:])

    @property
    def author(self) -> str:
        return f"{self.author_name} <{self.author_email}>"

    @property
    def app_path(self) -> Path:
        return Path(self.project_path, self.app_name)

    @field_validator("project_name")
    def validate_project_name(cls, name: str) -> str:
        def split_n_join(value: str, char: str) -> str:
            return "_".join(value.split(char))

        for char in [" ", "-"]:
            name = split_n_join(name, char)

        return name.lower()
