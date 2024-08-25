import os
from pathlib import Path
from enum import Enum
import importlib.resources as pkg_resources

from rich.console import Console


console = Console()

# Core URLs
DOCS_URL = "https://zentra.achronus.dev"
GITHUB_ROOT = "https://github.com/Achronus/zentra"
GITHUB_ISSUES_URL = f"{GITHUB_ROOT}/issues"

GETTING_STARTED_URL = f"{DOCS_URL}/starting/"
ERROR_GUIDE_URL = f"{DOCS_URL}/help/errors/"

DOCKER_URL = "https://docs.docker.com/engine/install/"

PKG_DIR = pkg_resources.files("zentra_sdk")
LOG_FOLDER = PKG_DIR.joinpath("logs")

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

FRONTEND_FILES_TO_REMOVE = [
    "bun.lockb",
    "next.config.mjs",
    ".gitignore",
]


class SetupSuccessCodes(Enum):
    TEST_SUCCESS = -2
    COMPLETE = 10
    ALREADY_CONFIGURED = 11


class CommonErrorCodes(Enum):
    TEST_ERROR = -1
    DOCKER_NOT_INSTALLED = 20
    PROJECT_NOT_FOUND = 21
    UNKNOWN_ERROR = 1000


class ProjectPaths:
    """Contains the local project filepaths."""

    def __init__(self, root: Path = Path(os.getcwd())) -> None:
        self.ROOT = root
        self.BACKEND_PATH = Path(self.ROOT, "backend")
        self.FRONTEND_PATH = Path(self.ROOT, "frontend")

        self.ENV_LOCAL = Path(self.FRONTEND_PATH, ".env.local")


class PackagePaths:
    """Contains the package filepaths."""

    def __init__(self) -> None:
        self.PKG_DIR = pkg_resources.files("zentra_sdk")
        self.SETUP_ASSETS = self.PKG_DIR.joinpath("cli", "setup_assets")

        self.ROOT = self.SETUP_ASSETS.joinpath("root")
        self.FRONTEND = self.SETUP_ASSETS.joinpath("frontend")
