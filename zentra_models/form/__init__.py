from pydantic import BaseModel, ConfigDict, Field, PrivateAttr, field_validator

from zentra_models.validation.constants import LOWER_CAMELCASE_SINGLE_WORD
from zentra_models.validation.common import check_pattern_match

from .enums import FormFieldType
from .validate import FieldValidation


class ImgDimensions(BaseModel):
    """A model for storing image dimensions."""

    width: int
    height: int


class DynamicFormField(BaseModel):
    """A model representation of a JSX dynamic form field."""

    fieldType: FormFieldType
    control: str = Field("form.control", frozen=True)
    name: str
    label: str
    placeholder: str | None = None
    icon: bool | None = None
    defaultCountry: str | None = None
    data: str | None = None
    isLoading: str | None = None
    fileTypes: str | None = None
    maxMB: int | None = None
    maxImgDim: str | None = None

    model_config = ConfigDict(use_enum_values=True)


class FormField(BaseModel):
    """
    A Zentra model containing the foundation of all form fields.

    Parameters:
    - `name` (`string`) - the name of the field. Must be `camelCase` and a maximum of 30 characters
    - `label` (`string`) - the field heading. E.g., `Email Address`
    """

    name: str = Field(..., max_length=30)
    label: str

    _field_type = PrivateAttr(None)
    model_config = ConfigDict(use_enum_values=True)

    @property
    def field_type(self) -> str:
        return self._field_type

    @field_validator("name")
    def validate_name(cls, name: str) -> str:
        return check_pattern_match(
            LOWER_CAMELCASE_SINGLE_WORD,
            name,
            err_msg="Must be 'lowercase' or 'camelCase', a single word and a maximum of '30' characters\n",
        )


class GenericFormField(FormField):
    """
    A Zentra model for generic form fields.

    Parameters:
    - `name` (`string`) - the name of the field. Must be `camelCase` and a maximum of 30 characters
    - `label` (`string`) - the field heading. E.g., `Email Address`
    - `placeholder` (`string, optional`) - the text to display inside the field. `None` by default
    - `icon` (`boolean, optional`) - a flag to display the fields unique icon. `False` by default
    """

    placeholder: str | None = None
    icon: bool = False


class FormSection(BaseModel):
    """A Zentra model for form sections."""

    title: str
    desc: str | None = None
    fields: list[FormField | list[FormField]]


class Form(BaseModel):
    """A Zentra model for forms."""

    name: str
    title: str
    desc: str | None = None
    sections: list[FormSection]
    btn_text: str
