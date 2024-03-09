import typer

from cli.conf.checks import check_folder_exists
from cli.conf.constants import CommonErrorCodes, ZentaFilepaths
from cli.conf.error import MessageHandler
from cli.tasks.setup import Setup
from cli.tasks.generate import Generate

from typing_extensions import Annotated
from rich.console import Console

from zentra.models import zentra


app = typer.Typer(
    help="Configure your project to work with Zentra using 'zentra init' or create your React components with 'zentra generate' based on your models in the zentra folder."
)

console = Console()
msg_handler = MessageHandler(console)


@app.command("init")
def init_app() -> None:
    """Perform basic configuration to setup your app to work with Zentra."""
    try:
        setup = Setup(zentra)
        setup.init_app()

    except typer.Exit as e:
        msg_handler.msg(e)


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
        # Check cwd has access to zentra
        if not check_folder_exists(ZentaFilepaths.ROOT):
            raise typer.Exit(CommonErrorCodes.ZENTRA_MISSING)

        generate = Generate(zentra)

        if filename == "all":
            generate.components()
        else:
            pass

    except typer.Exit as e:
        msg_handler.msg(e)
