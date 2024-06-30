import os
from enum import Enum

from zentra_models.cli.conf.extract import get_dirpaths, local_path
from rich.console import Console


console = Console()

# Library versions
NEXTJS_VERSION = "14.1.4"
SHADCN_UI_VERSION = "0.8.0"

# Request package URLs
GITHUB_ROOT = "https://github.com/Achronus/Zentra"
BRANCH = "main"
GITHUB_URL_CORE = f"{GITHUB_ROOT}/tree/{BRANCH}"

GITHUB_COMPONENTS_DIR = f"{GITHUB_URL_CORE}/components"
GITHUB_INIT_ASSETS_DIR = f"{GITHUB_URL_CORE}/init"


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


# TODO: update URLS
# Core folder names and URLS
FOLDER_NAME = "zentra"
SETUP_FILE = "__init__.py"
DEMO_DIR = "_demo"

GETTING_STARTED_URL = "#"
ERROR_GUIDE_URL = "#"
GITHUB_ISSUES_URL = "https://github.com/Astrum-AI/Zentra/issues"


class ZentraLocalFilepaths:
    """A storage container for the core filepaths in the `zentra` folder."""

    def __init__(self) -> None:
        # (cwd)/zentra
        self.ROOT = os.path.join(os.getcwd(), FOLDER_NAME)
        self.MODELS = os.path.join(self.ROOT, "models")
        self.GENERATED = os.path.join(self.ROOT, "generated")
        self.DEMO = os.path.join(self.MODELS, DEMO_DIR)

        self.CONF = os.path.join(self.MODELS, SETUP_FILE)


class ZentraGeneratedFilepaths:
    """A storage container for the core filepaths in the `zentra/generated` folder."""

    def __init__(self) -> None:
        self.ROOT = ZentraLocalFilepaths().GENERATED
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


# Util filepaths
local_paths = ZentraLocalFilepaths()

MODELS_FILEPATH = f"[magenta][link={local_paths.MODELS}]{local_path(local_paths.MODELS)}[/link][/magenta]"
CONFIG_URL = os.path.join(local_paths.MODELS, SETUP_FILE)
