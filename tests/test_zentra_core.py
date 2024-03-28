from pydantic import ValidationError
import pytest
from zentra.core import Zentra, Page, Component


class TestComponent:
    @staticmethod
    def test_attr_str():
        assert Component().attr_str() is None

    @staticmethod
    def test_content_str():
        assert Component().content_str() is None

    @staticmethod
    def test_unique_logic_str():
        assert Component().unique_logic_str() is None

    @staticmethod
    def test_below_content_str():
        assert Component().below_content_str() is None


class TestZentra:
    @pytest.fixture
    def zentra(self) -> Zentra:
        return Zentra()

    def test_init(self, zentra: Zentra):
        assert zentra.pages == []
        assert zentra.components == []

    def test_init_fail(self):
        with pytest.raises(ValidationError):
            Zentra(pages=["test"])

    def test_page_registration(self, zentra: Zentra):
        page1 = Page(
            name="Page1",
            components=[
                Component(name="Component1"),
            ],
        )
        page2 = Page(
            name="Page2",
            components=[
                Component(name="Component2"),
            ],
        )
        page_map = [page1, page2]
        zentra.register(page_map)

        assert zentra.pages == page_map
        assert zentra.components == []

    def test_register_components(self, zentra: Zentra):
        component1 = Component(name="Component1")
        component2 = Component(name="Component2")
        standalone_components = [component1, component2]
        zentra.register(standalone_components)

        assert zentra.pages == []
        assert zentra.components == standalone_components

    def test_mixed_registration(self, zentra: Zentra):
        page = Page(
            name="Page1",
            components=[
                Component(name="Component1"),
            ],
        )
        component = Component(name="Component1")
        mixed_list = [page, component]
        zentra.register(mixed_list)

        assert zentra.pages == [page]
        assert zentra.components == [component]

    def test_register_invalid_input(self, zentra: Zentra):
        invalid_input = "InvalidInput"
        with pytest.raises(ValueError):
            zentra.register(invalid_input)
