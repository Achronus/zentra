from pathlib import Path
from pydantic import BaseModel

from zentra_models.cli.constants.types import LibraryNamePairs


class ConfigExistStorage:
    """
    A storage container for boolean values for the following config checks:
    1. `zentra/models` folder exists
    2. `zentra/models` setup file exists
    3. `zentra.root` exists
    """

    def __init__(self) -> None:
        self.models_folder_exists = False
        self.config_file_exists = False
        self.root_exists = False

    def app_configured(self) -> bool:
        """Checks if all `zentra` files have been configured."""
        return all(
            [
                self.models_folder_exists,
                self.config_file_exists,
                self.root_exists,
            ]
        )


class CountStorage(BaseModel):
    """A simple storage container for Zentra model counts."""

    generate: int = 0
    remove: int = 0


class Dependency(BaseModel):
    """A storage container for a single dependency."""

    name: str
    version: str


class DependencyStorage(BaseModel):
    """A storage container for model dependencies."""

    external: list[Dependency] = []
    local: list[str] = []

    def as_dict(self) -> dict[str, dict[str, str]]:
        """Returns `external` as a dependency dictionary."""
        new_dict = {}

        for item in self.external:
            new_dict[item.name] = item.version

        return {"dependencies": new_dict}


class ModelFileStorage(BaseModel):
    """A storage container for storing Zentra model `(library, filename)` pairs."""

    generate: LibraryNamePairs = []
    remove: LibraryNamePairs = []
    existing: LibraryNamePairs = []

    counts: CountStorage = CountStorage()


class Filepath(BaseModel):
    """
    A storage container for storing a single components filepaths.

    Parameters:
    - `filename` (`string`) - the name of the file
    - `local` (`Path`) - the path to the `zentra` generate directory
    - `package` (`Path`) - the path to the `zentra_models` directory
    """

    filename: str
    local: Path
    package: Path


class ComponentDetails(BaseModel):
    """
    A storage container for a single set of component details.

    Parameters:
    - `name` (`string`) - the classname of the component
    - `library` (`string`) - the name of the library the component belongs to
    - `packages` (`list[Dependency]`) - the NPM packages associated to the component
    - `children` (`list[str]`) - the names of the sub-components used in the component
    - `local_path` (`Path`) - the base file location in the `zentra` directory
    - `package_path` (`Path`) - the base file location in the `zentra_models` packages
    """

    name: str
    library: str
    packages: list[Dependency]
    children: list[str]
    path: Filepath


class ComponentStorage(BaseModel):
    """A storage container for storing a list of component details."""

    items: list[ComponentDetails] = []

    def package_paths(self) -> list[str]:
        """Retrieves the packages paths for each item."""
        return [item.path.package for item in self.items]

    def local_paths(self) -> list[str]:
        """Retrieves the local paths for each item."""
        return [item.path.local for item in self.items]


class NameStorage(BaseModel):
    """
    A storage container for storing name values.

    Parameters:
    - `files` (`list[string]`) - Zentra `File` model names
    - `blocks` (`list[string]`) - Zentra `Block` model names
    - `components` (`list[string]`) - Zentra `Component` model classnames
    """

    files: list[str] = []
    blocks: list[str] = []
    components: list[str] = []


class ModelStorage(BaseModel):
    """A storage container for Zentra model filenames."""

    pages: ModelFileStorage = ModelFileStorage()
    components: ModelFileStorage = ModelFileStorage()


class AppStorage(BaseModel):
    """A storage container for the `Zentra` app."""

    names: NameStorage = NameStorage()
    components: ComponentStorage = ComponentStorage()

    def add_path(self, path: Filepath) -> None:
        """Adds a path to storage."""
        self.paths.items.append(path)

    def add_names(self, attr: str, names: list) -> None:
        """Add a list of names to an attribute in the names storage."""
        items: list = getattr(self.names, attr)
        items.extend(names)

        setattr(self.names, attr, items)

    def add_component(self, component: ComponentDetails) -> None:
        """Adds a component to storage."""
        self.components.items.append(component)
