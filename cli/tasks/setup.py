import os
import typer

from ..conf.constants import PASS, StatusCode
from ..conf.file_handler import FileHandler

from rich import print


class Setup:
    def __init__(self) -> None:
        self.folder_name = "zentra"
        self.folder_path = os.path.join(os.getcwd(), self.folder_name, "models")

        self.fh = FileHandler(self.folder_path)

        self.zentra_models_exists = self.fh.check_folder_exists()
        self.zentra_models_empty = self.fh.check_folder_empty()

    def __check_for_model(self) -> bool:
        """Helper function to check for component models in the `zentra` folder."""
        pass

    def create_demo_component(self) -> None:
        """Creates an example Zentra component."""
        pass

    def init_app(self) -> None:
        """Performs configuration to initialise application with `zentra`."""
        if self.zentra_models_exists:
            if self.zentra_models_empty:
                self.create_demo_component()
            else:
                if self.fh.check_component_model_exists():
                    print(
                        f"{PASS} Application already configured with components! Use [green]zentra generate[/green] to create them!"
                    )
                    typer.Exit(code=StatusCode.CONFIGURED)
        else:
            os.mkdir(self.folder_path)
