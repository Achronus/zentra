from pathlib import Path
from unittest.mock import mock_open, patch
import pytest

from zentra_api.cli.builder.poetry import (
    PoetryDescription,
    PoetryFile,
    PoetryScript,
    toml_str,
)


class TestTomlStr:
    @staticmethod
    def test_str_valid():
        assert toml_str("key", "value") == 'key = "value"\n'

    @staticmethod
    def test_list_valid():
        assert toml_str("key", ["value1", "value2"]) == 'key = ["value1, value2"]\n'


def test_poetry_desc_as_str():
    description = PoetryDescription(name="test_project", authors=["<Test author>"])
    result = description.as_str()
    expected = [
        'name = "test_project"\n',
        'version = "0.1.0"\n',
        'description = "A FastAPI backend for processing API data."\n',
        'authors = ["<Test author>"]\n',
        'readme = "README.md"\n',
    ]
    assert result == expected


def test_poetry_script_as_str():
    script = PoetryScript(name="run-dev", command="app.run:development")
    assert script.as_str() == 'run-dev = "app.run:development"\n'


class TestPoetryFile:
    @pytest.fixture
    def mock_content(self) -> str:
        return (
            "some previous content\n"
            "[tool.poetry.dependencies]\n"
            'other_content = "value"\n'
        )

    @pytest.fixture
    def target_details(self) -> str:
        return (
            "[tool.poetry]\n"
            'name = "test_project"\n'
            'version = "0.1.0"\n'
            'description = "A FastAPI backend for processing API data."\n'
            'authors = ["<Test author>"]\n'
            'readme = "README.md"\n'
            "\n[tool.poetry.scripts]\n"
            'run-dev = "app.run:development"\n'
            'run-prod = "app.run:production"\n'
        )

    @pytest.fixture
    def other_target_content(self) -> str:
        return '[tool.poetry.dependencies]\nother_content = "value"\n'

    @pytest.fixture
    def file_obj(self) -> PoetryFile:
        return PoetryFile("test_project", "<Test author>")

    @staticmethod
    def test_build_details(file_obj: PoetryFile, target_details: str):
        result = file_obj.build_details()
        assert result == target_details

    @staticmethod
    def test_get_other_content(
        file_obj: PoetryFile, mock_content: str, other_target_content: str
    ):
        with patch("builtins.open", mock_open(read_data=mock_content)):
            other_content = file_obj.get_other_content(Path("fake_path"))

        assert other_content == other_target_content

    @staticmethod
    def test_build_new_content(
        file_obj: PoetryFile,
        mock_content: str,
        target_details: str,
        other_target_content: str,
    ):
        with patch("builtins.open", mock_open(read_data=mock_content)):
            new_content = file_obj.build_new_content(Path("fake_path"))

        assert new_content == f"{target_details}\n{other_target_content}"

    @staticmethod
    def test_update(
        file_obj: PoetryFile,
        tmp_path: Path,
        mock_content: str,
        target_details: str,
        other_target_content: str,
    ):
        filepath = tmp_path / "fake_path"
        filepath.write_text(mock_content)

        file_obj.update(filepath)

        updated_content = filepath.read_text()
        target = f"{target_details}\n{other_target_content}"
        assert updated_content == target
