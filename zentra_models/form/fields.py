from pydantic import Field, PrivateAttr, ValidationInfo, field_validator
from pydantic_core import PydanticCustomError

from zentra_models.core import DataArray

from . import GenericFormField, FormField, ImgDimensions
from .enums import CountryCode, FileType


class TextField(GenericFormField):
    """
    A Zentra model for creating `text input` form fields.

    Uses the [Shadcn/ui Input](https://ui.shadcn.com/docs/components/input) component.

    Parameters:
    - `name` (`string`) - the name of the field. Must be `camelCase` and a maximum of 30 characters
    - `label` (`string`) - the field heading. E.g., `Full Name`
    - `placeholder` (`string, optional`) - the text to display inside the field. `None` by default
    - `icon` (`boolean, optional`) - a flag to display the fields unique icon. `False` by default
    """

    _field_type = PrivateAttr("input")


class EmailField(GenericFormField):
    """
    A Zentra model for creating `email` form fields.

    Uses the [Shadcn/ui Input](https://ui.shadcn.com/docs/components/input) component.

    Parameters:
    - `name` (`string`) - the name of the field. Must be `camelCase` and a maximum of 30 characters
    - `label` (`string`) - the field heading. E.g., `Email Address`
    - `placeholder` (`string, optional`) - the text to display inside the field. `None` by default
    - `icon` (`boolean, optional`) - a flag to display the fields unique icon. `False` by default
    """

    _field_type = PrivateAttr("input")


class PhoneField(GenericFormField):
    """
    A Zentra model for creating `phone number` form fields.

    Uses the [react-phone-number-input](https://www.npmjs.com/package/react-phone-number-input) component.

    Parameters:
    - `name` (`string`) - the name of the field. Must be `camelCase` and a maximum of 30 characters
    - `label` (`string`) - the field heading. E.g., `Contact Number`
    - `placeholder` (`string, optional`) - the text to display inside the field. `None` by default
    - `icon` (`boolean, optional`) - a flag to display the fields unique icon. `False` by default
    - `country` (`zentra_models.form.enums.CountryCode`) - a two letter country code for the phone field (200+ supported)
    """

    country: CountryCode

    _field_type = PrivateAttr("phone")


class CheckboxField(FormField):
    """
    A Zentra model for creating `checkbox` form fields.

    Uses the [Shadcn/ui Checkbox](https://ui.shadcn.com/docs/components/checkbox) and [Label](https://ui.shadcn.com/docs/components/label) components.

    Parameters:
    - `name` (`string`) - the name of the field. Must be `camelCase` and a maximum of 30 characters
    - `label` (`string`) - the text next to the checkbox
    """

    _field_type = PrivateAttr("checkbox")


class DateField(GenericFormField):
    """
    A Zentra model for creating `date` form fields.

    Uses the [react-datepicker](https://www.npmjs.com/package/react-datepicker) component.

    Parameters:
    - `name` (`string`) - the name of the field. Must be `camelCase` and a maximum of 30 characters
    - `label` (`string`) - the field heading. E.g., `Date of Birth`
    - `placeholder` (`string, optional`) - the text to display inside the field. `None` by default
    - `icon` (`boolean, optional`) - a flag to display the fields unique icon. `False` by default
    """

    _field_type = PrivateAttr("date")


class RadioGroupField(FormField):
    """
    A Zentra model for creating `radio button` form fields.

    Uses the [Shadcn/ui RadioGroup](https://ui.shadcn.com/docs/components/radio-group) component.

    Parameters:
    - `name` (`string`) - the name of the field. Must be `camelCase` and a maximum of 30 characters
    - `label` (`string`) - the field heading. E.g., `Gender`
    - `options` (`list[string]`) - the text for each radio button. E.g., `['male', 'female', 'other']`
    """

    options: list[str]

    _field_type = PrivateAttr("radio")

    @property
    def data(self) -> str:
        return f"{self.name}Data"


