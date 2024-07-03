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


class Dependency(BaseModel):
    """A storage container for a single dependency."""

    name: str
    version: str


class CountStorage(BaseModel):
    """A simple storage container for Zentra model counts."""

    generate: int = 0
    remove: int = 0


class DependencyStorage(BaseModel):
    """A storage container for model dependencies."""

    external: list[Dependency] = []
    local: list[str] = []


class ModelFileStorage(BaseModel):
    """A storage container for storing Zentra model `(library, filename)` pairs."""

    generate: LibraryNamePairs = []
    remove: LibraryNamePairs = []
    existing: LibraryNamePairs = []

    counts: CountStorage = CountStorage()


class BasicNameStorage(BaseModel):
    """A simple storage container for Zentra page and component names."""

    pages: list[str] = []
    components: list[str] = []
    filenames: LibraryNamePairs = []


class ModelStorage(BaseModel):
    """A storage container for Zentra model filenames."""

    pages: ModelFileStorage = ModelFileStorage()
    components: ModelFileStorage = ModelFileStorage()
