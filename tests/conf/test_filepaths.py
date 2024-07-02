import os
import pytest

from zentra_models.cli.conf.constants import (
    ZentraLocalFilepaths,
    ZentraGeneratedFilepaths,
)


@pytest.fixture
def local_paths(tmp_path) -> ZentraLocalFilepaths:
    return ZentraLocalFilepaths(tmp_path)


@pytest.fixture
def generate_paths(tmp_path) -> ZentraGeneratedFilepaths:
    return ZentraGeneratedFilepaths(tmp_path)


class TestZentraLocalFilepaths:
    @staticmethod
    def test_root_path(tmp_path, local_paths: ZentraLocalFilepaths):
        assert local_paths.ROOT == os.path.join(tmp_path, "zentra")

    @staticmethod
    def test_models_path(tmp_path, local_paths: ZentraLocalFilepaths):
        assert local_paths.MODELS == os.path.join(tmp_path, "zentra", "models")

    @staticmethod
    def test_generated_path(tmp_path, local_paths: ZentraLocalFilepaths):
        assert local_paths.GENERATED == os.path.join(tmp_path, "zentra", "build")

    @staticmethod
    def test_setup_filename(tmp_path, local_paths: ZentraLocalFilepaths):
        assert local_paths.CONF == os.path.join(
            tmp_path, "zentra", "models", "__init__.py"
        )


class TestZentraGeneratedFilepaths:
    @staticmethod
    def test_root_path(tmp_path, generate_paths: ZentraGeneratedFilepaths):
        assert generate_paths.ROOT == os.path.join(tmp_path, "zentra", "build")

    @staticmethod
    def test_pages_path(tmp_path, generate_paths: ZentraGeneratedFilepaths):
        assert generate_paths.PAGES == os.path.join(
            tmp_path, "zentra", "build", "pages"
        )

    @staticmethod
    def test_components_path(tmp_path, generate_paths: ZentraGeneratedFilepaths):
        assert generate_paths.COMPONENTS == os.path.join(
            tmp_path, "zentra", "build", "components"
        )

    @staticmethod
    def test_lib_path(tmp_path, generate_paths: ZentraGeneratedFilepaths):
        assert generate_paths.LIB == os.path.join(tmp_path, "zentra", "build", "lib")

    @staticmethod
    def test_zentra_path(tmp_path, generate_paths: ZentraGeneratedFilepaths):
        assert generate_paths.ZENTRA == os.path.join(
            tmp_path, "zentra", "build", "components", "zentra"
        )
