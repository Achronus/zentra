from cli.conf.storage import ConfigExistStorage, PathStorage
from cli.tasks.controllers.base import BaseController, status
from cli.conf.create import make_path_dirs
from cli.utils.printables import local_path


class SetupController(BaseController):
    """
    A controller for handling tasks for configuring Zentra.

    Parameters:
    - paths (storage.PathStorage) - a path storage container with filepaths specific to the controller
    - config_storage (storage.ConfigExistStorage) - a boolean value storage container for config checks
    """

    def __init__(self, paths: PathStorage, config_storage: ConfigExistStorage) -> None:
        self.paths = paths
        self.config_storage = config_storage

        self.highlighted_path = f"[magenta]{local_path(self.paths.demo)}[/magenta]"

        tasks = [
            (
                self.create_missing_files,
                "Creating [yellow]configuration[/yellow] files",
            ),
            (
                self.create_demo_files,
                f"Creating demo files in {self.highlighted_path}",
            ),
        ]

        super().__init__(tasks)

    @status
    def create_missing_files(self) -> None:
        """Creates the missing zentra files."""
        # make_path_dirs(self.paths.models)

    @status
    def create_demo_files(self) -> None:
        """Creates a demo folder with files to demonstrate how to use create Zentra Pages and Components."""
        pass
