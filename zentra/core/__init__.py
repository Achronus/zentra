from pydantic import BaseModel


class Component(BaseModel):
    """A Zentra model for all React components."""

    name: str


class Page(BaseModel):
    """A Zentra model for a single webpage of React components."""

    components: list[Component]
