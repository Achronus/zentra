import pytest

from tests.mappings.ui_imports import VALID_IMPORTS
from tests.mappings.ui_vals import VALID_VALS_MAP
from tests.templates.details import COMPONENT_DETAILS_MAPPING
from tests.templates.helper import SimpleCompBuilder

from zentra.ui.presentation import Separator


class TestSeparator:
    @pytest.fixture
    def separator(self) -> Separator:
        return Separator()

    @pytest.fixture
    def separator_full(self) -> Separator:
        return Separator(styles="mx-4", orientation="horizontal")

    @pytest.fixture
    def wrapper(self, separator: Separator) -> SimpleCompBuilder:
        return SimpleCompBuilder(separator, COMPONENT_DETAILS_MAPPING["Separator"])

    @pytest.fixture
    def wrapper_full(self, separator_full: Separator) -> SimpleCompBuilder:
        return SimpleCompBuilder(separator_full, COMPONENT_DETAILS_MAPPING["Separator"])

    @staticmethod
    def test_content_str(wrapper: SimpleCompBuilder):
        wrapper.run("content", VALID_VALS_MAP["separator"]["content"]["simple"])

    @staticmethod
    def test_content_str_full(wrapper_full: SimpleCompBuilder):
        wrapper_full.run("content", VALID_VALS_MAP["separator"]["content"]["full"])

    @staticmethod
    def test_import_str(wrapper: SimpleCompBuilder):
        wrapper.run("imports", VALID_IMPORTS["separator"])
