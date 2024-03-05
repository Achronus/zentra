import typer

from cli.conf.constants import FAIL, StatusCode, ZentaFilepaths
from cli.conf.extract import get_filenames_in_subdir

from rich.console import Console


console = Console()


def calc_component_count() -> int:
    """Calculates the number of components in the `zentra/models` folder."""
    return 0


def get_zentra_model_filenames() -> list[str]:
    """Returns a list of filenames found in the `zentra/models` folder."""
    return get_filenames_in_subdir(ZentaFilepaths.MODELS)


class Generate:
    """A class for handling the logic for the `zentra generate` command."""

    def __init__(self) -> None:
        pass

    def components(self) -> None:
        """Generates the react components based on the `zentra/models` folder."""
        num_components = calc_component_count()

        if num_components == 0:
            console.print(
                f"\n{FAIL} [red]No components found[/red] in [green]zentra/models[/green]! Need help? Check the [bright_blue][link=#]starter guide[/link][/bright_blue]! {FAIL}\n",
                markup=True,
            )
            typer.Exit(code=StatusCode.NO_COMPONENTS)
        else:
            # generate components
            pass
