from pydantic import BaseModel

from cli.conf.types import LibraryNamePairs


class ConfigExistStorage:
    """
    A storage container for boolean values for the following config checks:
    1. `zentra/models` folder exists
    2. `zentra/models` setup file exists
    3. `zentra/models` setup file is valid with required elements
    """

    def __init__(self) -> None:
        self.models_folder_exists = False
        self.config_file_exists = False
        self.config_file_valid = False

    def app_configured(self) -> bool:
        """Checks if Zentra has already been configured correctly."""
        return all(
            [
                self.models_folder_exists,
                self.config_file_exists,
                self.config_file_valid,
            ]
        )


class SetupPathStorage(BaseModel):
    """
    A storage container for file and folder paths specific to `zentra init`.

    Parameters:
    - `config` (`string`) - the filepath to the Zentra models config file
    - `models` (`string`) - the directory path to the Zentra models folder
    - `demo` (`string`) - the directory path to the Zentra models demo folder
    """

    config: str
    models: str
    demo: str


class GeneratePathStorage(BaseModel):
    """
    A storage container for file and folder paths specific to `zentra generate`.

    Parameters:
    - `config` (`string`) - the filepath to the Zentra models config file
    - `models` (`string`) - the directory path to the Zentra models folder
    - `generate` (`string`) - the directory path to the Zentra generate component folder
    - `templates` (`string`) - the directory path to the Zentra generate template folder
    - `lib` (`string`) - the directory path to the Zentra generate lib folder
    """

    config: str
    models: str
    generate: str
    templates: str
    lib: str


class CountStorage(BaseModel):
    """A simple storage container for Zentra model counts."""

    generate: int = 0
    remove: int = 0


class ComponentDetails(BaseModel):
    """A container for storing core component details extracted from base JSX files."""

    library: str
    filename: str
    component_name: str
    child_component_names: list[str]


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

    initalised_models: list[ComponentDetails] = []
