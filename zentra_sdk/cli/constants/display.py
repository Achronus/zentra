import textwrap

from zentra_sdk.cli.constants import MAGIC
from zentra_sdk.cli.constants.message import COMPLETE_MSG

from rich.panel import Panel


def create_panel(
    text: str,
    colour: str = "bright_green",
    padding: tuple[int, int] = (0, 4),
) -> Panel:
    """A utility function for building panels."""
    return Panel.fit(
        textwrap.dedent(text),
        border_style=colour,
        padding=padding,
    )


def success_panel(title: str, desc: str) -> Panel:
    return create_panel(f"""
    {MAGIC} [bright_green]{title}[/bright_green] {MAGIC}
    {desc}""")


def setup_complete_panel() -> Panel:
    """Creates a printable panel after successfully completing the `init` command."""
    return success_panel("Project created successfully!", COMPLETE_MSG)


def already_configured_panel() -> Panel:
    """Creates a printable panel for the `init` command if the project already exists."""
    return success_panel("Project already exists!", COMPLETE_MSG)
