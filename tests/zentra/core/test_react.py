import pytest

from tests.mappings.ui_imports import REACT_VALID_IMPORTS
from tests.mappings.ui_vals import LUCIDE_ICON_VALID_VALS
from tests.templates.helper import SimpleCompBuilder
from zentra_models.core.html import HTMLContent
from zentra_models.core.react import LucideIcon

from pydantic import ValidationError


class TestLucideIcon:
    @pytest.fixture
    def italic_icon(self) -> LucideIcon:
        return LucideIcon(name="italic")

    @pytest.fixture
    def italic_icon_text(self) -> LucideIcon:
        return LucideIcon(name="italic", text="test tag")

    @pytest.fixture
    def italic_icon_param(self) -> LucideIcon:
        return LucideIcon(name="italic", text="test $.tag")

    @pytest.fixture
    def italic_span_text(self) -> LucideIcon:
        return LucideIcon(
            name="italic",
            text=HTMLContent(tag="span", text="test $.tag"),
        )

    @pytest.fixture
    def italic_icon_full(self) -> LucideIcon:
        return LucideIcon(
            name="italic",
            text="test $.tag",
            size=24,
            color="red",
            stroke_width=2,
        )

    @staticmethod
    def test_content_simple(italic_icon: LucideIcon):
        builder = SimpleCompBuilder(italic_icon)
        builder.run("content", LUCIDE_ICON_VALID_VALS["content"]["simple"])

    @staticmethod
    def test_content_text(italic_icon_text: LucideIcon):
        builder = SimpleCompBuilder(italic_icon_text)
        builder.run("content", LUCIDE_ICON_VALID_VALS["content"]["text"])

    @staticmethod
    def test_content_text_param(italic_icon_param: LucideIcon):
        builder = SimpleCompBuilder(italic_icon_param)
        builder.run("content", LUCIDE_ICON_VALID_VALS["content"]["text_param"])

    @staticmethod
    def test_content_html_content_text(italic_span_text: LucideIcon):
        builder = SimpleCompBuilder(italic_span_text)
        builder.run("content", LUCIDE_ICON_VALID_VALS["content"]["html_content_text"])

    @staticmethod
    def test_content_full(italic_icon_full: LucideIcon):
        builder = SimpleCompBuilder(italic_icon_full)
        builder.run("content", LUCIDE_ICON_VALID_VALS["content"]["full"])

    @staticmethod
    def test_import_str_italic(italic_icon: LucideIcon):
        builder = SimpleCompBuilder(italic_icon)
        builder.run("imports", REACT_VALID_IMPORTS["lucide_icon"]["italic"])

    @staticmethod
    def test_import_str_loader():
        builder = SimpleCompBuilder(model=LucideIcon(name="loader"))
        builder.run("imports", REACT_VALID_IMPORTS["lucide_icon"]["loader"])

    @staticmethod
    def test_name_invalid():
        with pytest.raises(ValidationError):
            LucideIcon(name="test Me")
