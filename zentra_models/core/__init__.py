import asyncio
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, PrivateAttr, field_validator

from zentra_models.base import ZentraModel
from zentra_models.cli.constants.filepaths import GENERATE_PATHS, PACKAGE_PATHS
from zentra_models.cli.local.builder import FilepathBuilder
from zentra_models.cli.local.enums import FileType
from zentra_models.cli.local.extractor import PackageExtractor
from zentra_models.cli.local.nodes import ComponentNode
from zentra_models.cli.local.storage import AppStorage, ComponentDetails, Filepath
from zentra_models.core.constants import (
    LOWER_CAMELCASE_SINGLE_WORD,
    PASCALCASE_SINGLE_WORD,
    PASCALCASE_WITH_DIGITS,
)
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


class ReactFile(BaseModel):
    """
    A Zentra model for a single React file.

    Parameters:
    - `name` (`string`) - the name of the file in PascalCase
    - `block` (`zentra_models.core.Block | list[zentra_models.core.Block]`) - a single or list of `Block` model
    - `file_type` (`string, optional`) - the type of file. Determines what folder the file is stores. Options: `['component', 'layout', 'page']`. `component` by default
    """

    name: str = Field(min_length=1)
    blocks: Block | list[Block]
    file_type: FileType = "component"

    model_config = ConfigDict(use_enum_values=True)

    @field_validator("name")
    def validate_id(cls, name: str) -> str:
        return check_pattern_match(
            PASCALCASE_WITH_DIGITS, name, err_msg="must be PascalCase"
        )

    @field_validator("blocks")
    def validate_blocks(cls, blocks: Block | list[Block]) -> list[Block]:
        if isinstance(blocks, Block):
            blocks = [blocks]
        return blocks

    def block_names(self) -> list[str]:
        """Returns the files block names as a list."""
        return [block.name for block in self.blocks]

    def component_nodes(self) -> list[ComponentNode]:
        """Extracts the components from each block as nodes and returns them as a list."""
        nodes = []
        for block in self.blocks:
            nodes.extend(block.nodes())

        return nodes


class FileManager(BaseModel):
    """A Zentra model for managing multiple files."""

    items: list[ReactFile] = []

    def add(self, files: ReactFile | list[ReactFile]) -> None:
        """Adds files to the container."""
        if isinstance(files, ReactFile):
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
        self.files = FileManager()
        self.storage = AppStorage()
        self.extractor = PackageExtractor()

    def valid_type_checks(self, models: list) -> None:
        """A helper function for raising errors for invalid types to the `register()` method."""
        file_type = "<class 'zentra_models.core.File'>"

        error_msg_list = f"\nMust be (or inherit from) a list of {file_type}."

        if not isinstance(models, list):
            raise ValueError(
                f"Invalid component type: {type(models)}.\n{error_msg_list}"
            )

        for idx, model in enumerate(models):
            if not isinstance(model, ReactFile):
                raise ValueError(
                    f"Invalid component type (idx: {idx}): {type(models)}.\n{error_msg_list}"
                )

    def register(self, files: ReactFile | list[ReactFile]) -> None:
        """Register a list of Zentra `File` models to generate."""
        if isinstance(files, ReactFile):
            files = [files]

        self.valid_type_checks(files)
        self.files.add(files)

        self.fill_storage()

    def fill_storage(self) -> None:
        """Populates the `AppStorage` based on the registered files."""
        self.storage.add_names("files", self.files.names())
        self.storage.add_names("blocks", self.files.block_names())
        self.storage.add_names("components", self.files.component_names())

        libraries = set(lib for lib, _ in self.files.component_pairs())
        self.storage.add_names("libraries", list(libraries))

        self.store_component_details()

    def store_component_details(self) -> None:
        """Iterates through the files, extracts the components packages and their details and adds them to their separate storage containers."""
        packages = []
        for lib, name in self.files.component_pairs():
            path = self.get_base_paths(lib, name)
            local, external = self.extractor.get_packages(path.package)
            children = self.get_child_filepaths(local)

            self.storage.add_component(
                ComponentDetails(
                    name=name,
                    library=lib,
                    children=children,
                    path=path,
                )
            )
            packages.extend(external)

        packages = list(set(packages))

        deps = asyncio.run(self.extractor.get_versions(packages))
        self.storage.add_packages(deps)

    def get_child_filepaths(self, local_imports: list[str]) -> list[Filepath]:
        """Converts a list of local imports into a list of Filepath models."""
        paths = []
        for child in local_imports:
            if child.startswith("@/components/"):
                lib, name = child.split("/")[-2:]

                path = self.get_base_paths(lib, name)
                paths.append(path)

        return paths

    def get_base_paths(self, lib: str, name: str) -> Filepath:
        """Returns the core component Filepath storage container based on a `(library, name)` pair. Extracted from the `base` package directory."""
        path = FilepathBuilder(
            name=name,
            library=lib,
            local_root=GENERATE_PATHS.COMPONENTS,
            package_root=PACKAGE_PATHS.COMPONENT_ASSETS,
            package_sub="base",
        )
        return Filepath(
            filename=path.filename(),
            local=path.local_path(),
            package=path.package_path(),
        )
