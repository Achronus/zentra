from pydantic import ValidationError
import pytest

from tests.mappings.ui_imports import REACT_VALID_IMPORTS
from tests.mappings.ui_vals import LUCIDE_ICON_VALID_VALS
from tests.templates.helper import build_controller
from zentra.core.react import LucideIcon


class TestLucideIcon:
    @staticmethod
    def test_content_simple():
        result, _ = build_controller().build_icon(model=LucideIcon(name="Italic"))
        assert result[0] == LUCIDE_ICON_VALID_VALS["content"]["simple"]

    @staticmethod
    def test_content_text():
        result, _ = build_controller().build_icon(
            model=LucideIcon(name="Italic", text="test tag")
        )
        assert "\n".join(result) == LUCIDE_ICON_VALID_VALS["content"]["text"]

    @staticmethod
    def test_content_text_position():
        result, _ = build_controller().build_icon(
            model=LucideIcon(name="Italic", text="test tag", position="end")
        )
        assert "\n".join(result) == LUCIDE_ICON_VALID_VALS["content"]["text_end"]

    @staticmethod
    def test_content_text_param():
        result, _ = build_controller().build_icon(
            model=LucideIcon(name="Italic", text="test $tag")
        )
        assert "\n".join(result) == LUCIDE_ICON_VALID_VALS["content"]["text_param"]

    @staticmethod
    def test_content_text_param_position():
        result, _ = build_controller().build_icon(
            model=LucideIcon(name="Italic", text="test $tag", position="end")
        )
        assert "\n".join(result) == LUCIDE_ICON_VALID_VALS["content"]["text_param_end"]

    @staticmethod
    def test_import_str_italic():
        _, result = build_controller().build_icon(model=LucideIcon(name="Italic"))
        assert result == REACT_VALID_IMPORTS["lucide_icon"]["italic"]

    @staticmethod
    def test_import_str_loader():
        _, result = build_controller().build_icon(model=LucideIcon(name="Loader"))
        assert result == REACT_VALID_IMPORTS["lucide_icon"]["loader"]

    @staticmethod
    def test_name_invalid():
        with pytest.raises(ValidationError):
            LucideIcon(name="test Me")
