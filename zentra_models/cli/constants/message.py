from enum import Enum
import os
import textwrap
import typer

from rich.console import Console
from rich.panel import Panel


from zentra_models.cli.constants import (
    ERROR_GUIDE_URL,
    GETTING_STARTED_URL,
    GITHUB_ISSUES_URL,
    MAGIC,
    FAIL,
    SETUP_FILE,
    CommonErrorCodes,
    GenerateSuccessCodes,
    SetupErrorCodes,
    GenerateErrorCodes,
    SetupSuccessCodes,
)
from zentra_models.cli.constants.filepaths import LOCAL_PATHS
from zentra_models.cli.local.files import local_path


MODELS_FILEPATH = f"[magenta][link={LOCAL_PATHS.MODELS}]{local_path(LOCAL_PATHS.MODELS)}[/link][/magenta]"
CONFIG_URL = os.path.join(LOCAL_PATHS.MODELS, SETUP_FILE)


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

COMPONENTS_EXIST_MSG = """
[dark_goldenrod]Next Steps[/dark_goldenrod]
  1. [yellow]Move[/yellow] your [magenta]zentra/generated[/magenta] components
  2. Or, [green]add[/green] new ones to [magenta]zentra/models[/magenta]
"""


MISSING_FILES_CHECKS = """
Things to check:
  1. You are in the [yellow]correct directory[/yellow]
  2. You have [yellow]configured[/yellow] your project with [green]zentra init[/green]  
"""

CONFIG_URL_STR = f"[yellow][link={CONFIG_URL}]config[/link][/yellow]"
ACCESS_CONFIG_STR = f"\nAccess the {CONFIG_URL_STR} file.\n"

INVALID_CONFIG_CHECKS = (
    ACCESS_CONFIG_STR
    + """
Then, check if:
  1. You've [magenta]imported[/magenta] your created models
  2. You've [green]added[/green] them to [magenta]zentra[/magenta].[yellow]register[/yellow]()
"""
)

IMPORT_ERROR_CHECKS = (
    ACCESS_CONFIG_STR
    + """
Then:
  1. Check if [magenta]zentra[/magenta] = [yellow]Zentra[/yellow]() - is set
  2. Or, reset the config file with [red]zentra init --reset-config[/red]
"""
)

BUG_MSG = f"""
This is a [yellow]bug[/yellow], please report this as an issue [bright_blue][link={GITHUB_ISSUES_URL}]on GitHub[/link][/bright_blue].
"""

SETUP_COMPLETE_MSG = f"""
[yellow]Next Steps[/yellow]
  1. Create your models in the {MODELS_FILEPATH} folder
  2. Then, add your models to the {CONFIG_URL_STR} file

[dark_goldenrod]Need help?[/dark_goldenrod]
Check our [bright_blue][link={GETTING_STARTED_URL}]Getting Started Guide[/link][/bright_blue]!
"""


def error_msg_with_checks(title: str, checks: str) -> str:
    """Formats error messages that have a title and a list of checks."""
    return textwrap.dedent(f"\n{FAIL} {title} {FAIL}\n") + checks


def success_msg_with_checks(title: str, checks: str, icon: str = MAGIC) -> str:
    """Formats success messages that have a title and a list of checks."""
    return textwrap.dedent(f"\n{icon} {title} {icon}\n") + checks


SUCCESS_MSG_MAP = {
    SetupSuccessCodes.COMPLETE: "",
    SetupSuccessCodes.ALREADY_CONFIGURED: "",
    GenerateSuccessCodes.COMPLETE: "",
    GenerateSuccessCodes.NO_NEW_COMPONENTS: success_msg_with_checks(
        "No new [yellow]Components[/yellow] or [yellow]Pages[/yellow] to add!",
        checks=COMPONENTS_EXIST_MSG,
    ),
}


COMMON_ERROR_MAP = {
    CommonErrorCodes.TEST_ERROR: "Test",
    CommonErrorCodes.REQUEST_FAILED: "",
    CommonErrorCodes.CONFIG_MISSING: error_msg_with_checks(
        f"{MODELS_FILEPATH} [yellow]config[/yellow] file [red]missing[/red]!",
        checks=MISSING_FILES_CHECKS,
    ),
    CommonErrorCodes.INVALID_CONFIG: error_msg_with_checks(
        "[red]Invalid[/red] [yellow]config[/yellow] file [green]detected[/green]!",
        checks=INVALID_CONFIG_CHECKS,
    ),
    CommonErrorCodes.CONFIG_EMPTY: error_msg_with_checks(
        "[yellow]Config[/yellow] file is [red]empty[/red]!",
        checks="\nRun [green]zentra init[/green] to get started!\n",
    ),
    CommonErrorCodes.ZENTRA_MISSING: error_msg_with_checks(
        title="The [magenta]zentra[/magenta] folder is [red]missing[/red]!",
        checks=MISSING_FILES_CHECKS,
    ),
    CommonErrorCodes.MODELS_DIR_MISSING: error_msg_with_checks(
        f"{MODELS_FILEPATH} is missing!",
        checks=MISSING_FILES_CHECKS,
    ),
    CommonErrorCodes.NO_COMPONENTS: error_msg_with_checks(
        "[red]No components found[/red] in [yellow]config[/yellow] file!",
        checks=INVALID_CONFIG_CHECKS,
    ),
}

SETUP_ERROR_MAP = {
    SetupErrorCodes.IMPORT_ERROR: error_msg_with_checks(
        "[red]Cannot[/red] find or access the [magenta]Zentra[/magenta] app!",
        checks=IMPORT_ERROR_CHECKS,
    ),
}

GENERATE_ERROR_MAP = {
    GenerateErrorCodes.GENERATE_DIR_MISSING: error_msg_with_checks(
        title="The [magenta]zentra/generated[/magenta] folder is [red]missing[/red]!",
        checks=BUG_MSG,
    ),
}

MSG_MAPPER = {
    **SUCCESS_MSG_MAP,
    **COMMON_ERROR_MAP,
    **SETUP_ERROR_MAP,
    **GENERATE_ERROR_MAP,
}


class MessageHandler:
    """Handles all the messages for the `zentra-cli`."""

    def __init__(self, console: Console, msg_mapper: dict[Enum, str]) -> None:
        self.console = console
        self.msg_mapper = msg_mapper

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
            if e.exit_code not in self.msg_mapper.keys():
                e.exit_code = CommonErrorCodes.UNKNOWN_ERROR

            msg = textwrap.dedent(self.msg_mapper.get(e.exit_code, UNKNOWN_ERROR))

        except AttributeError:
            e.exit_code = CommonErrorCodes.UNKNOWN_ERROR

        msg_type = e.exit_code.__class__.__name__

        if msg != "":
            panel = (
                self.__error_msg(msg, e)
                if "Error" in msg_type
                else self.__success_msg(msg, e)
            )
            self.console.print(panel)
