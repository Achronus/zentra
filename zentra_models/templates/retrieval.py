import json
import requests

from zentra_models.cli.constants import CommonErrorCodes, console

import typer
from bs4 import BeautifulSoup
from pydantic import BaseModel

from zentra_models.cli.display.err_panels import request_failed_panel


class FilenameStorage(BaseModel):
    """A storage container library filenames."""

    base: list[str] = None
    templates: list[str] = None
    lib: list[str] = None


class InitFilesStorage(BaseModel):
    """A storage container for the `zentra init` files."""

    config: str
    demo_dir_path: str
    demo_filenames: list[str]


def create_soup(url: str) -> BeautifulSoup:
    """Creates a BeautifulSoup object from a given URL."""
    response = requests.get(url)

    if response.status_code == 200:
        return BeautifulSoup(response.text, "html.parser")
    else:
        console.print()
        console.print(request_failed_panel(status_code=response.status_code, url=url))
        raise typer.Exit(code=CommonErrorCodes.REQUEST_FAILED)


class GithubContentRetriever:
    """A class dedicated to retrieving directory and filenames from a Github repository using the requests and beautiful soup packages."""

    def __init__(self, url: str) -> None:
        self.url = url

    def get_content(self, url: str = None) -> dict:
        """Retrieves the list of file and folders displayed on a Github page. Returns it as a dictionary of JSON data."""
        if not url:
            url = self.url

        soup: BeautifulSoup = create_soup(url)
        content = soup.find("react-app").find("script").contents[0]
        return json.loads(content)

    def file_n_folders(self, url: str = None) -> list[dict]:
        """Retrieves a list of dictionaries from the page containing path related information. This includes:
        1. The `name` of the file/folder
        2. The `path` of it (`<previous_folder>/<name>`)
        3. the `contentType` (`directory` or `file`)
        """
        if not url:
            url = self.url

        return self.get_content(url=url)["payload"]["tree"]["items"]

    def filenames(self, url: str = None) -> list[str]:
        """Retrieves a list of filenames from a URL."""
        if not url:
            url = self.url

        payload = self.file_n_folders(url=url)
        filenames = [file["name"] for file in payload if file["contentType"] == "file"]
        return filenames

    def __repr__(self) -> str:  # pragma: no cover
        """Create a readable developer string representation of the object when using the `print()` function."""
        attributes = ", ".join(
            f"{key}={value!r}" for key, value in self.__dict__.items()
        )
        return f"{self.__class__.__name__}({attributes})"


class ZentraSetupRetriever(GithubContentRetriever):
    """A retriever for obtaining the setup filepaths for the `zentra init` command from Github."""

    def __init__(self, url: str) -> None:
        super().__init__(url)

        self.storage: InitFilesStorage = None

    def extract(self) -> None:
        """Extracts the filenames from Github and stores them in the retriever."""
        init_files = {}
        file_folder_list = self.file_n_folders(url=self.url)

        # Handle root
        for item in file_folder_list:
            if item["contentType"] == "file":
                init_files["config"] = item["name"]

            # Handle demo dir
            if item["contentType"] == "directory":
                new_url = f"{self.url}/{item['name']}"
                demo_file_folder_list = self.file_n_folders(url=new_url)
                init_files["demo_dir_path"] = item["name"]

                demo_filenames = []
                for file in demo_file_folder_list:
                    demo_filenames.append(file["name"])

                init_files["demo_filenames"] = demo_filenames

        self.storage = InitFilesStorage(**init_files)


class CodeRetriever(GithubContentRetriever):
    """A retriever for obtaining the raw code inside a file found on Github."""

    def __init__(self, url: str) -> None:
        super().__init__(url)

    def code(self, url: str) -> list[str]:
        """Retrieves a list of strings for each line of code in a given file URL."""
        return self.get_content(url=url)["payload"]["blob"]["rawLines"]

    def extract(self) -> str:
        """Extracts the code from a URL and returns it as a string."""
        code_lines = self.code(url=self.url)
        return "\n".join(code_lines)
