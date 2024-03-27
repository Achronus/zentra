import pytest

from cli.templates.ui import JSXContainer


class TestJSXContainer:
    @pytest.fixture
    def root(self) -> JSXContainer:
        return JSXContainer()

    @staticmethod
    def test_attributes(root: JSXContainer):
        assert root.attributes() is None

    @staticmethod
    def test_unique_logic(root: JSXContainer):
        assert root.unique_logic() is None

    @staticmethod
    def test_main_content(root: JSXContainer):
        assert root.main_content() is None
