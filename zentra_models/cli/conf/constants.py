import os
from enum import Enum

from zentra_models.cli.conf.extract import get_dirpaths
from rich.console import Console


console = Console()

# Library versions
NEXTJS_VERSION = "14.1.4"
SHADCN_UI_VERSION = "0.8.0"

# Core URLs
DOCS_URL = "https://zentra.achronus.dev"
GITHUB_ROOT = "https://github.com/Achronus/zentra"
GITHUB_ISSUES_URL = f"{GITHUB_ROOT}/issues"

GETTING_STARTED_URL = f"{DOCS_URL}/starting/"
ERROR_GUIDE_URL = f"{DOCS_URL}/help/errors/"


class CommonErrorCodes(Enum):
    TEST_ERROR = -1
    CONFIG_MISSING = 1
    INVALID_CONFIG = 2
    CONFIG_EMPTY = 3
    ZENTRA_MISSING = 4
    MODELS_DIR_MISSING = 5
    REQUEST_FAILED = 900
    UNKNOWN_ERROR = 1000


class SetupSuccessCodes(Enum):
    COMPLETE = 10
    ALREADY_CONFIGURED = 11


class SetupErrorCodes(Enum):
    NO_COMPONENTS = 12
    IMPORT_ERROR = 13


class GenerateSuccessCodes(Enum):
    COMPLETE = 20
    NO_NEW_COMPONENTS = 21


class GenerateErrorCodes(Enum):
    NO_COMPONENTS = 22
    GENERATE_DIR_MISSING = 23


# Custom print emoji's
PASS = "[green]\u2713[/green]"
FAIL = "[red]\u274c[/red]"
PARTY = ":party_popper:"
MAGIC = ":sparkles:"


# Core folder and file names
FOLDER_NAME = "zentra"
SETUP_FILE = "__init__.py"
DEMO_DIR = "_demo"
GENERATE_DIR = "build"


def find_zentra_root() -> str:
    """
    Searches for the `zentra.root` file by traversing up the directory tree from the current directory.

    Returns the path found or an empty string.
    """
    current_dir = os.getcwd()

    while True:
        potential_root = os.path.join(current_dir, "zentra.root")
        if os.path.isfile(potential_root):
            return os.path.split(potential_root)[0]

        # Traverse up parent directory
        parent_dir = os.path.dirname(current_dir)
        if parent_dir == current_dir:
            # Reached root directory without finding
            return ""

        current_dir = parent_dir


def __dotenv_setter(name: str, value: str) -> None:
    os.environ[name] = value


def set_zentra_root(name: str) -> None:
    """Sets the `zentra` root directory path as an environment variable."""
    __dotenv_setter("ZENTRA_ROOT", name)


def get_zentra_root() -> str:
    """Retrieves the `zentra` root directory path."""
    return os.environ.get("ZENTRA_ROOT")


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
        self.ROOT = os.path.join(root_path, GENERATE_DIR)
        self.PAGES = os.path.join(self.ROOT, "pages")
        self.COMPONENTS = os.path.join(self.ROOT, "components")
        self.LIB = os.path.join(self.ROOT, "lib")

        self.ZENTRA = os.path.join(self.COMPONENTS, "zentra")


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
