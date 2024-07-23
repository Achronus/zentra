import os
from types import ModuleType

import pytest
from zentra_api.cli.conf import load_module
from zentra_api.cli.conf.checks import check_file_exists, check_folder_exists


class TestLoadModule:
    @staticmethod
    def test_valid():
        assert isinstance(load_module("os", "path"), ModuleType)

    @staticmethod
    def test_invalid():
        with pytest.raises(ValueError):
            assert load_module("non", "existent")


class TestCheckFileExists:
    @pytest.fixture
    def temp_file(self, tmp_path):
        file = tmp_path / "temp_file.txt"
        file.write_text("This is a temporary file.")
        return file

    @staticmethod
    def test_success(temp_file):
        assert check_file_exists(temp_file)

    @staticmethod
    def test_invalid_file():
        assert not check_file_exists("/nonexistentfile")


class TestCheckFolderExists:
    @pytest.fixture
    def temp_dir(self, tmp_path):
        dir = tmp_path / "temp_dir"
        dir.mkdir()
        return dir

    @staticmethod
    def test_success(temp_dir):
        assert check_folder_exists(temp_dir)

    @staticmethod
    def test_invalid_dir():
        assert not check_folder_exists("non_existing_folder")

    @staticmethod
    def test_invalid_file(temp_dir):
        file_path = os.path.join(temp_dir, "test_file.txt")
        assert not check_folder_exists(file_path)
