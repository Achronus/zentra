import os

from cli.conf.types import LibraryNamePairs


def remove_files(pairs: LibraryNamePairs, dir_path: str) -> None:
    """Removes a set of `(library_name, filename)` pairs from a directory."""
    for folder, filename in pairs:
        dirpath = os.path.join(dir_path, folder)
        filepath = os.path.join(dirpath, filename)

        os.remove(filepath)

        if len(os.listdir(dirpath)) == 0:
            os.removedirs(dirpath)
