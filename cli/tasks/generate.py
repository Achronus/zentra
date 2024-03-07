import typer

from cli.conf.constants import FAIL, StatusCode

from rich.console import Console


console = Console()


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
            console.print(
                f"\n{FAIL} [red]No components found[/red] in [green]zentra/models[/green]! [magenta]Need help?[/magenta] Check the [bright_blue][link=#]starter guide[/link][/bright_blue]! {FAIL}\n"
            )
            typer.Exit(code=StatusCode.NO_COMPONENTS)
        else:
            # generate components
            pass
