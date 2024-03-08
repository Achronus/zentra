import typer

from cli.conf.constants import GenerateErrorCodes
from cli.tasks.controllers.generate import GenerateController
from zentra.core import Zentra


def calc_component_count() -> int:
    """Calculates the number of components in the `zentra/models` folder."""
    return 0


class Generate:
    """A class for handling the logic for the `zentra generate` command."""

    def __init__(self, zentra: Zentra) -> None:
        self.zentra = zentra

    def components(self) -> None:
        """Generates the react components based on the `zentra/models` folder."""
        num_components = calc_component_count()

        if num_components == 0:
            raise typer.Exit(code=GenerateErrorCodes.NO_COMPONENTS)
        else:
            controller = GenerateController(self.zentra)
            controller.run()
