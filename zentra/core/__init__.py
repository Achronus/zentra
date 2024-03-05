from pydantic import BaseModel


class Component(BaseModel):
    """
    A Zentra model for all React components.

    Parameters:
    - name (str) - the name of the component.
    """

    name: str


class Page(BaseModel):
    """A Zentra model for a single webpage of React components."""

    name: str
    components: list[Component]

    def get_schema(self, node: BaseModel = None) -> dict:
        """Returns a JSON tree of the `Page` components as nodes with a type (the component name) and its attributes (attrs)."""
        if node is None:
            node = self

        formatted_schema = {
            "node": {
                "type": node.__class__.__name__,
                "attrs": node.model_dump(),
            }
        }

        valid_attrs = ["content", "components", "fields"]
        components_attr = next(
            (attr for attr in valid_attrs if hasattr(node, attr)), None
        )

        if components_attr is not None:
            children = getattr(node, components_attr)

            # Handle leaf nodes
            if not isinstance(children, list):
                children = [children]

            if children:
                formatted_schema["children"] = [
                    self.get_schema(child) for child in children
                ]

        return formatted_schema


class Icon(BaseModel):
    """A Zentra model for [Radix Ui Icons](https://www.radix-ui.com/icons)."""

    name: str


class Zentra(BaseModel):
    """An application class for registering the components to create."""

    pages: list[Page] = []
    components: list[Component] = []

    def register(self, components: list[Page] | list[Component]) -> None:
        """Register a list of models to generate."""
        for component in components:
            if isinstance(component, Page):
                self.pages.append(component)
            elif isinstance(component, Component):
                self.components.append(component)
            else:
                raise ValueError(f"Invalid component type: {type(component)}")
