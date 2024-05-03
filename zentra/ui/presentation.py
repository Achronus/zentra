from zentra.core import Component
from zentra.core.enums.ui import Orientation
from zentra.ui import ShadcnUi


class Accordion(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui Accordion](https://ui.shadcn.com/docs/components/accordion) component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class AspectRatio(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui AspectRatio](https://ui.shadcn.com/docs/components/aspect-ratio) component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class Avatar(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui Avatar](https://ui.shadcn.com/docs/components/avatar) component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class Badge(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui Badge](https://ui.shadcn.com/docs/components/badge) component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class Card(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui Card](https://ui.shadcn.com/docs/components/card) component.

    Parameters:
    - `name` (`str`) - the name of the component
    """

    title: str = None
    description: str = None
    content: list[Component] = None
    footer: list[Component] = None


class Carousel(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui Carousel](https://ui.shadcn.com/docs/components/carousel) component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class DataTable(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui DataTable](https://ui.shadcn.com/docs/components/data-table) component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class HoverCard(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui HoverCard](https://ui.shadcn.com/docs/components/hover-card) component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class Progress(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui Progress](https://ui.shadcn.com/docs/components/progress) component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class Resizeable(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui Resizeable](https://ui.shadcn.com/docs/components/resizeable) component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class Separator(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui Separator](https://ui.shadcn.com/docs/components/separator) component.

    Parameters:
    - `styles` (`string, optional`) - an optional set of CSS classes. `None` by default
    - `orientation` (`string, optional`) - the axis orientation of the separator. Valid options: `['horizontal', 'vertical']`. `vertical` by default
    """

    styles: str = None
    orientation: Orientation = "vertical"


class Skeleton(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui Skeleton](https://ui.shadcn.com/docs/components/skeleton) component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class Table(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui Table](https://ui.shadcn.com/docs/components/table) component.

    Parameters:
    - `name` (`str`) - the name of the component
    """
