from zentra.core import Component
from zentra.ui import ShadcnUi


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
    - `name` (`str`) - the name of the component
    """


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
