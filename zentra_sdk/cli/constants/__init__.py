import os
from pathlib import Path
from enum import Enum

from rich.console import Console


console = Console()

# Core URLs
DOCS_URL = "https://zentra.achronus.dev"
GITHUB_ROOT = "https://github.com/Achronus/zentra"
GITHUB_ISSUES_URL = f"{GITHUB_ROOT}/issues"

GETTING_STARTED_URL = f"{DOCS_URL}/starting/"
ERROR_GUIDE_URL = f"{DOCS_URL}/help/errors/"

DOCKER_URL = "https://docs.docker.com/engine/install/"

# Custom print emoji's
PASS = "[green]\u2713[/green]"
FAIL = "[red]\u274c[/red]"
PARTY = ":party_popper:"
MAGIC = ":sparkles:"


# Docker details
DOCKER_FRONTEND_DETAILS = {
    "image_name": "achronus/nextjs-core",
    "container_name": "nextjs-container",
}


class SetupSuccessCodes(Enum):
    COMPLETE = 10
    ALREADY_CONFIGURED = 11


class CommonErrorCodes(Enum):
    TEST_ERROR = -1
    DOCKER_NOT_INSTALLED = 20
    PROJECT_NOT_FOUND = 21
    UNKNOWN_ERROR = 1000


class ProjectPaths:
    """Contains the local project filepaths."""

    cwd = os.getcwd()
    BACKEND_PATH = Path(cwd, "backend")
    FRONTEND_PATH = Path(cwd, "frontend")
