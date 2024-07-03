from enum import Enum

from rich.console import Console


console = Console()

# Dependency exclusions
DEPENDENCY_EXCLUSIONS = [
    "react",
]

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
    CONFIG_EMPTY = 2
    ZENTRA_MISSING = 3
    MODELS_DIR_MISSING = 4
    NO_COMPONENTS = 5
    REQUEST_FAILED = 900
    UNKNOWN_ERROR = 1000


class SetupSuccessCodes(Enum):
    COMPLETE = 10
    ALREADY_CONFIGURED = 11


class SetupErrorCodes(Enum):
    IMPORT_ERROR = 11


class GenerateSuccessCodes(Enum):
    COMPLETE = 20
    NO_NEW_COMPONENTS = 21


class GenerateErrorCodes(Enum):
    GENERATE_DIR_MISSING = 22


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
