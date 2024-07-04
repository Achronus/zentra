from pathlib import Path
from pydantic import BaseModel, ConfigDict

from zentra_models.cli.constants.types import LibraryNamePairs
from zentra_models.cli.local.enums import ZentraCoreOptions


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
    - `path` (`Filepath`) - a `Filepath` model
    - `children` (`list[Filepath]`) - a list of `Filepath` models for the components sub-components
    """

    name: str
    library: str
    path: Filepath
    children: list[Filepath]

    def __extract_paths(self, attr: str) -> list[Path]:
        """A helper method for extracting path values."""
        paths = [getattr(self.path, attr)]

        for child in self.children:
            paths.append(getattr(child, attr))

        return list(set(paths))

    def local_paths(self) -> list[Path]:
        """Returns the local paths as a list."""
        return self.__extract_paths("local")

    def package_paths(self) -> list[Path]:
        """Returns the package paths as a list."""
        return self.__extract_paths("package")


class ComponentStorage(BaseModel):
    """A storage container for storing a list of component details."""

    items: list[ComponentDetails] = []

    def __extract_paths(self, type: str) -> list[Path]:
        """A helper method for extracting paths."""
        paths = []
        for item in self.items:
            if type == "local":
                paths.extend(item.local_paths())
            elif type == "package":
                paths.extend(item.package_paths())

        return list(set(paths))

    def local_paths(self) -> list[Path]:
        """Retrieves the local paths for each item."""
        return self.__extract_paths("local")

    def package_paths(self) -> list[Path]:
        """Retrieves the packages paths for each item."""
        return self.__extract_paths("package")


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

    model_config = ConfigDict(use_enum_values=True)

    def count(self, option: ZentraCoreOptions) -> int:
        """Returns the name count of the desired option."""
        option_map = {
            ZentraCoreOptions.FILES.value: len(self.files),
            ZentraCoreOptions.BLOCKS.value: len(self.blocks),
            ZentraCoreOptions.COMPONENTS.value: len(self.components),
        }

        return option_map[option]


class ModelStorage(BaseModel):
    """A storage container for Zentra model filenames."""

    pages: ModelFileStorage = ModelFileStorage()
    components: ModelFileStorage = ModelFileStorage()


class AppStorage(BaseModel):
    """A storage container for the `Zentra` app."""

    names: NameStorage = NameStorage()
    components: ComponentStorage = ComponentStorage()
    packages: list[Dependency] = []

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

    def add_packages(self, packages: list[Dependency]) -> None:
        """Adds a package to storage."""
        self.packages.extend(packages)

    def package_dict(self) -> dict[str, dict[str, str]]:
        """Returns the package dependencies as a dictionary."""
        new_dict = {}

        for package in self.packages:
            new_dict[package.name] = package.version

        return {"dependencies": new_dict}

    def get_local_paths(self) -> list[Path]:
        """Returns the component local paths as a sorted list."""
        paths = self.components.local_paths()
        paths.sort()
        return paths

    def get_package_paths(self) -> list[Path]:
        """Returns the component package paths as a sorted list."""
        paths = self.components.package_paths()
        paths.sort()
        return paths

    def get_names(self) -> tuple[list[str], list[str], list[str]]:
        """Returns a tuple of lists for each set of names in the form: `(files, blocks, components)`."""
        return self.names.files, self.names.blocks, self.names.components

    def count(self, option: ZentraCoreOptions) -> int:
        """Returns the stored count for a given option."""
        return self.names.count(option)
