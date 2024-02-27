import os
import pytest

from cli.conf.file_handler import FileHandler


class TestFileHandler:
    @pytest.fixture
    def zentra_fh(self, zentra_path) -> FileHandler:
        return FileHandler(zentra_path)

    @pytest.fixture
    def dummy_fh(self, tmp_path) -> FileHandler:
        return FileHandler(os.path.join(tmp_path, "test_folder"))

    def test_check_folder_does_exist(self, zentra_fh, zentra_path):
        os.mkdir(zentra_path)

        assert (
            zentra_fh.check_folder_exists() is True
        ), f"Error with path: '{zentra_path}'"

    def test_check_folder_does_not_exist(self, dummy_fh):
        assert dummy_fh.check_folder_exists() is False, "Error: Folder exists."

    def test_check_folder_is_empty(self, zentra_fh, zentra_path):
        os.mkdir(zentra_path)
        assert (
            zentra_fh.check_folder_empty() is True
        ), f"Error in path, # files in folder '{os.path.basename(zentra_path)}': {len(os.listdir(zentra_path))}"

    def test_check_folder_is_not_empty(self, zentra_fh, zentra_path):
        os.mkdir(zentra_path)
        open(os.path.join(zentra_path, "file1.py"), "w")

        assert (
            zentra_fh.check_folder_empty() is False
        ), f"Error in path, # files in folder '{os.path.basename(zentra_path)}': {len(os.listdir(zentra_path))}"

    def test_get_python_files_has_files(self, zentra_fh, zentra_path):
        os.mkdir(zentra_path)
        open(os.path.join(zentra_path, "file1.py"), "w")

        assert len(zentra_fh.get_python_files()) > 0, "Error! No files exist."

    def test_get_python_files_has_no_files(self, zentra_fh, zentra_path):
        os.mkdir(zentra_path)
        file_count = len(zentra_fh.get_python_files())

        assert file_count == 0, f"Error! {file_count} files exist."
