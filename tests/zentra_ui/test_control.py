import pytest
from pydantic import BaseModel, ValidationError

from zentra.core.enums.ui import ButtonIconPosition, ButtonVariant


class ButtonModel(BaseModel):
    variant: ButtonVariant
    icon_position: ButtonIconPosition


def test_button_variant_valid():
    data = {"text": "test", "variant": "default", "icon_position": "start"}
    button_instance = ButtonModel(**data)
    assert button_instance.variant == ButtonVariant.DEFAULT


def test_button_icon_position_valid():
    data = {"text": "test", "variant": "default", "icon_position": "end"}
    button_instance = ButtonModel(**data)
    assert button_instance.icon_position == ButtonIconPosition.END


def test_button_variant_invalid():
    with pytest.raises(ValidationError):
        data = {"text": "test", "variant": "invalid_variant", "icon_position": "start"}
        ButtonModel(**data)


def test_button_icon_position_invalid():
    with pytest.raises(ValidationError):
        data = {
            "text": "test",
            "variant": "secondary",
            "icon_position": "invalid_position",
        }
        ButtonModel(**data)
