import textwrap
import typer

from rich.console import Console
from rich.panel import Panel
from cli.conf.checks import check_zentra_exists

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
from cli.conf.format import plural_name_formatter


MORE_HELP_INFO = f"""
[dark_goldenrod]Need more help?[/dark_goldenrod] 
  Check our [bright_blue][link={ERROR_GUIDE_URL}]Error Message Guide[/link][/bright_blue].

[red]Really stuck?[/red] 
  Report the issue [bright_blue][link={GITHUB_ISSUES_URL}]on GitHub[/link][/bright_blue].
"""

UNKNOWN_ERROR = f"""
{FAIL} 🥴 Well this is awkward... We didn't account for this! 🥴 {FAIL}

You've encountered something unexpected 🤯. Please report this issue on [bright_blue][link={GITHUB_ISSUES_URL}]GitHub[/link][/bright_blue].
"""


MISSING_FILES_CHECKS = """
Things to check:
  1. You are in the [yellow]correct directory[/yellow]
  2. You have [yellow]configured[/yellow] your project with [green]zentra init[/green]  
"""

INVALID_CONFIG_CHECKS = f"""
Access the config file at [magenta]zentra/models/[/magenta][yellow]{ZentaFilepaths.SETUP_FILENAME}[/yellow].

Then, check if:
  1. [magenta]zentra[/magenta] = [yellow]Zentra[/yellow]() is initalised
  2. [magenta]Zentra[/magenta] models are registered with [magenta]zentra[/magenta].[yellow]register[/yellow]() with   
    a list of [magenta]Zentra[/magenta] [yellow]Pages[/yellow] or [yellow]Components[/yellow]

For example:
  [magenta]zentra[/magenta].[yellow]register[/yellow]([cyan][[/cyan][yellow]Page[/yellow](...), [yellow]Page[/yellow](...)[cyan]][/cyan])
  [magenta]zentra[/magenta].[yellow]register[/yellow]([cyan][[/cyan][yellow]Accordion[/yellow](...), [yellow]Button[/yellow](...)[cyan]][/cyan])
  [magenta]zentra[/magenta].[yellow]register[/yellow]([cyan][[/cyan][yellow]Page[/yellow](...), [yellow]Accordion[/yellow](...)[cyan]][/cyan])
"""

VALID_CONFIG_NO_COMPONENTS = f"""
Access the config file at [magenta]zentra/models/[/magenta][yellow]{ZentaFilepaths.SETUP_FILENAME}[/yellow].

Then, check if:
  1. You've [magenta]imported[/magenta] your created models
  2. You've [green]added[/green] them to [magenta]zentra[/magenta].[yellow]register[/yellow]()
"""

IMPORT_ERROR_CHECKS = f"""
Access the config file at [magenta]zentra/models/[/magenta][yellow]{ZentaFilepaths.SETUP_FILENAME}[/yellow].

Then, check if:
  1. You've [magenta]imported[/magenta] your created models
  2. [magenta]from[/magenta] [green]zentra[/green].[green]core[/green] [magenta]import[/magenta] [green]Zentra[/green] - is present
  3. [magenta]zentra[/magenta] = [yellow]Zentra[/yellow]() - is set
"""


def error_msg_with_checks(title: str, checks: str) -> str:
    """Formats error messages that have a title and a list of checks."""
    return textwrap.dedent(f"\n{FAIL} {title} {FAIL}\n") + checks


def success_msg_with_checks(title: str, checks: str) -> str:
    """Formats success messages that have a title and a list of checks."""
    return textwrap.dedent(f"\n{PARTY} {title} {PARTY}\n") + checks


SUCCESS_MSG_MAP = {
    SetupSuccessCodes.CONFIGURED: success_msg_with_checks(
        "Application already configured with components!",
        checks="\nUse [green]zentra generate[/green] to create:",
    ),
}


COMMON_ERROR_MAP = {
    CommonErrorCodes.TEST_ERROR: "Test",
    CommonErrorCodes.CONFIG_MISSING: error_msg_with_checks(
        "[magenta]zentra/models[/magenta] config file missing!",
        checks=MISSING_FILES_CHECKS,
    ),
    CommonErrorCodes.INVALID_CONFIG: error_msg_with_checks(
        "[red]Invalid[/red] config file detected!",
        checks=INVALID_CONFIG_CHECKS,
    ),
    CommonErrorCodes.ZENTRA_MISSING: error_msg_with_checks(
        title="The [magenta]zentra[/magenta] folder is [red]missing[/red]!",
        checks=MISSING_FILES_CHECKS,
    ),
    CommonErrorCodes.MODELS_DIR_MISSING: error_msg_with_checks(
        "[magenta]zentra/models[/magenta] is missing!",
        checks=MISSING_FILES_CHECKS,
    ),
    CommonErrorCodes.SRC_DIR_MISSING: f"""
    {FAIL} [red]Source directory missing[/red]! {FAIL}

    This is a bug, please report this as an issue [bright_blue][link={GITHUB_ISSUES_URL}]on GitHub[/link][/bright_blue].
    """,
}

SETUP_ERROR_MAP = {
    SetupErrorCodes.NO_COMPONENTS: error_msg_with_checks(
        "Config [green]valid[/green] but [red]no components found[/red]!",
        checks=VALID_CONFIG_NO_COMPONENTS,
    ),
    SetupErrorCodes.IMPORT_ERROR: error_msg_with_checks(
        "[red]Cannot[/red] find or access the [magenta]Zentra[/magenta] app!",
        checks=IMPORT_ERROR_CHECKS,
    ),
}

GENERATE_ERROR_MAP = {
    GenerateErrorCodes.NO_COMPONENTS: error_msg_with_checks(
        "[red]No components found[/red] in [green]zentra/models[/green]!",
        checks=INVALID_CONFIG_CHECKS,
    ),
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

    def __msg_with_counts(self, msg: str) -> str:
        """Adds Zentra page and component counts to a message and returns the updated version."""
        zentra = check_zentra_exists()

        page_count = len(zentra.pages)
        component_count = len(zentra.component_names)

        component_str = f"\n  - {page_count} [yellow]{plural_name_formatter('Page', page_count)}[/yellow]\n  - {component_count} [yellow]{plural_name_formatter('Component', component_count)}[/yellow]\n"
        return msg + component_str

    def msg(self, e: typer.Exit) -> None:
        """Assigns a success or error message depending on the code received."""
        try:
            msg = textwrap.dedent(MSG_MAPPER.get(e.exit_code, UNKNOWN_ERROR))
        except AttributeError:
            e.exit_code = CommonErrorCodes.UNKNOWN_ERROR

        msg_type = e.exit_code.__class__.__name__

        if e.exit_code == SetupSuccessCodes.CONFIGURED:
            msg = self.__msg_with_counts(msg)

        panel = (
            self.__error_msg(msg, e)
            if "Error" in msg_type
            else self.__success_msg(msg, e)
        )

        self.console.print(panel)
