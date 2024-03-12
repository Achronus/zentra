from cli.conf.message import COMPONENTS_EXIST_MSG
from cli.conf.format import component_count_str

from zentra.core import Zentra

from ..conf.constants import (
    PARTY,
    MAGIC,
)

from rich.panel import Panel


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
    """Creates a printable panel for successful component completion."""
    panel = Panel.fit(
        f"\n{PARTY} Created Successfully! {PARTY}\n{COMPONENTS_EXIST_MSG}",
        border_style="bright_green",
    )
    return panel
