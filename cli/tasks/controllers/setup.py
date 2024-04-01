import os

from cli.conf.storage import ConfigExistStorage, SetupPathStorage
from cli.tasks.controllers.base import BaseController, status
from cli.conf.create import make_directories, make_file, make_code_files_from_url
from cli.conf.extract import local_path
from cli.templates.retrieval import (
    CodeRetriever,
    InitFilesStorage,
    ZentraSetupRetriever,
)


class SetupController(BaseController):
    """
    A controller for handling tasks for configuring Zentra.

    Parameters:
    - `url` (`string`) - a GitHub URL housing the setup files
    - `paths` (`storage.SetupPathStorage`) - a path storage container with filepaths specific to the controller
    - `config_exists` (`storage.ConfigExistStorage`) - a boolean value storage container for config checks
    """

    def __init__(
        self, url: str, paths: SetupPathStorage, config_exists: ConfigExistStorage
    ) -> None:
        self.url = url
        self.paths = paths
        self.config_exists = config_exists

        self.config_storage: InitFilesStorage = None

        demo_folder_str = (
            f"{local_path(self.paths.models)}/{os.path.basename(self.paths.demo)}"
        )
        highlighted_path = f"[magenta]{demo_folder_str}[/magenta]"

        tasks = [
            (
                self.retrieve_assets,
                "Retrieving [yellow]config[/yellow] filepaths from [yellow]GitHub[/yellow]",
            ),
            (
                self.create_missing_files,
                "Creating [yellow]config[/yellow] files",
            ),
            (
                self.create_demo_files,
                f"Creating demo files in {highlighted_path}",
            ),
        ]

        super().__init__(tasks)

    def _make_models_dir(self) -> None:
        """Creates the `zentra/models` directory if needed."""
        if not self.config_exists.models_folder_exists:
            make_directories(self.paths.models)

    def _make_config_file(self) -> None:
        """Creates the setup file in `zentra/models` if it doesn't exist."""
        if not self.config_exists.config_file_exists:
            config_url = f"{self.url}/{self.config_storage.config}"
            retriever = CodeRetriever(url=config_url)
            make_file(self.paths.config, retriever.extract())

    @status
    def retrieve_assets(self) -> None:
        """Retrieves the filenames and filepaths for the configuration files."""
        retriever = ZentraSetupRetriever(url=self.url)
        retriever.extract()

        self.config_storage = retriever.storage

    @status
    def create_missing_files(self) -> None:
        """Creates the missing zentra files."""
        self._make_models_dir()
        self._make_config_file()

    @status
    def create_demo_files(self) -> None:
        """Creates a demo folder with files to demonstrate how to create Zentra Pages and Components."""
        make_code_files_from_url(
            url=f"{self.url}/{self.config_storage.demo_dir_path}",
            filenames=self.config_storage.demo_filenames,
            dest_path=self.paths.demo,
        )
