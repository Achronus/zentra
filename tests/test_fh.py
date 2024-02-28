import os
import pytest

from cli.conf.file_handler import FileHandler


class TestFileHandler:
    @pytest.fixture
    def zentra_fh(self, zentra_path) -> FileHandler:
        return FileHandler(zentra_path)

    @pytest.fixture
    def dummy_fh(self, tmp_path) -> FileHandler:
        return FileHandler(os.path.join(tmp_path, "test_folder", "models"))

    def test_make_path_dirs_valid(self, zentra_fh, zentra_path):
        zentra_fh.make_path_dirs()

        assert os.path.exists(zentra_path), "Error! Directories not created."

    def test_check_folder_does_exist(self, zentra_fh, zentra_path):
        zentra_fh.make_path_dirs()

        assert (
            zentra_fh.check_folder_exists() is True
        ), f"Error with path: '{zentra_path}'"

    def test_check_folder_does_not_exist(self, dummy_fh):
        assert dummy_fh.check_folder_exists() is False, "Error: Folder exists."
