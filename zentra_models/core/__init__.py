from typing import Any

from pydantic import BaseModel, Field, PrivateAttr, field_validator

from zentra_models.cli.local.storage import BasicNameStorage
from zentra_models.cli.constants.types import LibraryNamePairs
from zentra_models.base import ZentraModel
from zentra_models.core.constants import (
    LOWER_CAMELCASE_SINGLE_WORD,
    PASCALCASE_SINGLE_WORD,
    PASCALCASE_WITH_DIGITS,
    COMPONENT_FILTER_LIST,
)
from zentra_models.core.utils import name_from_pascal_case
from zentra_models.core.validation import check_pattern_match
from zentra_models.core.validation.component import data_array_validation


class Component(ZentraModel):
    """
    A Zentra model for all React components.
    """

    _parent = PrivateAttr(default=False)

    @property
    def is_parent(self) -> bool:
        """When `True` sets a component as a parent component and iterates over its children to get their content before graph conversion. `False` by default."""
        return self._parent


class DataArray(BaseModel):
    """
    A Zentra model for predefined data array objects.

    Parameters:
    - `name` (`string`) - the name of the `data` object. E.g., 'works'. Must be `lowercase` or `camelCase`, a `single word`, and up to a maximum of `30` characters
    - `type_name` (`string`) - the name for the `TypeScript` props associated to the data. Types are automatically populated based on the `data` value type. Must be `PascalCase`, a `single word`, and up to a maximum of `40` characters
    - `data` (`list[dict[string, Any]]`) - A list of dictionaries containing information that is typically passed into a JS iterable function such as a `map` (`zentra.models.core.js.Map`). Each dictionary must have the same key values and values of the same type


    Example usage:
    1. A simple data array of artists work.
    ```python
    from zentra.models.core import DataArray

    artwork_data = DataArray(
        name="works",
        type_name="Artwork",
        data=[
            {
                'artist': "Ornella Binni",
                'art': "https://images.unsplash.com/photo-1465869185982-5a1a7522cbcb?auto=format&fit=crop&w=300&q=80"
            },
            {
                'artist': "Tom Byrom",
                'art': "https://images.unsplash.com/photo-1548516173-3cabfa4607e9?auto=format&fit=crop&w=300&q=80"
            },
        ]
    )
    ```
    JSX equivalent ->
    ```jsx
    type Artwork = {
        artist: string
        art: string
    }

    const works: Artwork[] = [
        {
            artist: "Ornella Binni",
            art: "https://images.unsplash.com/photo-1465869185982-5a1a7522cbcb?auto=format&fit=crop&w=300&q=80",
        },
        {
            artist: "Tom Byrom",
            art: "https://images.unsplash.com/photo-1548516173-3cabfa4607e9?auto=format&fit=crop&w=300&q=80",
        },
    ]
    ```
    """

    name: str = Field(min_length=1, max_length=30)
    type_name: str = Field(min_length=1, max_length=40)
    data: list[dict[str, Any]]

    @field_validator("data")
    def validate_data(cls, data: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return data_array_validation(data)

    @field_validator("name")
    def validate_name(cls, v: str) -> str:
        return check_pattern_match(
            LOWER_CAMELCASE_SINGLE_WORD,
            v,
            err_msg=f"'{v}'. Must be 'lowercase' or 'camelCase', a single word and a maximum of '30' characters\n",
        )

    @field_validator("type_name")
    def validate_type_name(cls, v: str) -> str:
        return check_pattern_match(
            PASCALCASE_SINGLE_WORD,
            v,
            err_msg=f"'{v}'. Must be 'PascalCase', a single word and a maximum of '40' characters\n",
        )


class Page(BaseModel):
    """
    A Zentra model for a single webpage of React components.

    Parameters:
    - `name` (`string`) - the name of the page
    - `components` (`list[Component]`) - a list of page components
    """

    name: str = Field(min_length=1)
    components: list[Component]

    @field_validator("name")
    def validate_id(cls, name: str) -> str:
        return check_pattern_match(
            PASCALCASE_WITH_DIGITS, name, err_msg="must be PascalCase"
        )

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
                    f"Invalid component type: {type(component)}.\nMust be (or inherit from) a list of either: {valid_types}.\n\nValid examples:\n  zentra.models.register([Page(...), Page(...)])\n  zentra.models.register([Accordion(...), Button(...)])\n  zentra.models.register([Page(...), Accordion(...)])\n"
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
            (folder, f"{name_from_pascal_case(name)}.tsx")
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
