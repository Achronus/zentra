from zentra.core import Component


class Accordion(Component):
    """A Zentra model for the `shadcn/ui` Accordion component."""


class AspectRatio(Component):
    """A Zentra model for the `shadcn/ui` AspectRatio component."""


class Avatar(Component):
    """A Zentra model for the `shadcn/ui` Avatar component."""


class Badge(Component):
    """A Zentra model for the `shadcn/ui` Badge component."""


class Card(Component):
    """A Zentra model for the `shadcn/ui` Card component."""

    title: str = None
    description: str = None
    content: list[Component] = None
    footer: list[Component] = None


class Carousel(Component):
    """A Zentra model for the `shadcn/ui` Carousel component."""


class DataTable(Component):
    """A Zentra model for the `shadcn/ui` DataTable component."""


class HoverCard(Component):
    """A Zentra model for the `shadcn/ui` HoverCard component."""


class Progress(Component):
    """A Zentra model for the `shadcn/ui` Progress component."""


class Resizeable(Component):
    """A Zentra model for the `shadcn/ui` Resizeable component."""


class Separator(Component):
    """A Zentra model for the `shadcn/ui` Separator component."""


class Skeleton(Component):
    """A Zentra model for the `shadcn/ui` Skeleton component."""


class Table(Component):
    """A Zentra model for the `shadcn/ui` Table component."""
