from zentra.core import Component


class Button(Component):
    """A Zentra model for the `shadcn/ui` Button component."""


class Calendar(Component):
    """A Zentra model for the `shadcn/ui` Calendar component."""


class Checkbox(Component):
    """A Zentra model for the `shadcn/ui` Checkbox component."""


class Collapsible(Component):
    """A Zentra model for the `shadcn/ui` Collapsible component."""


class Combobox(Component):
    """A Zentra model for the `shadcn/ui` Combobox component."""


class DatePicker(Component):
    """A Zentra model for the `shadcn/ui` DatePicker component."""


class Input(Component):
    """A Zentra model for the `shadcn/ui` Input component."""

    label: str
    placeholder: str
    read_only: bool = False


class Label(Component):
    """A Zentra model for the `shadcn/ui` Label component."""


class RadioGroup(Component):
    """A Zentra model for the `shadcn/ui` RadioGroup component."""


class ScrollArea(Component):
    """A Zentra model for the `shadcn/ui` ScrollArea component."""


class Select(Component):
    """A Zentra model for the `shadcn/ui` Select component."""


class Slider(Component):
    """A Zentra model for the `shadcn/ui` Slider component."""


class Switch(Component):
    """A Zentra model for the `shadcn/ui` Switch component."""


class Tabs(Component):
    """A Zentra model for the `shadcn/ui` Tabs component."""


class Textarea(Component):
    """A Zentra model for the `shadcn/ui` Textarea component."""


class Toggle(Component):
    """A Zentra model for the `shadcn/ui` Toggle component."""


class ToggleGroup(Component):
    """A Zentra model for the `shadcn/ui` ToggleGroup component."""
