import os
import shutil

from cli.conf.types import FolderFilePair


def transfer_folder_file_pairs(
    folder_file_pairs: FolderFilePair,
    src_dir: str,
    dest_dir: str,
    src_sub_dir: str = "",
) -> None:
    """Copies a set of filenames from one directory to another using a list of `folder, filename)` pairs. Additionally, accepts an optional `src_sub_dir` for more refinement."""
    for folder, filename in folder_file_pairs:
        src_path = os.path.join(src_dir, folder, src_sub_dir, filename)
        dest_path = os.path.join(dest_dir, folder, filename)

        shutil.copy(src_path, dest_path)


def remove_folder_file_pairs(folder_file_pairs: FolderFilePair, dir_path: str) -> None:
    """Removes a set of `(folder, filename)` pairs from a directory."""
    for folder, filename in folder_file_pairs:
        dirpath = os.path.join(dir_path, folder)
        filepath = os.path.join(dirpath, filename)

        os.remove(filepath)

        if len(os.listdir(dirpath)) == 0:
            os.removedirs(dirpath)


def copy_file(filepath: str, dest_dir: str) -> None:
    """Copies a single file from one directory to another."""
    shutil.copy(filepath, dest_dir)


def copy_dir_files(filepath: str, dest_dir: str) -> None:
    """Copies a directory and its files to a new location."""
    dest_path = os.path.join(dest_dir, os.path.basename(filepath))
    os.makedirs(dest_path, exist_ok=True)
    shutil.copytree(filepath, dest_path, dirs_exist_ok=True)
