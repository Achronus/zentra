import pytest

from cli.conf.storage import ConfigExistStorage, PathStorage


class TestConfigExistStorage:
    @pytest.fixture
    def storage(self) -> ConfigExistStorage:
        return ConfigExistStorage()

    @staticmethod
    def test_set_true_valid(storage: ConfigExistStorage):
        storage.set_true("models_folder_exists")
        assert storage.models_folder_exists

    @staticmethod
    def test_set_true_invalid(storage: ConfigExistStorage):
        with pytest.raises(ValueError):
            storage.set_true("not_here")

    @staticmethod
    def test_app_configured_true(storage: ConfigExistStorage):
        assert not storage.app_configured()

    @staticmethod
    def test_app_configured_false(storage: ConfigExistStorage):
        storage.set_true("models_folder_exists")
        storage.set_true("config_file_exists")
        storage.set_true("config_file_valid")
        storage.set_true("models_registered")
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
