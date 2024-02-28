from pydantic import BaseModel


class Component(BaseModel):
    """A Zentra model for creating a single React component."""

    ...


class Field(BaseModel):
    """A Zentra model for shadcn/ui form fields."""


class Form(BaseModel):
    """A Zentra model for shadcn/ui forms."""

    name: str
    fields: list[Field]


class Page(BaseModel):
    """A Zentra model for multiple React components."""

    components: list[Component]
