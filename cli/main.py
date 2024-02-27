import typer
from typing_extensions import Annotated
from rich.console import Console


app = typer.Typer()

console = Console()


@app.command("init")
def init_app() -> None:
    """Perform basic configuration to setup your app to work with Zentra."""
    ...


@app.command("generate")
def generate_components(
    filename: Annotated[
        str,
        typer.Argument(
            help="An optional filename for a set of React components stored in the zentra folder.",
            show_default=True,
        ),
    ] = "all",
) -> None:
    """Generates all React components based on the models stored in the 'zentra' folder. Optionally, takes a single 'filename' as argument to only generate certain components."""
    if filename:
        ...
    else:
        ...


@app.callback()
def callback() -> None:
    """
    Configure your project to work with Zentra using 'zentra init' or create your React components with 'zentra generate' based on your models in the zentra folder.

    Still confused? Use the '--help' flag on each command to gain more information!
    """
    pass
