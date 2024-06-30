import os

from zentra_models.cli.conf.types import LibraryNamePairs


def remove_files(
    pairs: LibraryNamePairs, dirpath: str, ignore_pair_folder: bool = False
) -> None:
    """Removes a set of `(library_name, filename)` pairs from a directory."""
    for folder, filename in pairs:
        if not ignore_pair_folder:
            dirpath = os.path.join(dirpath, folder)

        filepath = os.path.join(dirpath, filename)
        os.remove(filepath)

        if len(os.listdir(dirpath)) == 0:
            os.removedirs(dirpath)
