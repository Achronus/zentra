import os

from ..conf.constants import PARTY, PASS, FAIL

from rich.table import Table
from rich.panel import Panel


def path_exists_table(zentra_path: str, folder_exists: str) -> Table:
    """Creates a printable table showing the `zentra_path` and if the `folder` exists."""
    icon = PASS if folder_exists else FAIL

    table = Table()
    table.add_column("Zentra Path", style="bright_cyan", justify="center")
    table.add_column("Exists", justify="center")
    table.add_row(local_path(zentra_path), icon)
    return table


def complete_panel() -> Panel:
    """Creates a printable complete panel."""
    panel = Panel.fit(
        f"\n{PARTY} Components created successfully! {PARTY}",
        height=5,
        border_style="bright_green",
        style="bright_green",
    )
    return panel


def local_path(folder_path: str) -> str:
    """Extracts the last two directories from a `folder_path`."""
    head, tail = os.path.split(folder_path)
    root = os.path.basename(head)
    return "/".join([root, tail])
