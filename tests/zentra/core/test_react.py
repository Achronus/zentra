import pytest

from tests.mappings.ui_imports import REACT_VALID_IMPORTS
from tests.mappings.ui_vals import LUCIDE_ICON_VALID_VALS
from tests.templates.helper import build_controller
from zentra.core.react import LucideIcon, LucideIconWithText

from pydantic import ValidationError


class TestLucideIcon:
    @pytest.fixture
    def italic_icon(self) -> LucideIcon:
        return LucideIcon(name="Italic")

    @pytest.fixture
    def italic_icon_full(self) -> LucideIcon:
        return LucideIcon(name="Italic", size=24, color="red", stroke_width=2)

    @staticmethod
    def test_content_simple(italic_icon: LucideIcon):
        result, _ = build_controller().build_icon(italic_icon)
        assert result[0] == LUCIDE_ICON_VALID_VALS["content"]["simple"]

    @staticmethod
    def test_content_full(italic_icon_full: LucideIcon):
        result, _ = build_controller().build_icon(italic_icon_full)
        assert "\n".join(result) == LUCIDE_ICON_VALID_VALS["content"]["full_no_text"]

    @staticmethod
    def test_import_str_italic(italic_icon: LucideIcon):
        _, result = build_controller().build_icon(italic_icon)
        assert result == REACT_VALID_IMPORTS["lucide_icon"]["italic"]

    @staticmethod
    def test_import_str_loader():
        _, result = build_controller().build_icon(model=LucideIcon(name="Loader"))
        assert result == REACT_VALID_IMPORTS["lucide_icon"]["loader"]

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
        result, _ = build_controller().build_icon(italic_icon)
        assert result[0] == LUCIDE_ICON_VALID_VALS["content"]["simple"]

    @staticmethod
    def test_content_text(italic_icon_text: LucideIconWithText):
        result, _ = build_controller().build_icon(italic_icon_text)
        assert "\n".join(result) == LUCIDE_ICON_VALID_VALS["content"]["text"]

    @staticmethod
    def test_content_text_param(italic_icon_param: LucideIconWithText):
        result, _ = build_controller().build_icon(italic_icon_param)
        assert "\n".join(result) == LUCIDE_ICON_VALID_VALS["content"]["text_param"]

    @staticmethod
    def test_content_text_position(italic_icon_position: LucideIconWithText):
        result, _ = build_controller().build_icon(italic_icon_position)
        assert "\n".join(result) == LUCIDE_ICON_VALID_VALS["content"]["text_end"]

    @staticmethod
    def test_content_text_param_position(
        italic_icon_param_position: LucideIconWithText,
    ):
        result, _ = build_controller().build_icon(italic_icon_param_position)
        assert "\n".join(result) == LUCIDE_ICON_VALID_VALS["content"]["text_param_end"]

    @staticmethod
    def test_content_full(italic_icon_full: LucideIconWithText):
        result, _ = build_controller().build_icon(italic_icon_full)
        assert "\n".join(result) == LUCIDE_ICON_VALID_VALS["content"]["full"]

    @staticmethod
    def test_import_str_italic(italic_icon: LucideIconWithText):
        _, result = build_controller().build_icon(italic_icon)
        assert result == REACT_VALID_IMPORTS["lucide_icon"]["italic"]

    @staticmethod
    def test_import_str_loader():
        _, result = build_controller().build_icon(
            model=LucideIconWithText(name="Loader")
        )
        assert result == REACT_VALID_IMPORTS["lucide_icon"]["loader"]

    @staticmethod
    def test_name_invalid():
        with pytest.raises(ValidationError):
            LucideIconWithText(name="test Me")
