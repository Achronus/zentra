from zentra.core import Component


class Accordion(Component):
    """A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Accordion component."""


class AspectRatio(Component):
    """A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) AspectRatio component."""


class Avatar(Component):
    """A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Avatar component."""


class Badge(Component):
    """A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Badge component."""


class Card(Component):
    """A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Card component."""

    title: str = None
    description: str = None
    content: list[Component] = None
    footer: list[Component] = None


class Carousel(Component):
    """A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Carousel component."""


class DataTable(Component):
    """A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) DataTable component."""


class HoverCard(Component):
    """A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) HoverCard component."""


class Progress(Component):
    """A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Progress component."""


class Resizeable(Component):
    """A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Resizeable component."""


class Separator(Component):
    """A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Separator component."""


class Skeleton(Component):
    """A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Skeleton component."""


class Table(Component):
    """A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Table component."""
