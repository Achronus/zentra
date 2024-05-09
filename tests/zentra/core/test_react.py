import pytest

from tests.mappings.ui_imports import REACT_VALID_IMPORTS
from tests.mappings.ui_vals import LUCIDE_ICON_VALID_VALS
from tests.templates.helper import icon_builder
from zentra.core.react import LucideIcon, LucideIconWithText

from pydantic import ValidationError


class Builder:
    """A helper class that handles the logic for keeping `LucideIcon` model test implementations unified."""

    def __init__(self, model: LucideIcon | LucideIconWithText) -> None:
        self.model = model
        self.builder = icon_builder(model=model)

    def content(self, valid_value: str):
        result, _ = self.builder.build()
        assert "\n".join(result) == valid_value, (result, valid_value.split("\n"))

    def import_str(self, valid_value: str):
        _, result = self.builder.build()
        assert result == valid_value, (result, valid_value)


class TestLucideIcon:
    @pytest.fixture
    def italic_icon(self) -> LucideIcon:
        return LucideIcon(name="Italic")

    @pytest.fixture
    def italic_icon_full(self) -> LucideIcon:
        return LucideIcon(name="Italic", size=24, color="red", stroke_width=2)

    @pytest.fixture
    def wrapper(self, italic_icon: LucideIcon) -> Builder:
        return Builder(italic_icon)

    @pytest.fixture
    def wrapper_full(self, italic_icon_full: LucideIcon) -> Builder:
        return Builder(italic_icon_full)

    @staticmethod
    def test_content_simple(wrapper: Builder):
        wrapper.content(LUCIDE_ICON_VALID_VALS["content"]["simple"])

    @staticmethod
    def test_content_full(wrapper_full: Builder):
        wrapper_full.content(LUCIDE_ICON_VALID_VALS["content"]["full_no_text"])

    @staticmethod
    def test_import_str_italic(wrapper: Builder):
        wrapper.import_str(REACT_VALID_IMPORTS["lucide_icon"]["italic"])

    @staticmethod
    def test_import_str_loader():
        builder = Builder(model=LucideIcon(name="Loader"))
        builder.import_str(REACT_VALID_IMPORTS["lucide_icon"]["loader"])

    @staticmethod
    def test_name_invalid():
        with pytest.raises(ValidationError):
            LucideIcon(name="test Me")


class TestLucideIconWithText:
    @pytest.fixture
    def italic_icon(self) -> LucideIconWithText:
        return LucideIconWithText(name="Italic")

    @pytest.fixture
    def italic_icon_text(self) -> LucideIconWithText:
        return LucideIconWithText(name="Italic", text="test tag")

    @pytest.fixture
    def italic_icon_param(self) -> LucideIconWithText:
        return LucideIconWithText(name="Italic", text="test $tag")

    @pytest.fixture
    def italic_icon_position(self) -> LucideIconWithText:
        return LucideIconWithText(name="Italic", text="test tag", position="end")

    @pytest.fixture
    def italic_icon_param_position(self) -> LucideIconWithText:
        return LucideIconWithText(name="Italic", text="test $tag", position="end")

    @pytest.fixture
    def italic_icon_full(self) -> LucideIconWithText:
        return LucideIconWithText(
            name="Italic",
            text="test $tag",
            position="end",
            size=24,
            color="red",
            stroke_width=2,
        )

    @staticmethod
    def test_content_simple(italic_icon: LucideIconWithText):
        builder = Builder(italic_icon)
        builder.content(LUCIDE_ICON_VALID_VALS["content"]["simple"])

    @staticmethod
    def test_content_text(italic_icon_text: LucideIconWithText):
        builder = Builder(italic_icon_text)
        builder.content(LUCIDE_ICON_VALID_VALS["content"]["text"])

    @staticmethod
    def test_content_text_param(italic_icon_param: LucideIconWithText):
        builder = Builder(italic_icon_param)
        builder.content(LUCIDE_ICON_VALID_VALS["content"]["text_param"])

    @staticmethod
    def test_content_text_position(italic_icon_position: LucideIconWithText):
        builder = Builder(italic_icon_position)
        builder.content(LUCIDE_ICON_VALID_VALS["content"]["text_end"])

    @staticmethod
    def test_content_text_param_position(
        italic_icon_param_position: LucideIconWithText,
    ):
        builder = Builder(italic_icon_param_position)
        builder.content(LUCIDE_ICON_VALID_VALS["content"]["text_param_end"])

    @staticmethod
    def test_content_full(italic_icon_full: LucideIconWithText):
        builder = Builder(italic_icon_full)
        builder.content(LUCIDE_ICON_VALID_VALS["content"]["full"])

    @staticmethod
    def test_import_str_italic(italic_icon: LucideIconWithText):
        builder = Builder(italic_icon)
        builder.import_str(REACT_VALID_IMPORTS["lucide_icon"]["italic"])

    @staticmethod
    def test_import_str_loader():
        builder = Builder(model=LucideIconWithText(name="Loader"))
        builder.import_str(REACT_VALID_IMPORTS["lucide_icon"]["loader"])

    @staticmethod
    def test_name_invalid():
        with pytest.raises(ValidationError):
            LucideIconWithText(name="test Me")
