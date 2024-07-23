from pydantic import BaseModel, Field


class Zod(BaseModel):
    """A base model for [Zod](https://zod.dev/) forms."""

    pass


class FieldValidation(Zod):
    """A base model for validating form fields."""

    pass


class FieldMessages(Zod):
    """A base model for form field validation messages."""

    pass


class StringValidation(FieldValidation):
    """Form field validation for strings."""


class StringMessages(FieldMessages):
    """"""

    min: bool = False
    max: bool = Field()
