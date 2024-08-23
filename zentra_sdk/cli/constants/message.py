from enum import Enum
import textwrap
import typer

from rich.console import Console
from rich.panel import Panel

from zentra_sdk.cli.constants import (
    DOCKER_URL,
    ERROR_GUIDE_URL,
    FAIL,
    GITHUB_ISSUES_URL,
    MAGIC,
    CommonErrorCodes,
    SetupSuccessCodes,
)


def creation_msg() -> str:
    return f"\n{MAGIC} Creating new [yellow]FastAPI[/yellow] and [green]Next.js[/green] project {MAGIC}\n"


COMPLETE_MSG = """
[yellow]Backend[/yellow] [cyan]Next Steps[/cyan]
    1. Access the [yellow]backend[/yellow] with [dark_goldenrod]cd backend[/dark_goldenrod]
    2. Install the packages and scripts using [dark_goldenrod]poetry install[/dark_goldenrod]
    3. Start programming!

[green]Frontend[/green] [cyan]Next Steps[/cyan]
    1. Access the [green]frontend[/green] with [dark_goldenrod]cd frontend[/dark_goldenrod]
    2. Install the packages using [dark_goldenrod]npm install[/dark_goldenrod] (or equivalent)
    3. Start programming!
"""

MORE_HELP_INFO = f"""
[dark_goldenrod]Need more help?[/dark_goldenrod] 
  Check our [bright_blue][link={ERROR_GUIDE_URL}]Error Message Guide[/link][/bright_blue].

[red]Really stuck?[/red] 
  Report the issue [bright_blue][link={GITHUB_ISSUES_URL}]on GitHub[/link][/bright_blue].
"""

MISSING_PROJECT = """
Have you run [yellow]zentra init[/yellow]?
"""

MISSING_DOCKER = f"""
Have you installed the [link={DOCKER_URL}][cyan]Docker Engine[cyan][/link]?
"""

UNKNOWN_ERROR = f"""
{FAIL} 🥴 Well this is awkward... We didn't account for this! 🥴 {FAIL}

You've encountered something unexpected 🤯. Please report this issue on [bright_blue][link={GITHUB_ISSUES_URL}]GitHub[/link][/bright_blue].
"""


def error_msg_with_checks(title: str, desc: str) -> str:
    """Formats error messages that have a title and a list of checks."""
    return textwrap.dedent(f"\n{FAIL} [bright_red]{title}[/bright_red] {FAIL}\n") + desc


def success_msg_with_checks(title: str, desc: str, icon: str = MAGIC) -> str:
    """Formats success messages that have a title and a list of checks."""
    return (
        textwrap.dedent(f"\n{icon} [bright_green]{title}[/bright_green] {icon}\n")
        + desc
    )


SUCCESS_MSG_MAP = {
    SetupSuccessCodes.TEST_SUCCESS: success_msg_with_checks("Test", desc=""),
    SetupSuccessCodes.COMPLETE: "",
    SetupSuccessCodes.ALREADY_CONFIGURED: "",
}


COMMON_ERROR_MAP = {
    CommonErrorCodes.TEST_ERROR: error_msg_with_checks("Test", desc=""),
    CommonErrorCodes.DOCKER_NOT_INSTALLED: error_msg_with_checks(
        "Docker Engine not found!",
        desc=MISSING_DOCKER,
    ),
    CommonErrorCodes.PROJECT_NOT_FOUND: error_msg_with_checks(
        "Project not found!",
        desc=MISSING_PROJECT,
    ),
}


MSG_MAPPER = {
    **SUCCESS_MSG_MAP,
    **COMMON_ERROR_MAP,
}


class MessageHandler:
    """Handles all the error and success messages for the CLI."""

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
