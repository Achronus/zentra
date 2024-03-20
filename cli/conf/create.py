import os


def make_directories(dirpath: str) -> None:
    """Creates a set of directories, if they don't exist yet."""
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
