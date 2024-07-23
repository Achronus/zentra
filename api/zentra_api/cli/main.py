from typing import Annotated
import typer

from zentra_api.cli.commands.setup import Setup
from zentra_api.cli.constants import console
from zentra_api.cli.constants.enums import AddItem, DefaultFolderOptions
from zentra_api.cli.constants.message import MSG_MAPPER, MessageHandler


init_command = typer.style("init", typer.colors.YELLOW)
add_command = typer.style("add", typer.colors.YELLOW)

app = typer.Typer(
    help=f"Welcome to Zentra API! Create a project with {init_command} or add something with {add_command}.",
    rich_markup_mode="rich",
    pretty_exceptions_enable=True,
)

msg_handler = MessageHandler(console, MSG_MAPPER)


@app.command("init")
def init(
    project_name: Annotated[
        str,
        typer.Argument(
            help="The name of the FastAPI project to create",
            show_default=False,
        ),
    ],
) -> None:
    """Creates a new FastAPI project in a folder called <PROJECT_NAME>."""
    try:
        setup = Setup(project_name, console)
        setup.build()

    except typer.Exit as e:
        msg_handler.msg(e)


@app.command("add")
def add(
    item: Annotated[
        AddItem,
        typer.Argument(
            help="The type of item to add.",
            show_default=False,
        ),
    ],
    folder: Annotated[
        str,
        typer.Option(
            help="The folder to add the item to. E.g., 'auth'. When <item='route'>, defaults to 'api'. When <item='test'> defaults to 'tests'.",
            show_default=False,
        ),
    ] = None,
) -> None:
    """Adds a new <ITEM> into the project in <FOLDER> with <NAME>."""
    try:
        if not folder:
            folder = getattr(DefaultFolderOptions, item.upper())

        print(folder)

    except typer.Exit as e:
        msg_handler.msg(e)


if __name__ == "__main__":
    app()
