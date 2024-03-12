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


class PathStorage:
    """A storage container for folder paths provided to controllers."""

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, self._validate_path(val))

    def _validate_path(self, path: str) -> str:
        """Validates kwarg values to ensure they are strings."""
        if not isinstance(path, str):
            raise TypeError(f"Invalid path type: {type(path)}. Path must be a string.")
        return path


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
