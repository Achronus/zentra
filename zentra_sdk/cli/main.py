import typer

from zentra_sdk.cli.constants import console
from zentra_sdk.cli.constants.message import MSG_MAPPER, MessageHandler
from zentra_sdk.cli.commands.setup import Setup

init_command = typer.style("zentra init", typer.colors.YELLOW)

app = typer.Typer(
    help=f"Welcome to Zentra! To get started, create a project with {init_command}.",
    rich_markup_mode="rich",
    pretty_exceptions_enable=True,
)

msg_handler = MessageHandler(console, MSG_MAPPER)


@app.command("init")
def init() -> None:
    """Creates a new FastAPI and Next.js project in a current directory."""
    try:
        setup = Setup()
        setup.build()

    except typer.Exit as e:
        msg_handler.msg(e)


@app.command("build")
def build() -> None:
    """Creates a production ready version of the project."""
    pass
