import pytest
from types import ModuleType


from zentra_api.utils.package import load_module, package_path


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
