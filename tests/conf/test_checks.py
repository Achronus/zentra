import ast
import os
import tempfile
import pytest

from cli.conf.checks import (
    CheckConfigFileValid,
    check_file_exists,
    check_folder_exists,
    check_models_registered,
)
from cli.conf.extract import get_file_content
from zentra.core import Component, Zentra


class TestCheckFileExists:
    def test_success(self):
        with tempfile.NamedTemporaryFile() as temp_file:
            assert check_file_exists(temp_file.name)

    def test_invalid_file(self):
        assert not check_file_exists("/nonexistentfile")


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


class TestCheckModelsRegistered:
    def test_fail(self):
        zentra = Zentra()
        assert not check_models_registered(zentra)

    def test_success(self):
        zentra = Zentra()
        zentra.register([Component(name="Component1")])
        assert check_models_registered(zentra)


class TestCheckConfigFileValid:
    def test_success(self, tmp_path):
        filepath = os.path.join(tmp_path, "valid_code")
        with open(filepath, "w") as f:
            f.write(
                "from zentra.core import Zentra\nzentra = Zentra()\nzentra.register()"
            )

        checker = CheckConfigFileValid()
        file_content = get_file_content(filepath)
        tree = ast.parse(file_content, filename=filepath)
        checker.visit(tree)
        assert checker.is_valid()

    def test_fail(self, tmp_path):
        filepath = os.path.join(tmp_path, "invalid_code")
        with open(filepath, "w") as f:
            f.write("from zentra.core import Zentra\nzentra = Zentra()")

        checker = CheckConfigFileValid()
        file_content = get_file_content(filepath)
        tree = ast.parse(file_content, filename=filepath)
        checker.visit(tree)
        assert not checker.is_valid()
