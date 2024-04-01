import json

from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup


class FilenameStorage(BaseModel):
    """A storage container library filenames."""

    base: list[str] = None
    templates: list[str] = None
    lib: list[str] = None


def create_soup(url: str) -> BeautifulSoup:
    """Creates a BeautifulSoup object from a given URL."""
    response = requests.get(url)

    if response.status_code == 200:
        return BeautifulSoup(response.text, "html.parser")
    else:
        raise ConnectionError(f"Failed to fetch '{url}' contents.")


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

        self.ui: FilenameStorage = None
        self.uploadthing: FilenameStorage = None

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
        file_dict = self.extract_names()
        for library, values in file_dict.items():
            if hasattr(self, library):
                input_kwargs = {}
                for subdir, files in values.items():
                    input_kwargs[subdir] = files["files"]

                setattr(self, library, FilenameStorage(**input_kwargs))


class ZentraSetupRetriever(GithubContentRetriever):
    """A retriever for obtaining the setup filepaths for the `zentra init` command from Github."""

    def __init__(self, url: str) -> None:
        super().__init__(url)

        self.config: str = None
        self.demo_dir_path: str = None
        self.demo_filenames: list[str] = []

    def extract(self) -> None:
        """Extracts the filenames from Github and stores them in the retriever."""
        file_folder_list = self.file_n_folders(url=self.url)

        # Handle root
        for item in file_folder_list:
            if item["contentType"] == "file":
                self.config = item["name"]

            # Handle demo dir
            if item["contentType"] == "directory":
                new_url = f"{self.url}/{item['name']}"
                demo_file_folder_list = self.file_n_folders(url=new_url)
                self.demo_dir_path = item["name"]

                for file in demo_file_folder_list:
                    self.demo_filenames.append(file["name"])
