from pydantic import BaseModel

from .validate import FieldValidation


class FormField(BaseModel):
    """A Zentra model containing the foundation of all form fields."""

    id: str
    label: str


class GenericFormField(FormField):
    """A Zentra model for generic form fields."""

    placeholder: str | None = None
    icon: bool = False
    validation: FieldValidation | None = None


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
