import typer
import warnings

from zentra_models.cli.constants import console
from zentra_models.cli.constants.message import MSG_MAPPER, MessageHandler

from zentra_models.cli.commands.setup import Setup
from zentra_models.cli.commands.generate import Generate


warnings.filterwarnings("ignore", category=SyntaxWarning)


init_command = typer.style("zentra init", typer.colors.YELLOW)
generate_command = typer.style("zentra generate", typer.colors.YELLOW)

app = typer.Typer(
    help=f"Configure your project to work with Zentra using {init_command} or create your React components with {generate_command}.",
    pretty_exceptions_enable=True,
)


msg_handler = MessageHandler(console, MSG_MAPPER)


@app.command("init")
def init_app(reset_config: bool = False, force: bool = False) -> None:
    """Perform basic configuration to setup your app to work with Zentra."""
    try:
        setup = Setup()
        setup.init_app(force, reset_config)

    except typer.Exit as e:
        msg_handler.msg(e)


@app.command("generate")
def generate_components() -> None:
    """Generates all React components based on the models stored in the `Zentra` app."""
    try:
        generate = Generate()
        generate.init_checks()
        generate.create_components()

    except typer.Exit as e:
        msg_handler.msg(e)
