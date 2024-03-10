import os
from cli.conf.format import component_count_str

from zentra.core import Zentra

from ..conf.constants import PARTY, PASS, FAIL, MAGIC

from rich.table import Table
from rich.panel import Panel


def set_icon(exists: bool) -> str:
    """A helper function for setting the correct icon for tables."""
    return PASS if exists else FAIL


def path_exists_table(zentra_path: str, folder_exists: bool) -> Table:
    """Creates a printable table showing the `zentra_path` and if the `folder` exists."""
    icon = set_icon(folder_exists)

    table = Table()
    table.add_column("Zentra Path", style="bright_cyan", justify="center")
    table.add_column("Exists", justify="center")
    table.add_row(local_path(zentra_path), icon)
    return table


def configuration_complete_panel(folder_path: str, link: str) -> Panel:
    """Creates a printable panel related to configuration success."""
    panel = Panel.fit(
        f"\nCreate your models in the [magenta]{local_path(folder_path)}[/magenta] folder!\n\n[dark_goldenrod]Need help?[/dark_goldenrod]\nCheck our [bright_blue][link={link}]Getting Started Guide[/link][/bright_blue]!\n",
        title=f"{PARTY} Application configured! {PARTY}",
        border_style="bright_green",
    )
    return panel


def component_count_panel(
    zentra: Zentra, text_start: str = "", text_end: str = ""
) -> Panel:
    """Creates a printable panel highlighting the number of components and pages in the Zentra app with a custom message."""
    return Panel(
        f"{MAGIC} {text_start}{component_count_str(zentra)}{text_end} {MAGIC}",
        expand=False,
        border_style="green",
    )


def component_complete_panel() -> Panel:
    """Creates a printable complete panel related to component creation."""
    panel = Panel.fit(
        f"\n{PARTY} Components created successfully! {PARTY}",
        border_style="bright_green",
        style="bright_green",
    )
    return panel


def local_path(folder_path: str) -> str:
    """Extracts the last two directories from a `folder_path`."""
    head, tail = os.path.split(folder_path)
    root = os.path.basename(head)
    return "/".join([root, tail])
