from cli.utils.printables import local_path
from cli.conf.constants import ZENTRA_MODELS_PATH
from cli.conf.file_handler import FileHandler
from .base import BaseController


class FolderDoesNotExistController(BaseController):
    """A controller for handling tasks when the Zentra path does not exist."""

    def __init__(self) -> None:
        self.folder_path = ZENTRA_MODELS_PATH
        self.fh = FileHandler(self.folder_path)

        self.highlighted_path = (
            f"[bright_cyan]{local_path(self.folder_path)}[/bright_cyan]"
        )

        tasks = [
            (self.make_path, f"Creating {self.highlighted_path} folder"),
            (
                self.create_demo_component,
                "Creating demo [bright_blue]component[/bright_blue]",
            ),
        ]

        super().__init__(tasks)

    def make_path(self) -> None:
        """Create the folder path."""
        self.fh.make_path_dirs()

    def create_demo_component(self) -> None:
        """Creates a demo component in the Zentra path."""
        pass
