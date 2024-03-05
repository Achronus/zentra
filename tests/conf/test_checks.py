import os
import pytest

from cli.conf.checks import check_folder_exists


class TestCheckFolderExists:
    def test_success(self, zentra_path):
        os.makedirs(zentra_path)
        assert check_folder_exists(zentra_path), zentra_path

    def test_invalid_dir(
        self,
    ):
        non_existing_folder = "non_existing_folder"
        assert not check_folder_exists(non_existing_folder)

    def test_invalid_file(self, zentra_path):
        file_path = os.path.join(zentra_path, "test_file.txt")
        assert not check_folder_exists(file_path)
