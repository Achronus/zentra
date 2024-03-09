from .base import BaseController, PathStorage, status
from cli.conf.create import make_path_dirs
from cli.utils.printables import local_path


class SetupController(BaseController):
    """
    A controller for handling tasks for configuring Zentra.

    Parameters:
    - paths (controllers.base.PathStorage) - a path storage container with filepaths specific to the controller
    """

    def __init__(self, paths: PathStorage) -> None:
        self.paths = paths

        self.highlighted_path = (
            f"[bright_cyan]{local_path(self.paths.models)}[/bright_cyan]"
        )

        tasks = [
            (self.make_path, f"Creating {self.highlighted_path} folder"),
            (
                self.create_demo_component,
                f"Creating demo [cyan]component[/cyan] in {self.highlighted_path}",
            ),
        ]

        super().__init__(tasks)

    @status
    def make_path(self) -> None:
        """Create the folder path."""
        make_path_dirs(self.paths.models)

    @status
    def create_demo_component(self) -> None:
        """Creates a demo component in the Zentra path."""
        pass
