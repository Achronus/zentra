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


def make_code_files_from_url(url: str, filenames: list[str], dest_path: str) -> None:
    """
    Creates a set of code files from a url given a set of source filenames and a destination path. Creates directories automatically if they don't exist.

    Parameters:
    - `url` (`string`) - a URL to request information from
    - `filenames` (`list[str]`) - a list of filenames found at the URL
    - `dest_path` (`str`) - the location to create the files
    """
    os.makedirs(dest_path, exist_ok=True)

    for file in filenames:
        retriever = CodeRetriever(url=f"{url}/{file}")
        code = retriever.extract()
        make_file(os.path.join(dest_path, file), code)
