import os
import pytest

from cli.conf.handler.file import FileHandler


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

    def test_get_filenames_in_subdir_exist(self, zentra_fh):
        subdir_name = "test_success"
        dummy_files = [
            os.path.join(zentra_fh.folder_path, subdir_name, "file1.py"),
            os.path.join(zentra_fh.folder_path, subdir_name, "file2.py"),
        ]

        os.makedirs(os.path.join(zentra_fh.folder_path, subdir_name), exist_ok=True)
        for filename in dummy_files:
            with open(filename, "w") as f:
                f.write("")

        result_filenames = zentra_fh.get_filenames_in_subdir(subdir_name)
        assert result_filenames == dummy_files, "Error retrieving files."

    def test_get_filenames_in_subdir_not_exist(self, zentra_fh):
        subdir_name = "test_fail"
        os.makedirs(os.path.join(zentra_fh.folder_path, subdir_name), exist_ok=True)

        result_filenames = zentra_fh.get_filenames_in_subdir(subdir_name)
        assert result_filenames == [], "Error: files exist when they shouldn't!"
