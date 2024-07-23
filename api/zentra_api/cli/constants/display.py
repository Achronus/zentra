import textwrap

from zentra_api.cli.constants import MAGIC, ROOT_COMMAND

from rich.panel import Panel


def create_panel(text: str, colour: str = "bright_green") -> Panel:
    """A utility function for building panels."""
    return Panel.fit(
        textwrap.dedent(text),
        border_style=colour,
        padding=(0, 4),
    )


def setup_complete_panel() -> Panel:
    """Creates a printable panel after successfully completing the `init` command."""
    return create_panel(f"""
    {MAGIC} [bright_green]Project created successfully![/bright_green] {MAGIC}

    Use [yellow]{ROOT_COMMAND} add[/yellow] to create some [cyan]routes[/cyan]!
    """)
