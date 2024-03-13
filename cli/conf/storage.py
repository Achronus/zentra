from cli.conf.constants import LocalCoreComponentFilepaths
from cli.conf.extract import get_dirnames, get_filename_dir_pairs

from pydantic import BaseModel


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


class CorePaths(BaseModel):
    """
    A storage container for file and folder paths specific to Zentra Core paths.

    Parameters:
    - config (str) - the filepath to the zentra models config file
    - models (str) - the directory path to the zentra models folder
    - demo (str, optional) - the directory path to the zentra models demo folder. Default is `None`. Note: required for `SetupPathStorage`.
    """

    config: str
    models: str
    demo: str = None


class LocalZentraConfigPaths(BaseModel):
    """
    A storage container for file and folder paths specific to local Zentra config paths.

    Parameters:
    - zentra (str) - the path to the local zentra config folder
    - demo (str) - the path to the local zentra config demo folder
    """

    zentra: str
    demo: str


class LocalComponentPaths(BaseModel):
    """
    A storage container for file and folder paths specific to local component paths.

    Parameters:
    - ui_base (str) - the path to the local UI base folder
    - ut_base (str) - the path to the Uploadthing base folder
    """

    ui_base: str
    ut_base: str


class GenerateComponentPaths(BaseModel):
    """
    A storage container for file and folder paths specific to Zentra Generate Component paths.

    Parameters:
    - zentra (str) - the path to the Zentra folder inside Zentra Generate Components folder
    - ui (str) - the path to the Zentra Generate UI folder
    - ut (str) - the path to the Zentra Generate Uploadthing folder
    """

    zentra: str
    ui: str
    ut: str


class SetupPathStorage(BaseModel):
    """
    A storage container for file and folder paths specific to `zentra init`.

    Parameters:
    - core (storage.CorePaths) - a CorePaths object containing Zentra Core paths
    - local (storage.LocalZentraConfigPaths) - a LocalZentraConfigPaths object containing local Zentra Config paths
    """

    core: CorePaths
    local: LocalZentraConfigPaths


class GeneratePathStorage(BaseModel):
    """
    A storage container for file and folder paths specific to `zentra generate`.

    Parameters:
    - config (str) - the filepath to the zentra models config file
    - models (str) - the directory path to the zentra models folder
    - component (str) - the directory path to the local zentra component folder
    - zentra (str) - the directory path to the zentra generate component folder
    """

    config: str
    models: str
    component: str
    generate: str


class ModelStorage(BaseModel):
    """A storage container for Zentra model filenames."""

    base_files: list[tuple[str, str]] = get_filename_dir_pairs(
        parent_dir=LocalCoreComponentFilepaths.ROOT, sub_dir="base"
    )
    files_to_generate: list[tuple[str, str]] = []
    folders_to_generate: list[str] = get_dirnames(LocalCoreComponentFilepaths.ROOT)
    new_files: list[tuple[str, str]] = []
