from pydantic import BaseModel
from cli.conf.constants import LocalUIComponentFilepaths, LocalUploadthingFilepaths
from cli.conf.extract import get_filenames_in_subdir


# TODO: add --nextjs flag
NEXTJS_PROJECT = False


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
    """

    ui_base: str


class GenerateComponentPaths(BaseModel):
    """
    A storage container for file and folder paths specific to Zentra Generate Component paths.

    Parameters:
    - zentra (str) - the path to the Zentra folder inside Zentra Generate Components folder
    - ui_base (str) - the path to the Zentra Generate UI base folder
    """

    zentra: str
    ui_base: str


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
    - core (storage.CorePaths) - a CorePaths object containing Zentra Core paths
    - local (storage.LocalComponentPaths) - a LocalComponentPaths object containing Local Zentra Component paths
    - generate (storage.GenerateComponentPaths) - a GeneratePaths object containing Zentra Generate Component paths
    """

    core: CorePaths
    local: LocalComponentPaths
    generate: GenerateComponentPaths


class ModelStorage(BaseModel):
    """A storage container for Zentra model filenames."""

    UI_BASE: list[str] = get_filenames_in_subdir(LocalUIComponentFilepaths.BASE)
    UI_TO_GENERATE: list[str] = []

    UPLOADTHING: list[str] = get_filenames_in_subdir(
        LocalUploadthingFilepaths.BASE_NEXTJS
        if NEXTJS_PROJECT
        else LocalUploadthingFilepaths.BASE_BASIC
    )
    UT_TO_GENERATE: list[str] = []
