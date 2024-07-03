import os
import importlib.resources as pkg_resources
from pathlib import Path

from zentra_models.cli.constants import (
    DEMO_DIR,
    FOLDER_NAME,
    GENERATE_DIR,
    SETUP_FILE,
)
from zentra_models.cli.conf.env import find_zentra_root, set_zentra_root


def get_dirpaths(
    package: str, resource_dir: str = ".", ignore: list[str] = None
) -> dict[str, Path]:
    """List all files in the resource directory of the package and store them in a dictionary. Removes files and custom directories based on `ignore` parameters.

    Returns:
        `dict[str, str] = {<dir_name>: <dir_path>}`
    """
    package_dict = {}
    for item in pkg_resources.files(package).joinpath(resource_dir).iterdir():
        package_dict[str(item).split("\\")[-1]] = item

    if "__pycache__" in package_dict.keys():
        package_dict.pop("__pycache__")

    if ignore:
        for key in ignore:
            if key in package_dict.keys():
                package_dict.pop(key)

    dirnames = package_dict.copy()
    for key, value in package_dict.items():
        if not os.path.isdir(value):
            dirnames.pop(key)

    return dirnames


class ZentraLocalFilepaths:
    """A storage container for the core filepaths in the `zentra` folder."""

    def __init__(self, root_path: str) -> None:
        self.ROOT = os.path.join(root_path, FOLDER_NAME)
        self.MODELS = os.path.join(self.ROOT, "models")
        self.GENERATED = os.path.join(self.ROOT, GENERATE_DIR)
        self.DEMO = os.path.join(self.MODELS, DEMO_DIR)

        self.CONF = os.path.join(self.MODELS, SETUP_FILE)

        self.ZENTRA_ROOT = os.path.join(root_path, "zentra.root")


class ZentraGeneratedFilepaths:
    """A storage container for the core filepaths in the `zentra/generated` folder."""

    def __init__(self, root_path: str) -> None:
        self.ROOT = os.path.join(root_path, FOLDER_NAME, GENERATE_DIR)
        self.SRC = os.path.join(self.ROOT, "src")
        self.COMPONENTS = os.path.join(self.SRC, "components")
        self.PAGES = os.path.join(self.SRC, "pages")
        self.LAYOUTS = os.path.join(self.SRC, "layouts")
        self.LIB = os.path.join(self.SRC, "lib")


class ZentraPackageFilepaths:
    """A storage container for the filepaths in the `zentra_models` package."""

    def __init__(self) -> None:
        self.MODELS_DICT = get_dirpaths("zentra_models", ignore=["cli"])
        self.CLI_DICT = get_dirpaths("zentra_models", "cli")

        self.INIT_ASSETS = self.CLI_DICT["init_assets"]
        self.COMPONENT_ASSETS = self.CLI_DICT["components"]

        self.DEMO = os.path.join(self.INIT_ASSETS, DEMO_DIR)
        self.CONF = os.path.join(self.INIT_ASSETS, SETUP_FILE)


# Init filepaths
root_path = find_zentra_root()

if not root_path:
    root_path = os.getcwd()

set_zentra_root(root_path)

LOCAL_PATHS = ZentraLocalFilepaths(root_path)
GENERATE_PATHS = ZentraGeneratedFilepaths(root_path)
PACKAGE_PATHS = ZentraPackageFilepaths()
