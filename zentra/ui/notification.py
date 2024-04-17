from zentra.core import Component
from zentra.ui import ShadcnUi


class Alert(Component, ShadcnUi):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Alert component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class AlertDialog(Component, ShadcnUi):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) AlertDialog component.

    Parameters:
    - `name` (`str`) - the name of the component
    """

    title: str = None
    description: str = None
    content: list[Component] | str = None
    footer: list[Component] | str = None
    trigger: list[Component] | str = None


class Sonner(Component, ShadcnUi):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Sonner component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class Toast(Component, ShadcnUi):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Toast component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class Tooltip(Component, ShadcnUi):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Tooltip component.

    Parameters:
    - `name` (`str`) - the name of the component
    """
