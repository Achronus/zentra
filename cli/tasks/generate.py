import os
import typer

from cli.conf.constants import (
    GenerateErrorCodes,
    LocalUIComponentFilepaths,
    ZentaFilepaths,
    ZentraUIFilepaths,
)
from cli.tasks.controllers.base import PathStorage
from cli.tasks.controllers.generate import GenerateController
from cli.utils.printables import component_count_panel
from zentra.core import Zentra

from rich.console import Console

console = Console()


class Generate:
    """A class for handling the logic for the `zentra generate` command."""

    def __init__(self, zentra: Zentra) -> None:
        self.zentra = zentra
        self.paths = PathStorage(
            config=os.path.join(ZentaFilepaths.MODELS, ZentaFilepaths.SETUP_FILENAME),
            models=ZentaFilepaths.MODELS,
            local_ui_base=LocalUIComponentFilepaths.BASE,
            generated_ui_base=ZentraUIFilepaths.BASE,
        )

    def components(self) -> None:
        """Generates the react components based on the `zentra/models` folder."""

        if len(self.zentra.component_names) == 0:
            raise typer.Exit(code=GenerateErrorCodes.NO_COMPONENTS)

        console.print(component_count_panel(self.zentra, text_start="Generating "))

        controller = GenerateController(self.zentra, self.paths)
        controller.run()
