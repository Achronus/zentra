import os
import unittest

from cli.conf.constants import (
    LocalCoreComponentFilepaths,
    LocalUIComponentFilepaths,
    LocalUploadthingFilepaths,
    ZentaFilepaths,
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


class TestZentraGeneratedFilepaths(unittest.TestCase):
    def test_root_path(self):
        self.assertEqual(
            ZentraGeneratedFilepaths.ROOT,
            os.path.join(os.getcwd(), "zentra", "generated"),
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


class TestLocalCoreComponentsFilepaths(unittest.TestCase):
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


class TestUIComponentFilepaths(unittest.TestCase):
    def test_root_path(self):
        self.assertEqual(
            LocalUIComponentFilepaths.ROOT,
            os.path.join(os.getcwd(), "cli", "components", "ui"),
        )

    def test_base_path(self):
        self.assertEqual(
            LocalUIComponentFilepaths.BASE,
            os.path.join(os.getcwd(), "cli", "components", "ui", "base"),
        )

    def test_templates_path(self):
        self.assertEqual(
            LocalUIComponentFilepaths.TEMPLATES,
            os.path.join(os.getcwd(), "cli", "components", "ui", "templates"),
        )


class TestLocalUploadthingFilepaths(unittest.TestCase):
    def test_root_path(self):
        self.assertEqual(
            LocalUploadthingFilepaths.ROOT,
            os.path.join(os.getcwd(), "cli", "components", "uploadthing"),
        )

    def test_base_path(self):
        self.assertEqual(
            LocalUploadthingFilepaths.BASE,
            os.path.join(os.getcwd(), "cli", "components", "uploadthing", "base"),
        )

    def test_templates_path(self):
        self.assertEqual(
            LocalUploadthingFilepaths.TEMPLATES,
            os.path.join(os.getcwd(), "cli", "components", "uploadthing", "templates"),
        )
