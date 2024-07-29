import pytest
from types import ModuleType


from zentra_api.utils.package import load_module, package_path
from zentra_api.responses.utils import build_response, get_code_status, merge_dicts_list


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


class TestBuildResponse:
    @staticmethod
    def test_valid_code():
        result = build_response(100)
        target = "100_CONTINUE"
        assert result == target

    @staticmethod
    def test_with_no_strip():
        result = build_response(100, no_strip=True)
        target = "HTTP_100_CONTINUE"
        assert result == target

    @staticmethod
    def test_invalid_code():
        with pytest.raises(ValueError):
            build_response(6)


class TestGetCodeStatus:
    @staticmethod
    def test_success_code():
        assert get_code_status(200) == "success"

    @staticmethod
    def test_client_error_code():
        assert get_code_status(404) == "error"

    @staticmethod
    def test_info_code():
        assert get_code_status(100) == "info"

    @staticmethod
    def test_redirect_code():
        assert get_code_status(300) == "redirect"

    @staticmethod
    def test_server_error_code():
        assert get_code_status(500) == "error"

    @staticmethod
    def test_invalid_code():
        with pytest.raises(ValueError):
            get_code_status(6)


class TestMergeDictsList:
    @staticmethod
    def test_three_dicts():
        dict1 = {"a": 1, "b": 2}
        dict2 = {"c": 3}
        dict3 = {"d": 4, "e": 5}
        merged = merge_dicts_list([dict1, dict2, dict3])
        assert merged == {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5}
