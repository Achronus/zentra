import os

from cli.templates.retrieval import CodeRetriever


def make_directories(dirpath: str) -> None:
    """Creates a set of directories, if they don't exist yet."""
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)


def make_file(filepath: str, content: str) -> None:
    """Creates a new file in a given filepath with the given content."""
    with open(filepath, "w") as f:
        f.write(content)


def make_code_file_from_url(url: str, filename: str, dest_path: str) -> None:
    """
    Creates a code file from a URL given a filename and destination path.

    Parameters:
    - `url` (`string`) - a URL to request information from. Appends the filename to the end of it
    - `filenames` (`string`) - a filename found at the URL
    - `dest_path` (`string`) - the location to create the files
    """
    retriever = CodeRetriever(url=f"{url}/{filename}")
    code = retriever.extract()
    make_file(filepath=os.path.join(dest_path, filename), content=code)
