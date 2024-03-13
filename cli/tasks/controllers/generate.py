import os

from cli.conf.create import make_directories
from cli.conf.extract import extract_file_pairs_from_list
from cli.conf.format import name_from_camel_case
from cli.conf.move import transfer_folder_file_pairs
from cli.conf.storage import ModelStorage, GeneratePathStorage
from cli.tasks.controllers.base import BaseController, status

from zentra.core import Zentra


class GenerateController(BaseController):
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
            (self.extract_models, f"Retrieving {zentra_str} models"),
            (self.identify_new_files, f"Checking for new {zentra_str} models"),
            (self.create_files, f"Creating {react_str} component files"),
            (self.update_template_files, f"Configuring {react_str} components"),
        ]

        super().__init__(tasks)

        self.storage = ModelStorage()
        self.paths = paths
        self.zentra = zentra

    @status
    def extract_models(self) -> None:
        """Extracts the Zentra models and prepares them for file generation."""
        formatted_names = [
            f"{name_from_camel_case(name)}.tsx" for name in self.zentra.component_names
        ]

        filtered_list = extract_file_pairs_from_list(
            self.storage.base_files, formatted_names
        )

        # Handle uploadthing files
        if "file-upload.tsx" in formatted_names:
            uploadthing_files = extract_file_pairs_from_list(
                self.storage.base_files, ["uploadthing"], idx=0
            )
            filtered_list += uploadthing_files
        else:
            self.storage.folders_to_generate.remove("uploadthing")

        # Store found models
        self.storage.files_to_generate = filtered_list

    @status
    def identify_new_files(self) -> None:
        """Identifies the new files needed (if applicable) and stores them into `self.storage`."""
        pass

    def _make_needed_dirs(self) -> None:
        """Makes the needed directories in the `zentra/generate` folder."""
        for dir in self.storage.folders_to_generate:
            make_directories(os.path.join(self.paths.generate, dir))

    def _copy_base_ui(self) -> None:
        """Copies a list of `zentra/model` files from one location to another."""
        transfer_folder_file_pairs(
            self.storage.files_to_generate,
            self.paths.component,
            self.paths.generate,
            src_sub_dir="base",
        )

    @status
    def create_files(self) -> None:
        """Creates the React components based on the extracting models."""
        self._make_needed_dirs()
        self._copy_base_ui()

    @status
    def update_template_files(self) -> None:
        """Updates the React components based on the Zentra model attributes."""
        pass
        # Steps 6 to 8
