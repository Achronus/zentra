import pytest

from cli.conf.storage import ConfigExistStorage, PathStorage


class TestConfigExistStorage:
    @pytest.fixture
    def storage(self) -> ConfigExistStorage:
        return ConfigExistStorage()

    @staticmethod
    def test_app_configured_false(storage: ConfigExistStorage):
        assert not storage.app_configured()

    @staticmethod
    def test_app_configured_valid(storage: ConfigExistStorage):
        storage.models_folder_exists = True
        storage.config_file_exists = True
        storage.config_file_valid = True
        storage.models_registered = True
        assert storage.app_configured()


class TestPathStorage:
    @staticmethod
    def test_valid():
        storage = PathStorage(models_folder="/path/to/models")
        assert storage.models_folder == "/path/to/models"

    @staticmethod
    def test_invalid_type():
        with pytest.raises(TypeError):
            PathStorage(models_folder=123)
