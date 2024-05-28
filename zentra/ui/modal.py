from typing import Optional
from zentra.core import Component
from zentra.core.html import Div

from zentra.ui import ShadcnUi
from zentra.ui.control import Button


class Dialog(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui Dialog](https://ui.shadcn.com/docs/components/dialog) component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class Popover(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui Popover](https://ui.shadcn.com/docs/components/popover) component.

    Parameters:
    - `trigger` (`zentra.ui.control.Button | string`) - the item to activate the popover. Can be either:
      1. A Zentra `Button` model
      2. A string of text
    - `content` (`zentra.core.html.Div`) - a zentra `Div` model containing the content of the popover
    - `styles` (`string, optional`) - a set of custom CSS classes to apply to the `PopoverContent`. Automatically adds them to its `className`. `None` by default
    """

    trigger: Button | str
    content: Div
    styles: Optional[str] = None

    @property
    def custom_common_attributes(self) -> list[str]:
        return ["styles"]

    @property
    def child_names(self) -> list[str]:
        return ["PopoverTrigger", "PopoverContent"]


class Sheet(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui Sheet](https://ui.shadcn.com/docs/components/sheet) component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class Drawer(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui Drawer](https://ui.shadcn.com/docs/components/drawer) component.

    Parameters:
    - `name` (`str`) - the name of the component
    """
