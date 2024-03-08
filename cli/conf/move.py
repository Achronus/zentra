import os
import shutil

import typer
from cli.conf.checks import check_folder_exists
from cli.conf.constants import CommonErrorCodes
from cli.conf.logger import file_copy_logger


def copy_list_of_files(
    src: str, dest: str, filenames: list[str], src_err_code: int, dest_err_code: int
) -> None:
    """Copies a list of files from one directory to another."""
    if not check_folder_exists(src):
        file_copy_logger.error(
            f"FileNotFoundError: '{os.path.basename(src)}' directory does not exist. Path: {src}"
        )
        raise typer.Exit(code=src_err_code)

    if not check_folder_exists(dest):
        file_copy_logger.error(f"FileNotFoundError: '{dest}' directory does not exist.")
        raise typer.Exit(code=dest_err_code)

    for filename in filenames:
        src_path = os.path.join(src, filename)
        dest_path = os.path.join(dest, filename)

        if os.path.isfile(src_path):
            shutil.copy(src_path, dest_path)
