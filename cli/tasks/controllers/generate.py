import os

import typer

from cli.conf.constants import GenerateSuccessCodes
from cli.conf.create import make_directories
from cli.conf.extract import extract_file_pairs_from_list
from cli.conf.move import remove_folder_file_pairs, transfer_folder_file_pairs
from cli.conf.storage import ModelFileStorage, ModelStorage, GeneratePathStorage
from cli.conf.types import LibraryNamePairs
from cli.tasks.controllers.base import BaseController, status

from cli.templates.extract import (
    LocalExtractor,
    ModelExtractor,
    extract_component_details,
)
from cli.templates.retrieval import ComponentRetriever
from zentra.core import Zentra


class GenerateControllerHelper:
    """
    A class for helper functions used across multiple GenerateControllers.

    Parameters:
    - zentra (zentra.core.Zentra) - the Zentra application containing components to generate
    - paths (storage.GeneratePathStorage) - a path storage container with paths specific to the controller
    """

    def __init__(self, zentra: Zentra, paths: GeneratePathStorage):
        self.zentra = zentra
        self.paths = paths

        self.storage: ModelStorage = None

        # self.storage.base_names.components = zentra.name_storage.components
        # self.storage.base_names.pages = zentra.name_storage.pages

    def _check_for_uploadthing(
        self, generate_list: LibraryNamePairs, filenames: list[str]
    ) -> LibraryNamePairs:
        """Checks for uploadthings `FileUpload` in a list of Zentra model filenames. If it exists, we extract the required filenames and add them to the `generate_list`. If it doesn't, we return the `generate_list` as is."""
        if "file-upload.tsx" in filenames:
            uploadthing_files = extract_file_pairs_from_list(
                self.storage.base_files, ["uploadthing"], idx=0
            )
            generate_list += uploadthing_files
        else:
            self.storage.folders_to_generate.remove("uploadthing")

        return generate_list

    def _filter_ut(self, components: FolderFilePair) -> FolderFilePair:
        """A helper function for calculating the correct number of components, factoring in that `uploadthing` has multiple files."""
        filtered = []
        ut_found = False

        for model in components:
            if model[0] == "uploadthing":
                if not ut_found:
                    filtered.append(model)
                    ut_found = True
            else:
                filtered.append(model)
        return filtered


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
        self.model_extractor = ModelExtractor(url=url)
        self.local_extractor = LocalExtractor(
            generate_path=paths.generate, name_storage=zentra.name_storage
        )

        self.local_builder = LocalBuilder(
            generate_path=paths.generate,
            folders_to_generate=None,
        )

        react_str = "[cyan]React[/cyan]"
        zentra_str = "[magenta]Zentra[/magenta]"

        tasks = [
            (
                self.retrieve_assets,
                "Retrieving [yellow]component[/yellow] filepaths from [yellow]GitHub[/yellow]",
            ),
            (self.extract_models, f"Extracting {zentra_str} models"),
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
    def retrieve_assets(self) -> None:
        """Retrieves the component asset filenames from Github and stores them in the controller."""
        retriever = ComponentRetriever(url=self.url)
        retriever.extract()

        self.model_extractor.filenames = retriever.storage
        self.local_builder.folders_to_generate = self.model_extractor.folders()

    @status
    def extract_models(self) -> None:
        """Extracts the Zentra models and prepares them for file generation."""
        base_names = self.model_extractor.component_base_names()
        user_models = self.local_extractor.user_models()

        user_model_pairs = self.local_extractor.format_user_models(
            pairs=base_names, targets=user_models
        )

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
