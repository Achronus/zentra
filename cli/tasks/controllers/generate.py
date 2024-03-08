import os
import typer
from pydantic import BaseModel

from cli.conf.checks import (
    check_file_contents,
    check_file_exists,
    check_models_registered,
)
from cli.conf.format import name_from_camel_case
from cli.tasks.controllers.base import BaseController, status
from cli.conf.constants import (
    LocalUploadthingFilepaths,
    CommonErrorCodes,
    ZentaFilepaths,
)
from cli.conf.extract import get_filenames_in_subdir

from zentra.core import Zentra


# TODO: add --nextjs flag
NEXTJS_PROJECT = False


class NameStorage(BaseModel):
    """A storage container for Zentra model filenames."""

    UI_BASE: list[str] = get_filenames_in_subdir(LocalUIComponentFilepaths.BASE)
    UI_TO_GENERATE: list[str] = []

    UPLOADTHING: list[str] = get_filenames_in_subdir(
        LocalUploadthingFilepaths.BASE_NEXTJS
        if NEXTJS_PROJECT
        else LocalUploadthingFilepaths.BASE_BASIC
    )
    UT_TO_GENERATE: list[str] = []


class GenerateController(BaseController):
    """
    A controller for handling tasks that generate the Zentra components.

    Parameters:
    - zentra (zentra.core.Zentra) - the Zentra application containing components to generate
    """

    def __init__(self, zentra: Zentra) -> None:
        react_str = "[cyan]React[/cyan]"
        zentra_str = "[magenta]Zentra[/magenta]"

        tasks = [
            (self.check_config, f"Checking {zentra_str} configured correctly"),
            (self.extract_models, f"Retrieving {zentra_str} models"),
            (self.create_files, f"Creating {react_str} component files"),
            (self.update_template_files, f"Configuring {react_str} components"),
        ]

        super().__init__(tasks)

        self.storage = NameStorage()
        self.zentra = zentra

    @status
    def check_config(self) -> None:
        """Checks that the config files are setup correctly."""
        if not check_models_registered(self.zentra):
            raise typer.Exit(code=CommonErrorCodes.MODELS_DIR_MISSING)

        # Check config file exists
        if not check_file_exists(
            os.path.join(ZentaFilepaths.MODELS, ZentaFilepaths.SETUP_FILENAME)
        ):
            raise typer.Exit(code=CommonErrorCodes.CONFIG_MISSING)

        # Check config file content is valid
        valid_content = check_file_contents()

        if not valid_content:
            raise typer.Exit(code=1)

    @status
    def extract_models(self) -> None:
        """Extracts the Zentra models and prepares them for file generation."""
        formatted_names = [
            f"{name_from_camel_case(name)}.tsx" for name in self.zentra.component_names
        ]

        self.storage.UT_TO_GENERATE = list(
            set(formatted_names) - set(self.storage.UI_BASE)
        )

        self.storage.UI_TO_GENERATE = list(
            set(formatted_names) - set(self.storage.UT_TO_GENERATE)
        )

    @status
    def create_files(self) -> None:
        """Creates the React components based on the extracting models."""
        pass
        # Steps 4 and 5

    @status
    def update_template_files(self) -> None:
        """Updates the React components based on the Zentra model attributes."""
        pass
        # Steps 6 to 8


# 1. [X] Get filenames from components/ui/base <- make dynamic for future libraries
# 2. [X] Get components from zentra class
# 3. [X] Convert component names from camelcase
# 4. [] Copy files in base that match component names to components/zentra/ui/base
# 5. [] Copy template files that match component names to components/zentra/ui/<filename>
# 6. [] Convert components to JSON
# 7. [] Update template files with information from component attributes using JSON
# 8. [] Update components/zentra/ui/index.tsx with component exports
