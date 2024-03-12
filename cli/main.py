import typer

from cli.conf.error import MessageHandler
from cli.tasks.setup import Setup
from cli.tasks.generate import Generate

from rich.console import Console


app = typer.Typer(
    help="Configure your project to work with Zentra using 'zentra init' or create your React components with 'zentra generate' based on your models in the zentra folder."
)

console = Console()
msg_handler = MessageHandler(console)


@app.command("init")
def init_app() -> None:
    """Perform basic configuration to setup your app to work with Zentra."""
    try:
        setup = Setup()
        setup.init_app()

    except typer.Exit as e:
        msg_handler.msg(e)


@app.command("generate")
def generate_components() -> None:
    """Generates all React components based on the models stored in the 'zentra/models' folder."""
    try:
        generate = Generate()
        generate.init_checks()
        generate.components()

    except typer.Exit as e:
        msg_handler.msg(e)
