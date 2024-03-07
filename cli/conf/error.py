import typer

from rich.console import Console

from cli.conf.constants import StatusCode, PARTY, FAIL

ERROR_MSG_MAPPER = {
    StatusCode.INIT_SUCCESS: f"\n{PARTY} Application successfully configured! Refer to the demo files in [magenta]zentra/models[/magenta] to get started. {PARTY}\n",
    StatusCode.CONFIGURED: f"\n{PARTY} Application already configured with components! Use [green]zentra generate[/green] to create them! {PARTY}\n",
    StatusCode.ZENTRA_MISSING: f"\n{FAIL} The [magenta]zentra[/magenta] folder is [red]missing[/red]! Are you in the [yellow]correct directory(?)[/yellow] and have you [yellow]configured[/yellow] your project with [green]zentra init[/green]? {FAIL}\n",
    # TODO: update URL
    StatusCode.NO_COMPONENTS: f"\n{FAIL} [red]No components found[/red] in [green]zentra/models[/green]! [magenta]Need help?[/magenta] Check the [bright_blue][link=#]starter guide[/link][/bright_blue]! {FAIL}\n",
    StatusCode.SRC_DIR_MISSING: f"\n{FAIL} [red]Source directory missing[/red]! This is a bug, please log this as an issue [bright_blue][link=https://github.com/Astrum-AI/Zentra/issues]on GitHub[/link][/bright_blue]. {FAIL}\n",
    StatusCode.DEST_DIR_MISSING: f"\n{FAIL} Oops! Looks like you are [red]missing files[/red] in the [magenta]zentra[/magenta] folder! Are you in the [yellow]correct directory(?)[/yellow] and have you [yellow]configured[/yellow] your project with [green]zentra init[/green]? {FAIL}\n",
}


class ErrorHandler:
    """Handles all the errors of the CLI."""

    def __init__(self, console: Console) -> None:
        self.console = console

    def msg(self, e: typer.Exit):
        msg = ERROR_MSG_MAPPER.get(e.exit_code, "Unknown error.")
        self.console.print(msg)