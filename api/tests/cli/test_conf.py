import os
from pathlib import Path
from types import ModuleType

import pytest
from zentra_api.cli.conf import load_module, package_path, ProjectDetails
from zentra_api.cli.conf.checks import (
    check_file_exists,
    check_folder_exists,
    zentra_root_path,
)


class TestPackagePath:
    @staticmethod
    def test_success():
        assert package_path("zentra_api", ["cli"])

    @staticmethod
    def test_fail():
        with pytest.raises(FileNotFoundError):
            package_path("zentra_api", ["nonexistent"])


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


class TestProjectDetails:
    @pytest.fixture
    def details(self, tmp_path: Path) -> ProjectDetails:
        return ProjectDetails(project_name="Test Project", root=tmp_path)

    @staticmethod
    def test_project_name_validation(details: ProjectDetails):
        assert details.project_name == "test_project"

    @staticmethod
    def test_project_path(details: ProjectDetails, tmp_path: Path):
        assert details.project_path == Path(tmp_path, "test_project")

    @staticmethod
    def test_project_dir(details: ProjectDetails):
        assert details.project_dir == "test_project_dir0/test_project"

    @staticmethod
    def test_author(details: ProjectDetails):
        assert details.author == "Placeholder Name <placeholder@email.com>"

    @staticmethod
    def test_app_path(details: ProjectDetails, tmp_path: Path):
        assert details.app_path == Path(tmp_path, "test_project", "app")


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
