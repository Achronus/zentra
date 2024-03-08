from .base import BaseController, status
from cli.conf.create import make_path_dirs
from cli.utils.printables import local_path
from cli.conf.constants import ZentaFilepaths


class SetupController(BaseController):
    """A controller for handling tasks for configuring Zentra."""

    def __init__(self) -> None:
        self.folder_path = ZentaFilepaths.MODELS

        self.highlighted_path = (
            f"[bright_cyan]{local_path(self.folder_path)}[/bright_cyan]"
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
        make_path_dirs(self.folder_path)

    @status
    def create_demo_component(self) -> None:
        """Creates a demo component in the Zentra path."""
        pass
