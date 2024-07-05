import os
from pathlib import Path
import pytest

from zentra_models.cli.constants.filepaths import (
    ZentraLocalFilepaths,
    ZentraGeneratedFilepaths,
    ZentraPackageFilepaths,
    get_dirpaths,
)


@pytest.fixture
def local_paths(tmp_path) -> ZentraLocalFilepaths:
    return ZentraLocalFilepaths(tmp_path)


@pytest.fixture
def generate_paths(tmp_path) -> ZentraGeneratedFilepaths:
    return ZentraGeneratedFilepaths(tmp_path)


@pytest.fixture
def package_paths() -> ZentraPackageFilepaths:
    return ZentraPackageFilepaths()


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
    def test_demo_path(tmp_path, local_paths: ZentraLocalFilepaths):
        assert local_paths.DEMO == os.path.join(tmp_path, "zentra", "models", "_demo")

    @staticmethod
    def test_setup_filename(tmp_path, local_paths: ZentraLocalFilepaths):
        assert local_paths.CONF == os.path.join(
            tmp_path, "zentra", "models", "__init__.py"
        )

    @staticmethod
    def test_zentra_root(tmp_path, local_paths: ZentraLocalFilepaths):
        assert local_paths.ZENTRA_ROOT == os.path.join(tmp_path, "zentra.root")


class TestZentraGeneratedFilepaths:
    @staticmethod
    def test_root_path(tmp_path, generate_paths: ZentraGeneratedFilepaths):
        assert generate_paths.ROOT == os.path.join(tmp_path, "zentra", "build")

    @staticmethod
    def test_src_path(tmp_path, generate_paths: ZentraGeneratedFilepaths):
        assert generate_paths.SRC == os.path.join(tmp_path, "zentra", "build", "src")

    @staticmethod
    def test_components_path(tmp_path, generate_paths: ZentraGeneratedFilepaths):
        assert generate_paths.COMPONENTS == os.path.join(
            tmp_path, "zentra", "build", "src", "components"
        )

    @staticmethod
    def test_pages_path(tmp_path, generate_paths: ZentraGeneratedFilepaths):
        assert generate_paths.PAGES == os.path.join(
            tmp_path, "zentra", "build", "src", "pages"
        )

    @staticmethod
    def test_layouts_path(tmp_path, generate_paths: ZentraGeneratedFilepaths):
        assert generate_paths.LAYOUTS == os.path.join(
            tmp_path, "zentra", "build", "src", "layouts"
        )

    @staticmethod
    def test_lib_path(tmp_path, generate_paths: ZentraGeneratedFilepaths):
        assert generate_paths.LIB == os.path.join(
            tmp_path, "zentra", "build", "src", "lib"
        )


class TestZentraPackageFilepaths:
    @pytest.fixture
    def cli_dict(self) -> dict[str, Path]:
        return get_dirpaths("zentra_models", "cli")

    @pytest.fixture
    def models_dict(self) -> dict[str, Path]:
        return get_dirpaths("zentra_models", ignore=["cli"])

    @staticmethod
    def test_models_dict(models_dict: dict[str, Path]):
        target_keys = [
            "base",
            "core",
            "custom",
            "nextjs",
            "templates",
            "ui",
            "uploadthing",
        ]
        active_keys = list(models_dict.keys())
        assert target_keys == active_keys

    @staticmethod
    def test_cli_dict(cli_dict: dict[str, Path]):
        target_keys = [
            "commands",
            "components",
            "conf",
            "constants",
            "display",
            "init_assets",
            "local",
            "utils",
        ]
        active_keys = list(cli_dict.keys())
        assert target_keys == active_keys

    @staticmethod
    def test_init_assets(
        cli_dict: dict[str, Path], package_paths: ZentraPackageFilepaths
    ):
        assert package_paths.INIT_ASSETS == cli_dict["init_assets"]

    @staticmethod
    def test_component_assets(
        cli_dict: dict[str, Path], package_paths: ZentraPackageFilepaths
    ):
        assert package_paths.COMPONENT_ASSETS == cli_dict["components"]

    @staticmethod
    def test_demo_dir_path(
        cli_dict: dict[str, Path], package_paths: ZentraPackageFilepaths
    ):
        assert package_paths.DEMO == os.path.join(cli_dict["init_assets"], "_demo")

    @staticmethod
    def test_config_file_path(
        cli_dict: dict[str, Path], package_paths: ZentraPackageFilepaths
    ):
        assert package_paths.CONF == os.path.join(
            cli_dict["init_assets"], "__init__.py"
        )
