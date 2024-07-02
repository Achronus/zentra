import pytest

from zentra_models.cli.conf.storage import ConfigExistStorage


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
        storage.root_exists = True
        assert storage.app_configured()
