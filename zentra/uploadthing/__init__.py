from cli.conf.constants import GITHUB_COMPONENTS_DIR
from cli.conf.types import LibraryNamePairs
from cli.templates.retrieval import GithubContentRetriever
from zentra.core import Component
from zentra.core.enums.ui import LibraryType


class Uploadthing:
    """A Zentra model for all [uploadthing](https://uploadthing.com/) components."""

    def __init__(self, core_folder: str = "lib") -> None:
        self.core_folder = core_folder
        self.core_path = f"{GITHUB_COMPONENTS_DIR}/{self.library}/{core_folder}"
        self.retriever = GithubContentRetriever(url=self.core_path)

    @property
    def library(self) -> str:
        return LibraryType.UPLOADTHING.value

    def core_file_urls(self) -> tuple[str, list[str]]:
        """Provides the GitHub URL root of the core files needed for the library and the names of the files inside it.

        Returns: `(core_path, [core_filename, ...])` ->
        - `core_file_urls` - the core filepath URLs to the files found in the GitHub repository
        '"""
        return self.core_path, self.retriever.filenames()

    def core_file_pairs(self) -> LibraryNamePairs:
        """Provides a list of '(library_name, filename)' pairs for the core files needed for the library."""
        return [(self.core_folder, name) for name in self.retriever.filenames()]


class FileUpload(Component, Uploadthing):
    """A Zentra model for the [uploadthing](https://uploadthing.com/) FileUpload fields.

    Parameters:
    - `api_endpoint` (`str, optional`) - the API endpoint to use. Defaults to `media`. API endpoints are stored in `frontend/src/lib/core.ts -> uploadFileRouter`. We advise you leave this as `media` until you update your `frontend` files later. You can find more information about this in the [uploadthing docs](https://docs.uploadthing.com/getting-started/appdir#set-up-a-filerouter)
    """

    api_endpoint: str = "media"
