import re
from typing import Any

from pydantic import BaseModel, ConfigDict, PrivateAttr, ValidationInfo, field_validator
from pydantic_core import PydanticCustomError

from cli.conf.format import name_from_camel_case
from cli.conf.storage import BasicNameStorage
from cli.conf.types import LibraryNamePairs


LOWER_CAMELCASE_WITH_DIGITS = r"^[a-z]+(?:[A-Z][a-z]*)*\d*$"
CAPITALISED_CAMELCASE_WITH_DIGITS = r"^[A-Z][a-zA-Z0-9]*$"
LOWERCASE_SINGLE_WORD = r"^[a-z]+\b$"

COMPONENT_FILTER_LIST = [
    "FormField",
]


def has_valid_pattern(*, pattern: str, value: str) -> bool:
    match = re.match(pattern, value)
    return bool(match)


class Component(BaseModel):
    """
    A Zentra model for all React components.
    """

    _classname = PrivateAttr(default=None)
    model_config = ConfigDict(use_enum_values=True)

    @property
    def classname(self) -> str:
        """Stores the classname for the JSX builder."""
        return self._classname if self._classname else self.__class__.__name__


class Page(BaseModel):
    """
    A Zentra model for a single webpage of React components.

    Parameters:
    - `name` (`string`) - the name of the page
    - `components` (`list[Component]`) - a list of page components
    """

    name: str
    components: list[Component]

    @field_validator("name")
    def validate_id(cls, name: str) -> str:
        if not has_valid_pattern(pattern=CAPITALISED_CAMELCASE_WITH_DIGITS, value=name):
            raise PydanticCustomError(
                "string_pattern_mismatch",
                "must be capitalised and camelCase",
                dict(wrong_value=name, pattern=CAPITALISED_CAMELCASE_WITH_DIGITS),
            )
        return name

    def get_schema(self, node: BaseModel = None) -> dict:
        """Returns a JSON tree of the `Page` components as nodes with a type (the component name) and its attributes (attrs)."""
        if node is None:
            node = self

        if isinstance(node, list):
            return [self.get_schema(item) for item in node]

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


class Zentra(BaseModel):
    """An application class for registering the components to create."""

    _pages = PrivateAttr(default=[])
    _components = PrivateAttr(default=[])
    _name_storage = PrivateAttr(default=BasicNameStorage())

    @property
    def pages(self) -> list[Page]:
        """Stores a list of user created Pages found in the Zentra models folder."""
        return self._pages

    @property
    def components(self) -> list[Component]:
        """Stores a list of Zentra Components populated by the user in the Zentra models folder."""
        return self._components

    @property
    def name_storage(self) -> BasicNameStorage:
        """A storage container for the user defined Zentra pages and Component names."""
        return self._name_storage

    def __set_type(
        self, component: BaseModel, valid_types: tuple[BaseModel, ...]
    ) -> type:
        """Checks a components type and assigns it accordingly."""
        base_type = component.__class__.__base__
        return base_type if base_type in valid_types else type(component)

    def register(self, components: list[Page | Component]) -> None:
        """Register a list of Zentra models to generate."""
        type_mapping: dict[BaseModel, list] = {
            Page: self._pages,
            Component: self._components,
        }
        valid_types = tuple(type_mapping.keys())

        for component in components:
            if not isinstance(component, valid_types):
                raise ValueError(
                    f"Invalid component type: {type(component)}.\nMust be (or inherit from) a list of either: {valid_types}.\n\nValid examples:\n  zentra.register([Page(...), Page(...)])\n  zentra.register([Accordion(...), Button(...)])\n  zentra.register([Page(...), Accordion(...)])\n"
                )

            comp_type = self.__set_type(component, valid_types)
            type_mapping[comp_type].append(component)

        self.fill_storage(pages=self._pages)

    def fill_storage(self, pages: list[Page]) -> None:
        """Populates page and component names into name storage."""
        component_pairs = self.__extract_component_names(
            pages=pages, filter_list=COMPONENT_FILTER_LIST
        )
        component_names = [name for _, name in component_pairs]

        self._name_storage.components = component_names
        self._name_storage.pages = [page.name for page in pages]
        self._name_storage.filenames = [
            (folder, f"{name_from_camel_case(name)}.tsx")
            for folder, name in component_pairs
        ]

    @staticmethod
    def __extract_component_names(
        pages: list[Page], filter_list: list[str] = []
    ) -> LibraryNamePairs:
        """
        A helper function for retrieving the component names and their associated library name.


        Returns:
        `[(libray_name, component_name), ...]`
        """
        component_names = set()

        def recursive_extract(component: Component):
            if isinstance(component, list):
                for item in component:
                    recursive_extract(item)
            else:
                name = component.__class__.__name__
                if name not in filter_list:
                    library_name = component.library
                    component_names.add((library_name, name))

            for attr in ["content", "fields"]:
                if hasattr(component, attr):
                    next_node = getattr(component, attr)
                    recursive_extract(next_node)

        for page in pages:
            for component in page.components:
                recursive_extract(component)

        component_names = list(component_names)
        component_names.sort()
        return component_names
