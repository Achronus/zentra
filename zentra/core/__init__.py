from typing import Any
from pydantic import BaseModel, field_validator

from cli.conf.extract import extract_component_names
from cli.conf.storage import BasicNameStorage


class Component(BaseModel):
    """
    A Zentra model for all React components.
    """


class Page(BaseModel):
    """A Zentra model for a single webpage of React components."""

    name: str
    components: list[Component]

    def get_schema(self, node: BaseModel = None) -> dict:
        """Returns a JSON tree of the `Page` components as nodes with a type (the component name) and its attributes (attrs)."""
        if node is None:
            node = self

        formatted_schema = {
            "type": node.__class__.__name__,
            "attrs": node.model_dump(),
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
    names: BasicNameStorage = BasicNameStorage()

    @field_validator("pages", "components", "names", mode="plain")
    @classmethod
    def prevent_init_editing(cls, value: Any) -> ValueError:
        raise ValueError("Attributes cannot be updated during initialisation.")

    def __set_type(
        self, component: BaseModel, valid_types: tuple[BaseModel, ...]
    ) -> type:
        """Checks a components type and assigns it accordingly."""
        base_type = component.__class__.__base__
        return base_type if base_type in valid_types else type(component)

    def register(self, components: list[Page | Component]) -> None:
        """Register a list of Zentra models to generate."""
        type_mapping: dict[BaseModel, list] = {
            Page: self.pages,
            Component: self.components,
        }
        valid_types = tuple(type_mapping.keys())

        for component in components:
            if not isinstance(component, valid_types):
                raise ValueError(
                    f"Invalid component type: {type(component)}.\nMust be (or inherit from) a list of either: {valid_types}.\n\nValid examples:\n  zentra.register([Page(...), Page(...)])\n  zentra.register([Accordion(...), Button(...)])\n  zentra.register([Page(...), Accordion(...)])\n"
                )

            comp_type = self.__set_type(component, valid_types)
            type_mapping[comp_type].append(component)

        self.__set_component_cls_names()
        self.__set_page_names()

    def __get_page_component_names(self) -> list[str]:
        """A helper function for retrieving the page component names."""
        page_components = []

        for page in self.pages:
            page_components += extract_component_names(page.get_schema())

        return list(set(page_components))

    def __set_component_cls_names(self) -> None:
        """A helper function for storing the component class names."""
        filter_items = ["Page", "FormField"]
        page_components = self.__get_page_component_names()

        for component in self.components:
            page_components.append(component.__class__.__name__)

        self.names.components = list(set(page_components) - set(filter_items))

    def __set_page_names(self) -> None:
        """A helper function for retrieving the page names."""
        self.names.pages = [page.name for page in self.pages]
