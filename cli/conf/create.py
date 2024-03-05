import os


def make_path_dirs(dirpath: str) -> None:
    """Creates a set of directories, if they don't exist yet."""
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
