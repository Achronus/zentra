from zentra.core import Component


class FormField(Component):
    """A Zentra model for the `shadcn/ui` FormField inside the Form component."""

    label: str
    component: Component
    disabled: bool = False
    description: str = None
    message: bool = True


class Form(Component):
    """A Zentra model for the `shadcn/ui` Form component."""

    fields: list[FormField]


class FileUpload(Component):
    """A Zentra model for the `uploadthing` FileUpload fields."""

    ...
