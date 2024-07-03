from itertools import chain
from typing import Any, Union

from pydantic import BaseModel, Field, PrivateAttr, field_validator

from zentra_models.cli.local.nodes import ComponentNode
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
    A parent `Zentra` model for all React components.
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


class Block(BaseModel):
    """
    A `Zentra` model for a single React component function.
    """

    name: str = Field(min_length=1)
    components: list[Component]


class Page(BaseModel):
    """
    A Zentra model for a single webpage of React components.

    Parameters:
    - `name` (`string`) - the name of the page
    - `blocks` (`list[Block]`) - a list of block models
    """

    name: str = Field(min_length=1)
    blocks: list[Block]

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


class LocalFilesGraphBuilder:
    """Converts a model into a node graph. Useful for retrieving the `library_name` and `classname` from a `Component` model tree."""

    def __init__(self, model: Component) -> None:
        self.model = model

    def build(self) -> ComponentNode:
        """Builds a graph of nodes."""
        name = self.model.classname
        library = self.model.library
        children = self.get_children(self.model)

        return self.set_node(
            self.model,
            args={
                "name": name,
                "library": library,
                "children": children,
            },
        )

    def __get_children(self, model: Component) -> list[Component]:
        """A helper method for retrieving the models children based on its content attributes."""
        children = []
        if model.content_attributes:
            for attr_name in model.content_attributes:
                items = getattr(model, attr_name)

                if items and not isinstance(items, str):
                    if isinstance(items, list):
                        children.extend(items)
                    else:
                        children.append(items)

        return children

    def get_children(self, model: Component) -> list[ComponentNode]:
        """Retrieves the models children and converts it into nodes."""
        children = self.__get_children(model)

        if len(children) == 1:
            return [self.set_node(children[0])]

        return [self.set_node(model) for model in children]

    def set_node(self, model: Component, args: dict = None) -> ComponentNode:
        """Create a component node model."""
        children = self.get_children(model)

        if args is None:
            args = {
                "name": model.classname,
                "library": model.library,
                "children": children,
            }

        return ComponentNode(**args)


class Zentra:
    """An application class for registering the components to create."""

    def __init__(self) -> None:
        self.pages = []
        self.blocks = []

        self.name_storage = BasicNameStorage()

    def valid_type_checks(
        self, models: list, valid_types: tuple[BaseModel, ...]
    ) -> None:
        """A helper function for raising errors for invalid types to the `register()` method."""

        types_str = "  " + "\n  ".join(
            [f"{idx}. {item}" for idx, item in enumerate(valid_types, start=1)]
        )
        error_msg_list = (
            f"\nMust be (or inherit from) a list of either:\n{types_str}\n."
        )

        if not isinstance(models, list):
            raise ValueError(
                f"Invalid component type: {type(models)}.\n{error_msg_list}"
            )

        for idx, model in enumerate(models):
            if not isinstance(model, valid_types):
                raise ValueError(
                    f"Invalid component type (idx: {idx}): {type(models)}.\n{error_msg_list}"
                )

    def register(self, models: list[Union[Page, Block]]) -> None:
        """Register a list of Zentra models to generate."""
        type_mapping: dict[BaseModel, list] = {
            Page: self.pages,
            Block: self.blocks,
        }

        self.valid_type_checks(models, tuple(type_mapping.keys()))

        for model in models:
            for model_type in type_mapping.keys():
                if isinstance(model, model_type):
                    type_mapping[model_type].append(model)

        self.fill_storage(self.pages)

    def fill_storage(self, pages: list[Page]) -> None:
        """Populates page and component names into name storage."""
        self.name_storage.pages = [page.name for page in pages]
        self.name_storage.blocks = [
            block.name for page in pages for block in page.blocks
        ]

        component_pairs = self.extract_pairs(
            self.pages, filter_list=COMPONENT_FILTER_LIST
        )
        component_names = [name for _, name in component_pairs]

        self.name_storage.components = component_names
        self.name_storage.filenames = component_pairs

    def extract_pairs(
        self, pages: list[Page], filter_list: list[str]
    ) -> LibraryNamePairs:
        """Extracts the `(folder, filename)` pairs for each components `base` file from a list of pages."""
        components = list(
            chain.from_iterable(
                [block.components for page in pages for block in page.blocks]
            )
        )

        component_pairs = []
        for component in components:
            graph = LocalFilesGraphBuilder(component)
            pairs = self.extract_name_pairs(graph.build())
            pairs = [(lib, name) for lib, name in pairs if name not in filter_list]
            component_pairs.extend(pairs)

        component_pairs = list(set(component_pairs))
        return [
            (lib, f"{name_from_pascal_case(name)}.tsx") for lib, name in component_pairs
        ]

    def extract_name_pairs(self, node: ComponentNode) -> LibraryNamePairs:
        """Creates a list of `(library, name)` pairs from a tree node."""
        pairs = [node.pair()]

        for child in node.children:
            if isinstance(child, ComponentNode):
                pairs.extend(self.extract_name_pairs(child))

        return pairs
