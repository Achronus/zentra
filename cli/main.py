import os
import typer

from cli.conf.constants import FAIL, StatusCode
from .tasks.setup import Setup
from .tasks.generate import Generate

from typing_extensions import Annotated
from rich.console import Console


app = typer.Typer()

console = Console()


def check_in_correct_folder() -> bool:
    """Checks if the user is in the correct folder before using the tool."""
    current_directory = os.getcwd()
    zentra_folder_path = os.path.join(current_directory, "zentra")

    if os.path.exists(zentra_folder_path) and os.path.isdir(zentra_folder_path):
        return True

    return False


@app.command("init")
def init_app() -> None:
    """Perform basic configuration to setup your app to work with Zentra."""
    setup = Setup()
    setup.init_app()


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
    """Generates all React components based on the models stored in the 'zentra/models' folder. Optionally, supply a single 'filename' as argument to only generate certain components."""
    if not check_in_correct_folder():
        console.print(
            f"\n{FAIL} The [magenta]zentra[/magenta] folder is [red]missing[/red]! Are you in the [yellow]correct directory(?)[/yellow] and have you [yellow]configured[/yellow] your project with [green]zentra init[/green]? {FAIL}\n"
        )
        typer.Exit(StatusCode.FAIL)

    generate = Generate()

    if filename == "all":
        generate.components()
    else:
        pass


@app.callback()
def callback() -> None:
    """
    Configure your project to work with Zentra using 'zentra init' or create your React components with 'zentra generate' based on your models in the zentra folder.

    Still confused? Use the '--help' flag on each command to gain more information!
    """
    pass
