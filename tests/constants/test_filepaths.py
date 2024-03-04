import os
import unittest

from cli.conf.constants import (
    ZentaFilepaths,
    ZentraGeneratedFilepaths,
    ZentraUIFilepaths,
)


class TestZentaFilepaths(unittest.TestCase):
    def test_root_path(self):
        self.assertEqual(ZentaFilepaths.ROOT, os.path.join(os.getcwd(), "zentra"))

    def test_models_path(self):
        self.assertEqual(
            ZentaFilepaths.MODELS, os.path.join(os.getcwd(), "zentra", "models")
        )

    def test_generated_path(self):
        self.assertEqual(
            ZentaFilepaths.GENERATED, os.path.join(os.getcwd(), "zentra", "generated")
        )


class TestZentraGeneratedFilepaths(unittest.TestCase):
    def test_root_path(self):
        self.assertEqual(ZentraGeneratedFilepaths.ROOT, ZentaFilepaths.GENERATED)

    def test_components_path(self):
        self.assertEqual(
            ZentraGeneratedFilepaths.COMPONENTS,
            os.path.join(ZentaFilepaths.GENERATED, "components"),
        )

    def test_zentra_path(self):
        self.assertEqual(
            ZentraGeneratedFilepaths.ZENTRA,
            os.path.join(ZentraGeneratedFilepaths.COMPONENTS, "zentra"),
        )


class TestZentraUIFilepaths(unittest.TestCase):
    def test_root_path(self):
        expected_path = os.path.join(ZentraGeneratedFilepaths.ZENTRA, "ui")
        self.assertEqual(ZentraUIFilepaths.ROOT, expected_path)

    def test_base_path(self):
        expected_path = os.path.join(ZentraUIFilepaths.ROOT, "base")
        self.assertEqual(ZentraUIFilepaths.BASE, expected_path)

    def test_control_path(self):
        expected_path = os.path.join(ZentraUIFilepaths.ROOT, "control")
        self.assertEqual(ZentraUIFilepaths.CONTROL, expected_path)

    def test_modal_path(self):
        expected_path = os.path.join(ZentraUIFilepaths.ROOT, "modal")
        self.assertEqual(ZentraUIFilepaths.MODAL, expected_path)

    def test_navigation_path(self):
        expected_path = os.path.join(ZentraUIFilepaths.ROOT, "navigation")
        self.assertEqual(ZentraUIFilepaths.NAVIGATION, expected_path)

    def test_notification_path(self):
        expected_path = os.path.join(ZentraUIFilepaths.ROOT, "notification")
        self.assertEqual(ZentraUIFilepaths.NOTIFICATION, expected_path)

    def test_presentation_path(self):
        expected_path = os.path.join(ZentraUIFilepaths.ROOT, "presentation")
        self.assertEqual(ZentraUIFilepaths.PRESENTATION, expected_path)
