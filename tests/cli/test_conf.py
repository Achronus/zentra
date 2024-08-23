import os
import pytest

from zentra_sdk.cli.conf.checks import (
    check_file_exists,
    check_folder_exists,
    zentra_root_path,
)


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


class TestZentraRootPath:
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, tmp_path):
        self.original_cwd = os.getcwd()
        os.chdir(tmp_path)
        yield
        os.chdir(self.original_cwd)

    def test_found_in_current_dir(self, tmp_path):
        zentra_root = tmp_path / "zentra.root"
        zentra_root.touch()
        assert "zentra.root" in zentra_root_path().parts

    def test_found_in_parent_dir(self, tmp_path):
        project_dir = tmp_path / "project"
        subdir = project_dir / "subdir"
        subdir.mkdir(parents=True)

        zentra_root = project_dir / "zentra.root"
        zentra_root.touch()
        os.chdir(subdir)

        assert "zentra.root" in zentra_root_path().parts

    def test_not_found(self, tmp_path):
        project_dir = tmp_path / "project"
        subdir = project_dir / "subdir"
        subdir.mkdir(parents=True)

        os.chdir(subdir)

        assert zentra_root_path() is None
