import os

import typer

from cli.conf.constants import GenerateSuccessCodes
from cli.conf.create import make_directories
from cli.conf.extract import extract_file_pairs_from_list, get_filename_dir_pairs
from cli.conf.format import name_from_camel_case
from cli.conf.move import remove_folder_file_pairs, transfer_folder_file_pairs
from cli.conf.storage import ModelStorage, GeneratePathStorage
from cli.conf.types import FolderFilePair
from cli.tasks.controllers.base import BaseController, status

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
        self.storage = ModelStorage()

    def _get_and_format_models(self) -> list[str]:
        """Retrieves the Zentra model from the app and converts the name into a suitable format for comparison."""
        return [
            f"{name_from_camel_case(name)}.tsx" for name in self.zentra.component_names
        ]

    def _make_needed_dirs(self) -> None:
        """Makes the needed directories in the `zentra/generate` folder."""
        for dir in self.storage.folders_to_generate:
            make_directories(os.path.join(self.paths.generate, dir))

    def _generate_files(self, sub_dir: str) -> None:
        """Create a list of Zentra model files in the generate folder."""
        transfer_folder_file_pairs(
            self.storage.models_to_generate,
            self.paths.component,
            self.paths.generate,
            src_sub_dir=sub_dir,
        )

    def _remove_files(self) -> None:
        """Removes a list of Zentra models from the generate folder."""
        remove_folder_file_pairs(self.storage.models_to_remove, self.paths.generate)

    def _check_for_uploadthing(
        self, generate_list: FolderFilePair, filenames: list[str]
    ) -> FolderFilePair:
        """Checks for uploadthings `FileUpload` in a list of Zentra model filenames. If it exists, we extract the required filenames and add them to the `generate_list`. If it doesn't, we return the `generate_list` as is."""
        if "file-upload.tsx" in filenames:
            uploadthing_files = extract_file_pairs_from_list(
                self.storage.base_files, ["uploadthing"], idx=0
            )
            generate_list += uploadthing_files
        else:
            self.storage.folders_to_generate.remove("uploadthing")

        return generate_list

    def _get_existing_models(self) -> FolderFilePair:
        """Retrieves a list of existing models."""
        return get_filename_dir_pairs(parent_dir=self.paths.generate)

    def _get_model_updates(
        self, old: FolderFilePair, new: FolderFilePair
    ) -> FolderFilePair:
        """Extracts the difference between folder and filenames to detect Zentra model changes."""
        largest, smallest = max(old, new), min(old, new)
        return list(set(largest) - set(smallest))

    def _get_model_changes(
        self,
        model_updates: FolderFilePair,
    ) -> tuple[FolderFilePair, FolderFilePair]:
        """Provides two lists of `FolderFilePair` changes. In the form of: `(to_remove, to_add)`."""
        to_remove, to_add = [], []
        for model in model_updates:
            if model in self.storage.existing_models:
                to_remove.append(model)
            else:
                to_add.append(model)

        return to_remove, to_add


class GenerateController(BaseController, GenerateControllerHelper):
    """
    A controller for handling tasks that generate the Zentra components.

    Parameters:
    - zentra (zentra.core.Zentra) - the Zentra application containing components to generate
    - paths (storage.GeneratePathStorage) - a path storage container with paths specific to the controller
    """

    def __init__(self, zentra: Zentra, paths: GeneratePathStorage) -> None:
        react_str = "[cyan]React[/cyan]"
        zentra_str = "[magenta]Zentra[/magenta]"

        tasks = [
            (self.extract_models, f"Extracting {zentra_str} models"),
            (self.update_files, f"Handling {react_str} component files"),
            (self.update_template_files, f"Configuring {react_str} components"),
        ]

        GenerateControllerHelper.__init__(self, zentra, paths)
        BaseController.__init__(self, tasks)

    @status
    def extract_models(self) -> None:
        """Extracts the Zentra models and prepares them for file generation."""
        formatted_names = self._get_and_format_models()

        generate_list = extract_file_pairs_from_list(
            self.storage.base_files, formatted_names
        )
        generate_list = self._check_for_uploadthing(generate_list, formatted_names)
        model_updates = self._get_existing_models()

        if generate_list == model_updates:
            raise typer.Exit(code=GenerateSuccessCodes.NO_NEW_COMPONENTS)

        self.storage.existing_models = model_updates
        model_updates = self._get_model_updates(generate_list, model_updates)

        self.storage.models_to_remove, self.storage.models_to_generate = (
            self._get_model_changes(model_updates)
        )

    @status
    def update_files(self) -> None:
        """Creates or removes the React components based on the extracted models."""
        if len(self.storage.models_to_generate) != 0:
            self._make_needed_dirs()
            self._generate_files(sub_dir="base")

        if len(self.storage.models_to_remove) != 0:
            self._remove_files()

    @status
    def update_template_files(self) -> None:
        """Updates the React components based on the Zentra model attributes."""
        pass
        # Steps 6 to 8
