import typer

from rich.console import Console
from rich.panel import Panel

from cli.conf.constants import (
    CommonErrorCodes,
    SetupErrorCodes,
    GenerateErrorCodes,
    PARTY,
    FAIL,
)

COMMON_ERROR_MAP = {
    CommonErrorCodes.CONFIG_MISSING: f"CONFIG FILE MISSING!",
    CommonErrorCodes.INVALID_CONFIG: f"INVALID CONFIG FILE!",
    CommonErrorCodes.ZENTRA_MISSING: f"\n{FAIL} The [magenta]zentra[/magenta] folder is [red]missing[/red]! Are you in the [yellow]correct directory(?)[/yellow] and have you [yellow]configured[/yellow] your project with [green]zentra init[/green]? {FAIL}\n",
    CommonErrorCodes.MODELS_DIR_MISSING: f"MODELS DIR MISSING!",
    CommonErrorCodes.SRC_DIR_MISSING: f"\n{FAIL} [red]Source directory missing[/red]! This is a bug, please log this as an issue [bright_blue][link=https://github.com/Astrum-AI/Zentra/issues]on GitHub[/link][/bright_blue]. {FAIL}\n",
    CommonErrorCodes.DEST_DIR_MISSING: f"""
    {FAIL} Oops! Looks like you are [red]missing files[/red] in the [magenta]zentra[/magenta] folder! {FAIL} 
    
    Things to check:
      1. You are in the [yellow]correct directory[/yellow]
      2.You have [yellow]configured[/yellow] your project with [green]zentra init[/green]
    """,
}

SETUP_ERROR_MAP = {
    SetupErrorCodes.INIT_SUCCESS: f"\n{PARTY} Application successfully configured! Refer to the demo files in [magenta]zentra/models[/magenta] to get started. {PARTY}\n",
    SetupErrorCodes.CONFIGURED: f"\n{PARTY} Application already configured with components! Use [green]zentra generate[/green] to create them! {PARTY}\n",
}

GENERATE_ERROR_MAP = {
    # TODO: update URL
    GenerateErrorCodes.NO_COMPONENTS: f"\n{FAIL} [red]No components found[/red] in [green]zentra/models[/green]! [magenta]Need help?[/magenta] Check the [bright_blue][link=#]starter guide[/link][/bright_blue]! {FAIL}\n",
}

ERROR_MSG_MAPPER = {**COMMON_ERROR_MAP, **SETUP_ERROR_MAP, **GENERATE_ERROR_MAP}


class MessageHandler:
    """Handles all the messages of the CLI."""

    def __init__(self, console: Console) -> None:
        self.console = console

    @staticmethod
    def __error_msg(msg: str, e: typer.Exit) -> Panel:
        """Handles error messages and returns a panel with their information."""
        err_str = "[cyan]Error code[/cyan]"
        error_code = f"\n{err_str}: {e.exit_code.value}\n"

        return Panel(
            msg + MORE_HELP_INFO + error_code,
            expand=False,
            border_style="bright_red",
        )

    @staticmethod
    def __success_msg(msg: str, e: typer.Exit) -> Panel:
        """Handles success messages and returns a panel with their information."""
        return Panel(msg, expand=False, border_style="bright_green")

    def msg(self, e: typer.Exit) -> None:
        """Assigns a success or error message depending on the code received."""
        try:
            e.exit_code.value
        except AttributeError:
            e.exit_code = CommonErrorCodes.UNKNOWN_ERROR

        msg = textwrap.dedent(MSG_MAPPER.get(e.exit_code, UNKNOWN_ERROR))
        msg_type = e.exit_code.__class__.__name__

        panel = (
            self.__error_msg(msg, e)
            if "Error" in msg_type
            else self.__success_msg(msg, e)
        )

        self.console.print(panel)
