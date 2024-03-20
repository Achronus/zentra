from zentra.core import Component


class Accordion(Component):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Accordion component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class AspectRatio(Component):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) AspectRatio component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class Avatar(Component):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Avatar component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class Badge(Component):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Badge component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class Card(Component):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Card component.

    Parameters:
    - `name` (`str`) - the name of the component
    """

    title: str = None
    description: str = None
    content: list[Component] = None
    footer: list[Component] = None


class Carousel(Component):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Carousel component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class DataTable(Component):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) DataTable component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class HoverCard(Component):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) HoverCard component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class Progress(Component):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Progress component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class Resizeable(Component):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Resizeable component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class Separator(Component):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Separator component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class Skeleton(Component):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Skeleton component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class Table(Component):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Table component.

    Parameters:
    - `name` (`str`) - the name of the component
    """
