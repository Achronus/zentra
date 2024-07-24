from enum import Enum
from rich.console import Console


console = Console()


# Core URLs
DOCS_URL = "https://zentra.achronus.dev"
GITHUB_ROOT = "https://github.com/Achronus/zentra"
GITHUB_ISSUES_URL = f"{GITHUB_ROOT}/issues"

GETTING_STARTED_URL = f"{DOCS_URL}/starting/api/"
ERROR_GUIDE_URL = f"{DOCS_URL}/help/errors/"

ROOT_COMMAND = "zentra-api"

# Custom print emoji's
PASS = "[green]\u2713[/green]"
FAIL = "[red]\u274c[/red]"
PARTY = ":party_popper:"
MAGIC = ":sparkles:"


def pypi_url(package: str) -> str:
    return f"https://pypi.org/pypi/{package}/json"


# Define packages
PYTHON_VERSION = "3.12"

CORE_PIP_PACKAGES = [
    "fastapi",
    "sqlalchemy",
    "alembic",
    "pydantic-settings",
]

DEV_PIP_PACKAGES = [
    "pytest",
    "hypothesis",
]


class SetupSuccessCodes(Enum):
    COMPLETE = 10
    ALREADY_CONFIGURED = 11


class CommonErrorCodes(Enum):
    TEST_ERROR = -1
    UNKNOWN_ERROR = 1000
