from pathlib import Path
from pydantic import BaseModel, ConfigDict

from zentra_models.cli.local.enums import ZentraNameOptions


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


class Dependency(BaseModel):
    """A storage container for a single dependency."""

    name: str
    version: str


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

    @property
    def names(self) -> list[str]:
        """Returns the names of the components."""
        return [comp.name for comp in self.items]

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

    def add(self, comp: ComponentDetails) -> None:
        """Adds a component to storage."""
        if comp not in self.items:
            self.items.append(comp)

    def get_comp_by_filename(self, name: str) -> ComponentDetails:
        """Returns a component based on its filename."""
        for comp in self.items:
            if name == comp.path.filename:
                return comp


class NameStorage(BaseModel):
    """
    A storage container for storing name values.

    Parameters:
    - `files` (`list[string]`) - Zentra `ReactFile` model names
    - `blocks` (`list[string]`) - Zentra `Block` model names
    - `components` (`list[string]`) - Zentra `Component` model classnames
    - `libraries` (`list[string]`) - component library names
    """

    files: list[str] = []
    blocks: list[str] = []
    components: list[str] = []
    libraries: list[str] = []


class AppStorage(BaseModel):
    """A storage container for the `Zentra` app."""

    names: NameStorage = NameStorage()
    components: ComponentStorage = ComponentStorage()
    packages: list[Dependency] = []

    model_config = ConfigDict(use_enum_values=True)

    def add_names(self, attr: str, names: list) -> None:
        """Add a list of names to an attribute in the names storage."""
        items: list = getattr(self.names, attr)
        items.extend(names)

        setattr(self.names, attr, items)

    def add_component(self, component: ComponentDetails) -> None:
        """Adds a component to storage."""
        self.components.add(component)

    def add_packages(self, packages: list[Dependency]) -> None:
        """Adds a package to storage."""
        self.packages.extend(packages)

    def package_dict(self) -> dict[str, dict[str, str]]:
        """Returns the package dependencies as a dictionary."""
        new_dict = {}

        for package in self.packages:
            new_dict[package.name] = package.version

        return {"dependencies": new_dict}

    def get_target_components(self) -> ComponentStorage:
        """Returns a new `ComponentStorage` object with the components found in `NameStorage`."""
        return ComponentStorage(
            items=[
                comp
                for comp in self.components.items
                if comp.name in self.names.components
            ]
        )

    def get_local_paths(self, names: list[str]) -> list[Path]:
        """Returns the component local paths as a sorted list."""
        paths = self.components.local_paths(names)
        paths.sort()
        return paths

    def get_package_paths(self, names: list[str]) -> list[Path]:
        """Returns the component package paths as a sorted list."""
        paths = self.components.package_paths(names)
        paths.sort()
        return paths

    def get_names(self) -> tuple[list[str], list[str], list[str]]:
        """Returns a tuple of lists for each set of names in the form: `(files, blocks, components)`."""
        return self.names.files, self.names.blocks, self.names.components

    def get_name_option(self, option: ZentraNameOptions) -> list[str]:
        """Returns the stored names for a given option."""
        return getattr(self.names, option)

    def count(self, option: ZentraNameOptions) -> int:
        """Returns the stored count for a given option."""
        return len(self.get_name_option(option))


class ItemCounts(BaseModel):
    """A storage container for a single item that contains a list of strings and its size."""

    items: list[str] = []
    total: int = 0

    def update(self) -> None:
        """Updates the total automatically based on the number of items in the items list."""
        self.total = len(self.items)


class CountStorage:
    """A storage container for file counts."""

    def __init__(self) -> None:
        self.existing = ItemCounts()
        self.generate = ItemCounts()
        self.remove = ItemCounts()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(existing={repr(self.existing)}, generate={repr(self.generate)}, remove={repr(self.remove)})"

    def add(self, attr: str, items: list[str]) -> None:
        """Adds a list of items to an attribute."""
        item_counts: ItemCounts = getattr(self, attr)
        item_counts.items.extend(items)

    def update(self) -> None:
        """Updates the totals in storage."""
        self.existing.update()
        self.generate.update()
        self.remove.update()

    def get_count(self, attr: str) -> None:
        """Returns the item total for a given attribute."""
        return getattr(self, attr).total

    def fill(self, **kwargs) -> None:
        """Adds items to count storage based on `(key_name, values)` and updates its totals."""
        for key, value in kwargs.items():
            self.add(key, value)

        self.update()
