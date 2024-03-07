import typer

from cli.conf.constants import StatusCode
from cli.tasks.controllers.generate import GenerateController
from zentra.models import zentra


def calc_component_count() -> int:
    """Calculates the number of components in the `zentra/models` folder."""
    return 0


class Generate:
    """A class for handling the logic for the `zentra generate` command."""

    def __init__(self) -> None:
        pass

    def components(self) -> None:
        """Generates the react components based on the `zentra/models` folder."""
        num_components = calc_component_count()

        if num_components == 0:
            raise typer.Exit(code=StatusCode.NO_COMPONENTS)
        else:
            controller = GenerateController(zentra=zentra)
            controller.run()
