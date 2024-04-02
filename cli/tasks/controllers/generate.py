import os

import typer

from cli.conf.constants import GenerateSuccessCodes
from cli.conf.create import make_code_file_from_url, make_directories
from cli.conf.cleanup import remove_files
from cli.conf.storage import ModelFileStorage, ModelStorage, GeneratePathStorage
from cli.conf.types import LibraryNamePairs
from cli.tasks.controllers.base import BaseController, status

from cli.templates import ComponentFileType
from cli.templates.extract import (
    LocalExtractor,
    extract_component_details,
)
from cli.templates.retrieval import CodeRetriever
from zentra.core import Zentra
from zentra.core.enums.ui import LibraryType


class LocalBuilder:
    """
    Handles functionality for creating files and directories in the Zentra generate folder.

    Parameters:
    - `generate_path` (`string`) - path to the Zentra generate folder
    - `folders_to_generate` (`list[string]`) - a list of folder names to create
    """

    def __init__(self, generate_path: str, folders_to_generate: list[str]) -> None:
        self.path = generate_path
        self.folders_to_generate = folders_to_generate

    def make_dirs(self) -> None:
        """Makes the needed directories."""
        for dir in self.folders_to_generate:
            make_directories(os.path.join(self.path, dir))

    def create_base_files(self, models: LibraryNamePairs, sub_dir: str) -> None:
        """Creates the base files for Zentra model that need to be generated in the generate folder."""
        # TODO: replace with 'code_from_files'
        transfer_folder_file_pairs(
            self.storage.components.generate,
            self.paths.component,
            self.path,
            src_sub_dir=sub_dir,
        )

    def remove_models(self) -> None:
        """Removes a list of Zentra models from the generate folder."""
        # TODO: update parameters
        remove_folder_file_pairs(self.storage.components.remove, self.paths.generate)


class GenerateController(BaseController):
    """
    A controller for handling tasks that generate the Zentra components.

    Parameters:
    - `url` (`string`) - a GitHub URL housing the component files
    - `zentra` (`zentra.core.Zentra`) - the Zentra application containing components to generate
    - `paths` (`storage.GeneratePathStorage`) - a path storage container with paths specific to the controller
    """

    def __init__(self, url: str, zentra: Zentra, paths: GeneratePathStorage) -> None:
        self.url = url

        self.storage: ModelStorage = ModelStorage()
        self.local_extractor = LocalExtractor(
            generate_path=paths.generate, name_storage=zentra.name_storage
        )

        self.local_builder = LocalBuilder(
            generate_path=paths.generate,
            components=None,
        )

        react_str = "[cyan]React[/cyan]"
        zentra_str = "[magenta]Zentra[/magenta]"

        tasks = [
            (self.detect_models, f"Detecting {zentra_str} models"),
            (
                self.retrieve_assets,
                "Retrieving [yellow]component[/yellow] assets from [yellow]GitHub[/yellow]",
            ),
            (self.update_files, f"Handling {react_str} component files"),
            (self.update_template_files, f"Configuring {react_str} components"),
        ]

        BaseController.__init__(self, tasks)

    def store_models(
        self,
        existing: LibraryNamePairs,
        add: LibraryNamePairs,
        remove: LibraryNamePairs,
    ) -> None:
        """Stores Zentra model changes in `ModelStorage`."""
        changes = {
            "existing": existing,
            "generate": add,
            "remove": remove,
            "counts": self.local_extractor.model_counts,
        }

        self.storage.components = ModelFileStorage(**changes)

    @status
    def detect_models(self) -> None:
        """Detects the user defined Zentra models and prepares them for file generation."""
        user_model_pairs = self.local_extractor.user_models()
        existing_models = self.local_extractor.existing_models()

        if user_model_pairs == existing_models:
            raise typer.Exit(code=GenerateSuccessCodes.NO_NEW_COMPONENTS)

        to_generate, to_remove = self.local_extractor.model_changes(
            existing_models,
            user_model_pairs,
        )

        self.store_models(
            existing=existing_models,
            add=to_generate,
            remove=to_remove,
        )

    @status
    def update_files(self) -> None:
        """Creates or removes the React components based on the extracted models."""
        if self.storage.components.counts.generate != 0:
            self.local_builder.make_dirs()
            self.local_builder.create_base_files(sub_dir="base")

        if self.storage.components.counts.remove != 0:
            self.local_builder.remove_models()

    @status
    def update_template_files(self) -> None:
        """Updates the React components based on the Zentra model attributes."""
        pass
        # Steps 6 to 8