class SelectField(GenericFormField):
    """
    A Zentra model for creating `select box` form fields.

    Uses the [Shadcn/ui Select](https://ui.shadcn.com/docs/components/select) component.

    Parameters:
    - `name` (`string`) - the name of the field. Must be `camelCase` and a maximum of 30 characters
    - `label` (`string`) - the field heading. E.g., `Email Address`
    - `placeholder` (`string, optional`) - the text to display inside the field. `None` by default
    - `icon` (`boolean, optional`) - a flag to display the fields unique icon. `False` by default
    - `api_url` (`string, optional`) - the api URL path to retrieve the data from. Cannot be used with `items`. `None` by default
    - `items` (`zentra_models.core.DataArray | list[string], optional`) - a Zentra `DataArray` or `list[strings]` of items to pass into the `selectbox`. Useful for passing predefined values stored locally. Cannot be used with `api_url`. `None` by default
    """

    api_url: str | None = None
    items: DataArray | list[str] | None = Field(None, validate_default=True)

    _field_type = PrivateAttr("select")

    @property
    def data(self) -> str:
        return f"{self.name}Data"

    @property
    def is_loading(self) -> str | None:
        if self.api_url:
            return f"{self.name}Loading"

        return None

    @field_validator("items")
    def validate_items(
        cls, items: DataArray | list[str] | None, info: ValidationInfo
    ) -> DataArray | list[str] | None:
        api_url = info.data.get("api_url")

        if items and api_url:
            raise PydanticCustomError(
                "mututal_exclusion_error",
                "Cannot use 'api_url' with 'items'. Please select one.",
                dict(wrong_value=api_url),
            )
        elif not items and not api_url:
            raise PydanticCustomError(
                "missing_data",
                "A data source is required. Provide an 'api_url' or a set of 'items'",
                dict(wrong_value_one=items, wrong_value_two=api_url),
            )

        return items


class TextareaField(GenericFormField):
    """
    A Zentra model for creating `textarea` form fields.

    Uses the [Shadcn/ui Textarea](https://ui.shadcn.com/docs/components/textarea) component.

    Parameters:
    - `name` (`string`) - the name of the field. Must be `camelCase` and a maximum of 30 characters
    - `label` (`string`) - the field heading. E.g., `Email Address`
    - `placeholder` (`string, optional`) - the text to display inside the field. `None` by default
    - `icon` (`boolean, optional`) - a flag to display the fields unique icon. `False` by default
    """

    _field_type = PrivateAttr("textarea")


class FileUploadField(FormField):
    """
    A Zentra model for creating `file upload` form fields.

    Uses the [react-dropzone](https://www.npmjs.com/package/react-dropzone) component.

    Parameters:
    - `name` (`string`) - the name of the field. Must be `camelCase` and a maximum of 30 characters
    - `label` (`string`) - the field heading. E.g., `Email Address`
    - `file_types` (`list[form.FileType], optional`) - a list of valid file types. Can be any of the following: `['svg', 'png', 'jpg', 'pdf']`. `["SVG", "PNG", "JPG", "PDF"]` by default
    - `max_img_size` (`tuple[integer, integer], optional`) - the valid max image size that can be uploaded. Requires a tuple of integers in the form: `(width, height)` pixel values. `(800, 400)` by default
    - `max_file_size` (`integer, optional`) - the maximum file size in megabytes (MB). `20` by default
    """

    file_types: list[FileType] = ["SVG", "PNG", "JPG", "PDF"]
    max_img_size: tuple[int, int] = (800, 400)
    max_file_size: int = 20

    _field_type = PrivateAttr("fileupload")

    @property
    def file_type_names(self) -> str:
        return f"{self.name}FileTypes"

    @property
    def img_dim_name(self) -> str:
        return f"{self.name}ImgDimensions"

    @field_validator("file_types")
    def validate_file_types(cls, file_types: list[FileType]) -> list[str]:
        return [file_type.upper() for file_type in file_types]

    @field_validator("max_img_size")
    def validate_img_size(cls, size_tuple: tuple[int, int]) -> ImgDimensions:
        return ImgDimensions(
            width=size_tuple[0],
            height=size_tuple[1],
        )
