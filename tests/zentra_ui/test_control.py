import pytest
from pydantic import BaseModel, ValidationError

from zentra.core.enums.ui import ButtonIconPosition, ButtonVariant


class ButtonModel(BaseModel):
    variant: ButtonVariant
    icon_position: ButtonIconPosition


def test_button_variant_valid():
    data = {"name": "test", "variant": "primary", "icon_position": "start"}
    button_instance = ButtonModel(**data)
    assert button_instance.variant == ButtonVariant.primary


def test_button_icon_position_valid():
    data = {"name": "test", "variant": "primary", "icon_position": "end"}
    button_instance = ButtonModel(**data)
    assert button_instance.icon_position == ButtonIconPosition.end


def test_button_variant_invalid():
    with pytest.raises(ValidationError):
        data = {"name": "test", "variant": "invalid_variant", "icon_position": "start"}
        ButtonModel(**data)


def test_button_icon_position_invalid():
    with pytest.raises(ValidationError):
        data = {
            "name": "test",
            "variant": "primary",
            "icon_position": "invalid_position",
        }
        ButtonModel(**data)
