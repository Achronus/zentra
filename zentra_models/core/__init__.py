import asyncio
import os
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, PrivateAttr, field_validator

from zentra_models.base import ZentraModel
from zentra_models.cli.constants.filepaths import PACKAGE_PATHS
from zentra_models.cli.local.dependencies import DependencyManager
from zentra_models.cli.local.enums import FileType
from zentra_models.cli.local.nodes import ComponentNode
from zentra_models.cli.local.storage import AppStorage, ComponentDetails
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

    Parameters:
    - `name` (`string`) - the name of the function in PascalCase
    - `components` (`list[zentra_models.core.Component]`) - a list of `Component` models
    """

    name: str = Field(min_length=1)
    components: list[Component]

    @field_validator("name")
    def validate_id(cls, name: str) -> str:
        return check_pattern_match(
            PASCALCASE_WITH_DIGITS, name, err_msg="must be PascalCase"
        )

    def nodes(self) -> list[ComponentNode]:
        """Converts each component into component nodes and returns them as a list."""
        nodes = []
        for component in self.components:
            graph = LocalFilesGraphBuilder(component)
            nodes.append(graph.build())

        return nodes


class File(BaseModel):
    """
    A Zentra model for a single React file.

    Parameters:
    - `name` (`string`) - the name of the file in PascalCase
    - `block` (`zentra_models.core.Block`) - the main block to export from the file
    - `file_type` (`string, optional`) - the type of file. Determines what folder the file is stores. Options: `['component', 'layout', 'page']`. `component` by default
    - `extra_blocks` (`list[zentra_models.core.Block], optional`) - an optional list of block models associated to the main block. `None` by default
    """

    name: str = Field(min_length=1)
    block: Block
    file_type: FileType = "component"
    extra_blocks: list[Block] = None

    model_config = ConfigDict(use_enum_values=True)

    @field_validator("name")
    def validate_id(cls, name: str) -> str:
        return check_pattern_match(
            PASCALCASE_WITH_DIGITS, name, err_msg="must be PascalCase"
        )

    def get_blocks(self) -> list[Block]:
        """Extracts the blocks from the file and returns them as a list."""
        blocks = [self.block]

        if self.extra_blocks:
            blocks.extend(self.extra_blocks)

        return blocks

    def block_names(self) -> list[str]:
        """Returns the files block names as a list."""
        blocks = self.get_blocks()
        return [block.name for block in blocks]

    def component_nodes(self) -> list[ComponentNode]:
        """Extracts the components from each block as nodes and returns them as a list."""
        blocks = self.get_blocks()

        nodes = []
        for block in blocks:
            nodes.extend(block.nodes())

        return nodes


class FileManager(BaseModel):
    """A Zentra model for managing multiple files."""

    items: list[File] = []

    def add(self, files: File | list[File]) -> None:
        """Adds files to the container."""
        if isinstance(files, File):
            self.items.append(files)
        else:
            self.items.extend(files)

    def names(self) -> list[str]:
        """Returns the file names as a list."""
        return [file.name for file in self.items]

    def block_names(self) -> list[str]:
        """Returns the block names as a list."""
        names = []
        for file in self.items:
            names.extend(file.block_names())

        return names

    def component_nodes(self) -> list[ComponentNode]:
        """Returns the components in each file as a nodes list."""
        nodes = []
        for file in self.items:
            nodes.extend(file.component_nodes())
        return nodes

    def component_names(self) -> list[str]:
        """Returns the names of each component in each file as a list."""
        names = []
        for node in self.component_nodes():
            names.extend(self.node_names(node))

        names = list(set(names))
        names.sort()
        return names

    def component_pairs(self) -> list[tuple[str, str]]:
        """Returns the component `(library, name)` pairs from each files component nodes and returns them as a list."""
        pairs = []
        for node in self.component_nodes():
            pairs.extend(self.node_pairs(node))

        return pairs

    def node_names(self, node: ComponentNode) -> list[str]:
        """Extracts the component names from a component node and returns them as a list."""
        names = [node.name]
        for child in node.children:
            names.extend(self.node_names(child))

        return names

    def node_pairs(self, node: ComponentNode) -> list[tuple[str, str]]:
        """Extracts the `(library, name)` pairs from a component node and returns them as a list."""
        pairs = [node.pair()]
        for child in node.children:
            pairs.extend(self.node_pairs(child))

        return pairs


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
