import os
import unittest

from zentra_models.cli.conf.constants import (
    ZentraLocalFilepaths,
    ZentraGeneratedFilepaths,
)


class TestZentaFilepaths(unittest.TestCase):
    def test_root_path(self):
        self.assertEqual(
            ZentraLocalFilepaths.ROOT,
            os.path.join(os.getcwd(), "zentra"),
        )

    def test_models_path(self):
        self.assertEqual(
            ZentraLocalFilepaths.MODELS,
            os.path.join(os.getcwd(), "zentra", "models"),
        )

    def test_generated_path(self):
        self.assertEqual(
            ZentraLocalFilepaths.GENERATED,
            os.path.join(os.getcwd(), "zentra", "generated"),
        )

    def test_setup_filename(self):
        self.assertEqual(ZentraLocalFilepaths.SETUP_FILENAME, "__init__.py")


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

    def test_lib_path(self):
        self.assertEqual(
            ZentraGeneratedFilepaths.LIB,
            os.path.join(os.getcwd(), "zentra", "generated", "lib"),
        )

    def test_zentra_path(self):
        self.assertEqual(
            ZentraGeneratedFilepaths.ZENTRA,
            os.path.join(os.getcwd(), "zentra", "generated", "components", "zentra"),
        )
