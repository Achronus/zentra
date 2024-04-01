import json
import requests

from cli.conf.constants import FAIL, CommonErrorCodes, console
from cli.conf.message import BUG_MSG

import typer
from bs4 import BeautifulSoup
from pydantic import BaseModel
from rich.panel import Panel


class FilenameStorage(BaseModel):
    """A storage container library filenames."""

    base: list[str] = None
    templates: list[str] = None
    lib: list[str] = None


class ComponentStorage(BaseModel):
    """A storage container for all library filenames."""

    ui: FilenameStorage
    uploadthing: FilenameStorage


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
        console.print(
            Panel(
                f"\n{FAIL} [red]Failed to fetch file contents[/red] {FAIL}\n\nStatus code: [red]{response.status_code}[/red]\nFile URL: [magenta]{url}[/magenta].\n{BUG_MSG}\n[cyan]Error code[/cyan]: {CommonErrorCodes.REQUEST_FAILED.value}",
                expand=False,
                border_style="bright_red",
            )
        )
        raise typer.Exit(code=CommonErrorCodes.REQUEST_FAILED)


class GithubContentRetriever:
    """A class dedicated to retrieving directory and filenames from a Github repository using the requests and beautiful soup packages."""

    def __init__(self, url: str) -> None:
        self.url = url

    def get_content(self, url: str) -> dict:
        """Retrieves the list of file and folders displayed on a Github page. Returns it as a dictionary of JSON data."""
        soup: BeautifulSoup = create_soup(url)
        content = soup.find("react-app").find("script").contents[0]
        return json.loads(content)

    def file_n_folders(self, url: str) -> list[dict]:
        """Retrieves a list of dictionaries from the page containing path related information. This includes:
        1. The `name` of the file/folder
        2. The `path` of it (`<previous_folder>/<name>`)
        3. the `contentType` (`directory` or `file`)
        """
        return self.get_content(url=url)["payload"]["tree"]["items"]

    def __repr__(self) -> str:  # pragma: no cover
        """Create a readable developer string representation of the object when using the `print()` function."""
        attributes = ", ".join(
            f"{key}={value!r}" for key, value in self.__dict__.items()
        )
        return f"{self.__class__.__name__}({attributes})"


class ComponentRetriever(GithubContentRetriever):
    """A retriever for extracting the component directory and filenames from Github."""

    def __init__(self, url: str) -> None:
        super().__init__(url)
        self.root_dirs: list[str] = self.set_dirnames(url=self.url)
        self.storage: ComponentStorage = None

        self.cache = {}

    def set_dirnames(self, url: str) -> list[str]:
        """Retrieves the directory names from a URL and returns them as a list."""
        dirnames = []
        file_folder_list = self.file_n_folders(url=url)

        for item in file_folder_list:
            if item["contentType"] == "directory":
                dirnames.append(item["name"])

        return dirnames

    def extract_names(self, url: str = None) -> dict:
        """Recursively extracts file and directory names."""
        if url is None:
            url = self.url

        if url in self.cache:
            return self.cache[url]

        file_dict = {}
        file_folder_list = self.file_n_folders(url=url)

        for item in file_folder_list:
            if item["contentType"] == "directory":
                subdir_url = f"{url}/{item['name']}"
                subdir_file_dict = self.extract_names(url=subdir_url)

                file_dict[item["name"]] = subdir_file_dict

            elif item["contentType"] == "file":
                if "files" not in file_dict:
                    file_dict["files"] = []
                file_dict["files"].append(item["name"])

        self.cache[url] = file_dict
        return file_dict

    def extract(self) -> None:
        """Populates the `FilenameStorage` containers."""
        components = {}
        file_dict = self.extract_names()

        for library, values in file_dict.items():
            input_kwargs = {}
            for subdir, files in values.items():
                input_kwargs[subdir] = files["files"]

            components[library] = FilenameStorage(**input_kwargs)

        self.storage = ComponentStorage(**components)


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
