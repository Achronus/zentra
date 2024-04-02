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
    - `url` (`string`) - a GitHub URL housing the component files
    - `paths` (`storage.GeneratePathStorage`) - a path storage container with paths specific to the controller
    - `components` (`ModelFileStorage`) - a container filled with the Zentra model pairs to `generate` and `remove`
    """

    def __init__(
        self, url: str, paths: GeneratePathStorage, components: ModelFileStorage
    ) -> None:
        self.url = url
        self.paths = paths
        self.components = components

        self.retriever = CodeRetriever(url=url)

    def folders(self, pairs: LibraryNamePairs) -> list[str]:
        """Returns a list of `library_name` folders from a list of `LibraryNamePairs`."""
        return list(set(item[0] for item in pairs))

    def make_dirs(self) -> None:
        """Creates the needed directories inside the generate folder."""
        for dir in self.folders(self.components.generate):
            make_directories(os.path.join(self.paths.generate, dir))

    def create_base_files(self, file_type: ComponentFileType) -> None:
        """
        Creates the base files for Zentra models that need to be generated in the generate folder.

        Parameter:
        - `file_type` (`string`) - the type of file to extract. Options: ['base', 'templates', 'lib']
        """
        for folder, filename in self.components.generate:
            url = f"{self.url}/{folder}/{file_type}"
            make_code_file_from_url(
                url=url,
                filename=filename,
                dest_path=self.paths.generate,
            )

            if folder == LibraryType.UPLOADTHING.value:
                pass

    def remove_models(self) -> None:
        """Removes a list of Zentra models from the generate folder."""
        remove_files(pairs=self.components.remove, dir_path=self.paths.generate)

        if LibraryType.UPLOADTHING.value in self.folders(self.components.remove):
            pass


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
            url=url,
            paths=paths,
            components=None,
        )

        react_str = "[cyan]React[/cyan]"
        zentra_str = "[magenta]Zentra[/magenta]"

        tasks = [
            (self.detect_models, f"Detecting {zentra_str} models"),
            (
                self.retrieve_assets,
                "Retrieving core [yellow]component[/yellow] assets from [yellow]GitHub[/yellow]",
            ),
            (self.remove_models, f"Removing unused {zentra_str} models"),
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
        self.local_builder.components = self.storage.components

    @status
    def detect_models(self) -> None:
        """Detects the user defined Zentra models and prepares them for file generation."""
        user_model_pairs = self.local_extractor.user_models()
        existing_models = self.local_extractor.existing_models()

        if user_model_pairs == existing_models:
            raise typer.Exit(code=GenerateSuccessCodes.NO_NEW_COMPONENTS)

        to_add, to_remove = self.local_extractor.model_changes(
            existing_models,
            user_model_pairs,
        )

        self.store_models(
            existing=existing_models,
            add=to_add,
            remove=to_remove,
        )

    @status
    def retrieve_assets(self) -> None:
        """Retrieves the core component assets from GitHub and stores them in the Zentra generate folder."""
        if self.storage.components.counts.generate != 0:
            self.local_builder.make_dirs()
            self.local_builder.create_base_files(sub_dir="base")

    @status
    def remove_models(self) -> None:
        """Removes the React component files that are no longer used from the Zentra generate folder."""
        if self.storage.components.counts.remove != 0:
            self.local_builder.remove_models()

    @status
    def update_template_files(self) -> None:
        """Updates the React components based on the Zentra model attributes."""
        pass
