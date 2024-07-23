import textwrap

from zentra_api.cli.conf import ProjectDetails
from zentra_api.cli.constants import MAGIC, ROOT_COMMAND

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


def setup_complete_panel(details: ProjectDetails) -> Panel:
    """Creates a printable panel after successfully completing the `init` command."""
    return create_panel(f"""
    {MAGIC} [bright_green]Project created successfully![/bright_green] {MAGIC}

    Access it here: [dark_goldenrod][link={details.project_path}]{details.project_dir}[/link][/dark_goldenrod]

    Use [yellow]{ROOT_COMMAND} add[/yellow] to create some [cyan]routes[/cyan]!
    """)
