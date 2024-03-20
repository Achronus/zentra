from zentra.core import Component


class Alert(Component):
    """A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Alert component."""


class AlertDialog(Component):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) AlertDialog component.

    Parameters:
    - name (str) - the name of the component.
    """

    title: str = None
    description: str = None
    content: list[Component] | str = None
    footer: list[Component] | str = None
    trigger: list[Component] | str = None


class Sonner(Component):
    """A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Sonner component."""


class Toast(Component):
    """A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Toast component."""


class Tooltip(Component):
    """A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Tooltip component."""
