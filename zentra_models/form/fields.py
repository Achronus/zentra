from zentra_models.form import GenericFormField, FormField


class TextField(GenericFormField):
    """A Zentra model for creating `text input` form fields."""

    pass


class EmailField(GenericFormField):
    """A Zentra model for creating `email` form fields."""

    pass


class PhoneField(GenericFormField):
    """A Zentra model for creating `phone number` form fields."""

    country: str


class CheckboxField(FormField):
    """A Zentra model for creating `checkbox` form fields."""

    pass


class DateField(GenericFormField):
    """A Zentra model for creating `date` form fields."""

    pass


class RadioGroupField(FormField):
    """A Zentra model for creating `radio button` form fields."""

    options: list[str]


class SelectField(GenericFormField):
    """A Zentra model for creating `select box` form fields."""

    items: list


class TextareaField(GenericFormField):
    """A Zentra model for creating `textarea` form fields."""

    pass


class FileUploadField(FormField):
    """A Zentra model for creating `file upload` form fields."""

    file_types: list[str]
    max_img_size: str = "800x400"
    max_file_size: str = "20MB"
    multiple: bool = False
