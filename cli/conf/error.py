import textwrap
import typer

from rich.console import Console
from rich.panel import Panel

from cli.conf.constants import (
    ERROR_GUIDE_URL,
    GITHUB_ISSUES_URL,
    CommonErrorCodes,
    SetupErrorCodes,
    GenerateErrorCodes,
    PARTY,
    FAIL,
    SetupSuccessCodes,
    ZentaFilepaths,
)


MORE_HELP_INFO = f"""
[dark_goldenrod]Need more help?[/dark_goldenrod] 
  Check our [bright_blue][link={ERROR_GUIDE_URL}]Error Message Guide[/link][/bright_blue].

[red]Really stuck?[/red] 
  Report the issue [bright_blue][link={GITHUB_ISSUES_URL}]on GitHub[/link][/bright_blue].
"""

UNKNOWN_ERROR = f"""
{FAIL} 🥴 Well this is awkward... We didn't account for this! 🥴 {FAIL}

You've encountered something unexpected 🤯. Please report this issue on [bright_blue][link={GITHUB_ISSUES_URL}]on GitHub[/link][/bright_blue].
"""


MISSING_FILES_CHECKS = """
Things to check:
  1. You are in the [yellow]correct directory[/yellow]
  2. You have [yellow]configured[/yellow] your project with [green]zentra init[/green]
"""

INVALID_CONFIG_CHECKS = f"""
Access the file at [magenta]zentra/models/{ZentaFilepaths.SETUP_FILENAME}[/magenta].

Then, check if:
  1. [magenta]zentra = Zentra()[/magenta] is initalised
  2. Zentra models are registered with [magenta]zentra.register()[/magenta] and has a list of Zentra pages or components inside it
"""


def msg_with_checks(title: str, checks: str) -> str:
    """Formats messages that have a title and a list of checks."""
    return textwrap.dedent(title) + checks


SUCCESS_MSG_MAP = {
    SetupSuccessCodes.INIT_SUCCESS: f"\n{PARTY} Application successfully configured! Refer to the demo files in [magenta]zentra/models[/magenta] to get started. {PARTY}\n",
    SetupSuccessCodes.CONFIGURED: f"\n{PARTY} Application already configured with components! Use [green]zentra generate[/green] to create them! {PARTY}\n",
}


COMMON_ERROR_MAP = {
    CommonErrorCodes.CONFIG_MISSING: msg_with_checks(
        f"\n{FAIL} [magenta]zentra/models[/magenta] config file missing! {FAIL}\n",
        checks=MISSING_FILES_CHECKS,
    ),
    CommonErrorCodes.INVALID_CONFIG: msg_with_checks(
        f"\n{FAIL} Oops! [magenta]zentra/models[/magenta] is configured incorrectly! {FAIL}\n",
        checks=INVALID_CONFIG_CHECKS,
    ),
    CommonErrorCodes.ZENTRA_MISSING: msg_with_checks(
        title=f"\n{FAIL} The [magenta]zentra[/magenta] folder is [red]missing[/red]! {FAIL}\n",
        checks=MISSING_FILES_CHECKS,
    ),
    CommonErrorCodes.MODELS_DIR_MISSING: msg_with_checks(
        f"\n{FAIL} [magenta]zentra/models[/magenta] is missing! {FAIL}\n",
        checks=MISSING_FILES_CHECKS,
    ),
    CommonErrorCodes.SRC_DIR_MISSING: f"""
    {FAIL} [red]Source directory missing[/red]! {FAIL}

    This is a bug, please report this as an issue [bright_blue][link={GITHUB_ISSUES_URL}]on GitHub[/link][/bright_blue].
    """,
    CommonErrorCodes.DEST_DIR_MISSING: msg_with_checks(
        title=f"\n{FAIL} Oops! Looks like you are [red]missing files[/red] in the [magenta]zentra[/magenta] folder! {FAIL}\n",
        checks=MISSING_FILES_CHECKS,
    ),
}

SETUP_ERROR_MAP = {}

GENERATE_ERROR_MAP = {
    # TODO: update URL
    GenerateErrorCodes.NO_COMPONENTS: f"""
    {FAIL} [red]No components found[/red] in [green]zentra/models[/green]! {FAIL}

    Things to check:
      1. [green]zentra/models/{ZentaFilepaths.SETUP_FILENAME}[/green] exists
      2. [magenta]page_map = [][/magenta] has pages
      3. [magenta]standalone_components = [][/magenta] has components
      4. [yellow]zentra.register(page_map)[/yellow] exists
      5. [yellow]zentra.register(standalone_components)[/yellow] exist

    Note: only one of [magenta]page_map[/magenta] and [magenta]standalone_components[/magenta] need to have items.
    """,
}

MSG_MAPPER = {
    **SUCCESS_MSG_MAP,
    **COMMON_ERROR_MAP,
    **SETUP_ERROR_MAP,
    **GENERATE_ERROR_MAP,
}


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
