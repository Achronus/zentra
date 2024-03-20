from zentra.core import Component


class FormField(Component):
    """A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) FormField inside the Form component."""

    label: str
    content: Component
    disabled: bool = False
    description: str = None
    message: bool = True


class Form(Component):
    """A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Form component."""

    fields: list[FormField]


class FileUpload(Component):
    """A Zentra model for the [uploadthing](https://uploadthing.com/) FileUpload fields."""

    ...
