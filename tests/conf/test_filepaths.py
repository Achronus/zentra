import os
import unittest

from cli.conf.constants import (
    LocalCoreComponentFilepaths,
    ZentaFilepaths,
    ZentraConfigFilepaths,
    ZentraGeneratedFilepaths,
)


class TestZentaFilepaths(unittest.TestCase):
    def test_root_path(self):
        self.assertEqual(
            ZentaFilepaths.ROOT,
            os.path.join(os.getcwd(), "zentra"),
        )

    def test_models_path(self):
        self.assertEqual(
            ZentaFilepaths.MODELS,
            os.path.join(os.getcwd(), "zentra", "models"),
        )

    def test_generated_path(self):
        self.assertEqual(
            ZentaFilepaths.GENERATED,
            os.path.join(os.getcwd(), "zentra", "generated"),
        )

    def test_setup_filename(self):
        self.assertEqual(ZentaFilepaths.SETUP_FILENAME, "__init__.py")


class TestConfigFilepaths(unittest.TestCase):
    def test_root_path(self):
        self.assertEqual(
            ZentraConfigFilepaths.ROOT,
            os.path.join(os.getcwd(), "cli", "zentra_config"),
        )

    def test_demo_path(self):
        self.assertEqual(
            ZentraConfigFilepaths.DEMO,
            os.path.join(os.getcwd(), "cli", "zentra_config", "_demo"),
        )


class TestLocalCoreComponentFilepaths(unittest.TestCase):
    def test_root_path(self):
        self.assertEqual(
            LocalCoreComponentFilepaths.ROOT,
            os.path.join(os.getcwd(), "cli", "components"),
        )

    def test_ui_path(self):
        self.assertEqual(
            LocalCoreComponentFilepaths.UI,
            os.path.join(os.getcwd(), "cli", "components", "ui"),
        )

    def test_uploadthing_path(self):
        self.assertEqual(
            LocalCoreComponentFilepaths.UPLOADTHING,
            os.path.join(os.getcwd(), "cli", "components", "uploadthing"),
        )


class TestZentraGeneratedFilepaths(unittest.TestCase):
    def test_root_path(self):
        self.assertEqual(
            ZentraGeneratedFilepaths.ROOT,
            os.path.join(os.getcwd(), "zentra", "generated"),
        )

    def test_pages_path(self):
        self.assertEqual(
            ZentraGeneratedFilepaths.PAGES,
            os.path.join(os.getcwd(), "zentra", "generated", "pages"),
        )

    def test_components_path(self):
        self.assertEqual(
            ZentraGeneratedFilepaths.COMPONENTS,
            os.path.join(os.getcwd(), "zentra", "generated", "components"),
        )

    def test_zentra_path(self):
        self.assertEqual(
            ZentraGeneratedFilepaths.ZENTRA,
            os.path.join(os.getcwd(), "zentra", "generated", "components", "zentra"),
        )
