import os
import shutil

import typer
from cli.conf.checks import check_folder_exists
from cli.conf.logger import file_copy_logger

from rich.console import Console

console = Console()


def copy_list_of_files(
    src: str,
    dest: str,
    src_err_code: int,
    dest_err_code: int,
    filenames: list[str] = None,
) -> None:
    """
    Copies a list of files from one directory to another.

    Parameters:
    - filenames (list[str], optional) - a list of filenames to copy over. When `None`, selects all files in the `src` directory. Defaults to `None`
    """
    if not check_folder_exists(src):
        file_copy_logger.error(
            f"SrcDirMissingError: '{os.path.basename(src)}' directory does not exist. Path: {src}"
        )
        raise typer.Exit(code=src_err_code)

    if not check_folder_exists(dest):
        file_copy_logger.error(
            f"DestDirMissingError: '{dest}' directory does not exist."
        )
        raise typer.Exit(code=dest_err_code)

    if filenames is None:
        filenames = []
        for entry in os.listdir(src):
            filepath = os.path.join(src, entry)
            if os.path.isfile(filepath):
                filenames.append(entry)

    for filename in filenames:
        src_path = os.path.join(src, filename)
        dest_path = os.path.join(dest, filename)

        if os.path.isfile(src_path):
            shutil.copy(src_path, dest_path)


def transfer_folder_file_pairs(
    folder_file_pairs: list[tuple[str, str]],
    src_dir: str,
    dest_dir: str,
    src_sub_dir: str = "",
) -> None:
    """Copies a set filenames from one directory to another using a list of `folder, filename)` pairs. Additionally, accepts an optional `src_sub_dir` for more refinement."""
    for folder, filename in folder_file_pairs:
        src_path = os.path.join(src_dir, folder, src_sub_dir, filename)
        dest_path = os.path.join(dest_dir, folder, filename)

        shutil.copy(src_path, dest_path)
