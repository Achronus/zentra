import textwrap
from enum import Enum

from cli.conf.constants import MAGIC
from cli.conf.checks import check_zentra_exists
from cli.conf.format import set_colour, name_to_plural
from cli.conf.storage import BasicNameStorage, ModelStorage

from pydantic import BaseModel
from rich.panel import Panel

from cli.conf.types import ChangeStrData


class Action(Enum):
    ADD = ("+", "green")
    REMOVE = ("-", "red")


class PanelFormatter(BaseModel):
    """Handles the logic for creating complete panels.

    Parameters:
    - storage (storage.BasicNameStorage) - the storage container with Zentra model names
    - action (Enum.Action) - an Action Enum value to indicate an addition or subtraction string
    """

    storage: BasicNameStorage
    action: Action

    def format_item(self, name: str, count: int) -> str:
        """Creates an item string for the panel."""
        formatted_symbol = set_colour(self.action.value[0], self.action.value[1])
        formatted_name = set_colour(name_to_plural(name.capitalize(), count), "yellow")
        return f"{formatted_symbol} {count} {formatted_name}"

    def page_str(self, count: int) -> str:
        """Creates a page string for the panel."""
        return self.format_item("page", count)

    def component_str(self, count: int) -> str:
        """Creates a component string for the panel."""
        return self.format_item("component", count)

    def change_str(self, data: ChangeStrData, heading: str) -> str:
        """Creates a modification string based on the provided data with 'added' and 'removed' items for the panel."""
        change_str = ""
        for size, formatter in data:
            if size > 0:
                change_str += formatter(size)

        if change_str != "":
            heading_str = (
                f"[{self.action.value[1]}]{heading}[/{self.action.value[1]}]\n"
            )
            change_str = heading_str + change_str

        return change_str


def setup_complete_panel() -> Panel:
    """Creates a printable panel after successfully completing `zentra init`."""
    zentra = check_zentra_exists()
    storage = zentra.names
    add_formatter = PanelFormatter(storage=storage, action=Action.ADD)

    return Panel.fit(
        textwrap.dedent(f"""
    {MAGIC} [magenta]Zentra[/magenta] configured successfully! {MAGIC}

    Use [green]zentra generate[/green] to create your models.

    [bright_cyan]Models To Convert[/bright_cyan]
    {add_formatter.component_str(storage.components)}
    {add_formatter.page_str(storage.pages)}
    """),
        border_style="bright_green",
    )


def generate_complete_panel(storage: ModelStorage) -> Panel:
    """Creates a printable panel after successfully completing `zentra generate`."""
    add_formatter = PanelFormatter(storage=storage, action=Action.ADD)
    del_formatter = PanelFormatter(storage=storage, action=Action.REMOVE)

    add_data = [
        (storage.component_generate_count, add_formatter.component_str),
        (len(storage.pages_to_generate), add_formatter.page_str),
    ]

    del_data = [
        (storage.component_remove_count, del_formatter.component_str),
        (len(storage.pages_to_remove), del_formatter.page_str),
    ]

    add_str = add_formatter.change_str(add_data, "Added")
    del_str = del_formatter.change_str(del_data, "Removed")

    del_str = f"\n\n{del_str}" if (add_str != "" and del_str != "") else del_str

    return Panel.fit(
        textwrap.dedent(f"""
    {MAGIC} [magenta]Zentra[/magenta] → [bright_cyan]React[/bright_cyan] conversion successful! {MAGIC}
    
    Access them in [magenta]zentra/generated[/magenta].
    {storage.uploadthing_file_count}
    """)
        + add_str
        + del_str,
        border_style="bright_green",
    )
