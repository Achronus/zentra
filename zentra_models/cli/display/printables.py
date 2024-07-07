from enum import Enum
from functools import partial
import textwrap

from zentra_models.cli.constants import GENERATE_DIR, MAGIC
from zentra_models.cli.local.storage import CountStorage
from zentra_models.cli.utils.format import list_to_str, set_colour, name_to_plural
from zentra_models.cli.constants.message import SETUP_COMPLETE_MSG

from pydantic import BaseModel
from rich.panel import Panel

from zentra_models.core import Zentra


# (list[items_to_add], list[items_to_remove])
GenerateDataTuple = tuple[list[str], list[str]]


class Action(Enum):
    ADD = ("+", "green")
    REMOVE = ("-", "red")


class Details(BaseModel):
    """A model for storing panel details."""

    title: str
    desc: str


class SetupPanelFormatter(BaseModel):
    """Handles the logic for creating completion panels for `zentra init`.

    Parameters:
    - `action` (`Enum.Action`) - a single Action Enum item to indicate an addition or subtraction string
    """

    action: Action

    def title_str(
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


class GeneratePanelFormatter(BaseModel):
    """Handles the logic for creating completion panels for `zentra generate`.

    Parameters:
    - `name` (`str`) - a name to associate the formatter used in the title string (e.g., 'component' or 'page')
    - `actions` (`Enum.Action`) - an Action Enum class with an addition and subtraction value
    - `data` (`GenerateDataTuple`) - a tuple containing two `lists` of item information: `(list[items_to_add], list[items_to_remove])`
    """

    name: str
    actions: type[Action]
    data: GenerateDataTuple

    def data_str(self) -> str:
        """Creates a detailed string of information."""
        data_str = ""
        for item, action in zip(self.data, self.actions):
            data_str += f"{list_to_str(item, action)}\n"
        return data_str.rstrip()

    def title_str(self, counts: tuple[int, int], colour: str) -> str:
        """Creates a title string with the item name and its data counts."""
        count_str = ""
        headings = ("Added", "Removed")
        for count, heading, action in zip(counts, headings, self.actions):
            head_str = f"{count} {heading}"
            count_str += f"{set_colour(head_str, action.value[1])}, "

        formatted_name = set_colour(
            name_to_plural(self.name.capitalize(), sum(counts)),
            colour,
        )
        return f"{formatted_name} ({count_str.rstrip(', ')})"


def setup_first_run_panel() -> Panel:
    """Creates a printable panel after successfully running `zentra init` for the first time."""
    return Panel.fit(
        textwrap.dedent(f"""
    {MAGIC} [magenta]Zentra[/magenta] configured successfully! {MAGIC}
    """)
        + SETUP_COMPLETE_MSG,
        border_style="bright_green",
    )


def setup_complete_panel(zentra: Zentra) -> Panel:
    """Creates a printable panel after successfully completing `zentra init`."""
    file_names, block_names, component_names = zentra.storage.get_names()
    add_formatter = SetupPanelFormatter(action=Action.ADD)

    component = Details(
        title=add_formatter.title_str("component", "yellow", len(component_names)),
        desc=list_to_str(component_names, action=Action.ADD),
    )
    block = Details(
        title=add_formatter.title_str("block", "red", len(block_names)),
        desc=list_to_str(block_names, action=Action.ADD),
    )
    file = Details(
        title=add_formatter.title_str("file", "dark_goldenrod", len(file_names)),
        desc=list_to_str(file_names, action=Action.ADD),
    )

    return Panel.fit(
        textwrap.dedent(f"""
    {MAGIC} [magenta]Zentra[/magenta] configured successfully! {MAGIC}

    Use [green]zentra generate[/green] to create your models.

    [bright_cyan]Models To Generate[/bright_cyan]
    """)
        + f"{component.title}\n{component.desc}\n\n"
        + f"{block.title}\n{block.desc}\n\n"
        + f"{file.title}\n{file.desc}",
        border_style="bright_green",
    )


def generate_complete_panel(counts: CountStorage) -> Panel:
    """Creates a printable panel after successfully completing `zentra generate`."""
    components = (
        counts.generate.items,
        counts.remove.items,
    )

    formatter = partial(GeneratePanelFormatter, actions=Action)
    comp_formatter = formatter(name="component", data=components)

    comp_totals = (
        counts.get_count("generate"),
        counts.get_count("remove"),
    )

    comp_str = comp_formatter.data_str()

    component_title = comp_formatter.title_str(comp_totals, "yellow")

    return Panel.fit(
        textwrap.dedent(f"""
    {MAGIC} [magenta]Zentra[/magenta] → [bright_cyan]React[/bright_cyan] conversion successful! {MAGIC}
    
    Access them in [magenta]zentra/{GENERATE_DIR}[/magenta].
    
    [bright_cyan]Model Updates[/bright_cyan]
    """)
        + f"{component_title}\n{comp_str}",
        border_style="bright_green",
    )
