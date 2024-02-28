from zentra.core import Component


class Form(Component):
    """A Zentra model for the `shadcn/ui` Form component."""

    fields: list[Component]


class FileUpload(Component):
    """A Zentra model for `uploadthings` FileUpload fields."""

    ...
