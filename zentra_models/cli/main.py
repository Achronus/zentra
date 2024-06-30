import os
import typer
import warnings

from zentra_models.cli.conf.constants import (
    ZentraLocalFilepaths,
    ZentraGeneratedFilepaths,
    console,
)
from zentra_models.cli.conf.message import MSG_MAPPER, MessageHandler
from zentra_models.cli.conf.storage import GeneratePathStorage
from zentra_models.cli.tasks.setup import Setup
from zentra_models.cli.tasks.generate import Generate


warnings.filterwarnings("ignore", category=SyntaxWarning)


app = typer.Typer(
    help="Configure your project to work with Zentra using 'zentra init' or create your React components with 'zentra build' based on your models in the zentra folder.",
    pretty_exceptions_enable=True,
)


msg_handler = MessageHandler(console, MSG_MAPPER)


@app.command("init")
def init_app() -> None:
    """Perform basic configuration to setup your app to work with Zentra."""
    try:
        setup = Setup()
        setup.init_app()

    except typer.Exit as e:
        msg_handler.msg(e)


@app.command("build")
def generate_components() -> None:
    """Generates all React components based on the models stored in the 'zentra/models' folder."""
    try:
        paths = GeneratePathStorage(
            config=os.path.join(
                ZentraLocalFilepaths.MODELS, ZentraLocalFilepaths.SETUP_FILENAME
            ),
            models=ZentraLocalFilepaths.MODELS,
            components=ZentraGeneratedFilepaths.COMPONENTS,
            templates=ZentraGeneratedFilepaths.ZENTRA,
            lib=ZentraGeneratedFilepaths.LIB,
        )
        generate = Generate(paths)
        generate.init_checks()
        generate.create_components()

    except typer.Exit as e:
        msg_handler.msg(e)
