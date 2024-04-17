from zentra.core import Component
from zentra.core.enums.ui import Orientation
from zentra.ui import ShadcnUi


class Accordion(Component, ShadcnUi):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Accordion component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class AspectRatio(Component, ShadcnUi):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) AspectRatio component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class Avatar(Component, ShadcnUi):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Avatar component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class Badge(Component, ShadcnUi):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Badge component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class Card(Component, ShadcnUi):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Card component.

    Parameters:
    - `name` (`str`) - the name of the component
    """

    title: str = None
    description: str = None
    content: list[Component] = None
    footer: list[Component] = None


class Carousel(Component, ShadcnUi):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Carousel component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class DataTable(Component, ShadcnUi):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) DataTable component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class HoverCard(Component, ShadcnUi):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) HoverCard component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class Progress(Component, ShadcnUi):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Progress component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class Resizeable(Component, ShadcnUi):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Resizeable component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class Separator(Component, ShadcnUi):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Separator component.

    Parameters:
    - `styles` (`string, optional`) - an optional set of CSS classes. `None` by default
    - `orientation` (`string, optional`) - the axis orientation of the separator. Valid options: `['horizontal', 'vertical']`. `vertical` by default
    """

    styles: str = None
    orientation: Orientation = "vertical"


class Skeleton(Component, ShadcnUi):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Skeleton component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class Table(Component, ShadcnUi):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Table component.

    Parameters:
    - `name` (`str`) - the name of the component
    """
