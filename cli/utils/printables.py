from enum import Enum
import textwrap

from cli.conf.constants import MAGIC
from cli.conf.checks import check_zentra_exists
from cli.conf.format import set_colour, name_to_plural
from cli.conf.storage import BasicNameStorage, ModelStorage

from pydantic import BaseModel
from rich.panel import Panel

from cli.conf.types import FolderFilePair


class Action(Enum):
    ADD = ("+", "green")
    REMOVE = ("-", "red")


class PanelFormatter(BaseModel):
    """Handles the logic for creating complete panels.

    Parameters:
    - storage (storage.BasicNameStorage | storage.ModelStorage) - the storage container with Zentra model names
    - action (Enum.Action) - an Action Enum value to indicate an addition or subtraction string
    """

    storage: BasicNameStorage | ModelStorage
    action: Action

    def title_str_with_count(
        self,
        name: str,
        title_colour: str,
        count: int,
    ) -> str:
        """Creates a title string for a set of models with the number of items at the front."""
        count_str = set_colour(count, self.action.value[1])
        formatted_name = set_colour(
            name_to_plural(name.capitalize(), count),
            title_colour,
        )
        return f"{count_str} {formatted_name}"

    def page_str(self, count: int) -> str:
        """Creates a page string for the panel."""
        return self.format_item("page", count)

    def component_str(self, count: int) -> str:
        """Creates a component string for the panel."""
        return self.format_item("component", count)

    def change_str(self, data: dict) -> str:
        """Creates a modification string based on the provided data with 'added' and 'removed' items for the panel."""
        change_str = ""
        for size, formatter in data:
            if size > 0:
                change_str += formatter(size)

        if change_str != "":
            heading_str = f"{set_colour(heading, colour=self.action.value[1])}\n"
            change_str = heading_str + change_str

        return change_str

    def list_to_str(
        self, items: list[str], items_per_line: int = 6, items_coloured: bool = False
    ) -> str:
        """Converts a list of `items` into a single readable string separated by commas. Items are passed onto new lines `items_per_line` is reached."""
        symbol, colour = self.action.value
        symbol = set_colour(symbol, colour)
        combined_string = f"  {symbol} "

        if len(items) > 0:
            # Split items equally across lines up to desired value
            num_lines = -(-len(items) // items_per_line)
            items_per_line = -(-len(items) // num_lines)

            for i, item in enumerate(items):
                start_newline = (i + 1) % items_per_line == 0 and len(items) != 1
                combined_string += set_colour(item, colour) if items_coloured else item
                combined_string += f"\n  {symbol} " if start_newline else ", "

            return combined_string.rstrip(", ")
        return ""


def setup_complete_panel() -> Panel:
    """Creates a printable panel after successfully completing `zentra init`."""
    zentra = check_zentra_exists()
    storage = zentra.names
    add_formatter = PanelFormatter(storage=storage, action=Action.ADD)

    component_str = add_formatter.list_to_str(storage.components)
    page_str = add_formatter.list_to_str(storage.pages)

    component_title = add_formatter.title_str_with_count(
        "component", "yellow", len(storage.components)
    )
    page_title = add_formatter.title_str_with_count(
        "page", "dark_goldenrod", len(storage.pages)
    )

    return Panel.fit(
        textwrap.dedent(f"""
    {MAGIC} [magenta]Zentra[/magenta] configured successfully! {MAGIC}

    Use [green]zentra generate[/green] to create your models.

    [bright_cyan]Models To Generate[/bright_cyan]
    """)
        + f"{component_title}\n{component_str}\n\n"
        + f"{page_title}\n{page_str}",
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
    
    """)
        + add_str
        + del_str,
        border_style="bright_green",
    )
