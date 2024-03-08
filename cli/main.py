import typer

from cli.conf.checks import check_in_correct_folder
from cli.conf.constants import CommonErrorCodes
from cli.conf.error import ErrorHandler
from cli.tasks.setup import Setup
from cli.tasks.generate import Generate

from typing_extensions import Annotated
from rich.console import Console


app = typer.Typer(
    help="Configure your project to work with Zentra using 'zentra init' or create your React components with 'zentra generate' based on your models in the zentra folder."
)

console = Console()
error_handler = ErrorHandler(console)


@app.command("init")
def init_app() -> None:
    """Perform basic configuration to setup your app to work with Zentra."""
    try:
        setup = Setup()
        setup.init_app()

    except typer.Exit as e:
        error_handler.msg(e)


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
    try:
        if not check_in_correct_folder():
            raise typer.Exit(CommonErrorCodes.ZENTRA_MISSING)

        generate = Generate()

        if filename == "all":
            generate.components()
        else:
            pass

    except typer.Exit as e:
        error_handler.msg(e)
