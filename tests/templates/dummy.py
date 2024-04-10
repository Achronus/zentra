from zentra.core import Component
from zentra.core.enums.ui import ButtonIconPosition, ButtonVariant, IconButtonSize
from zentra.ui import ShadcnUi

from pydantic import Field, HttpUrl, PrivateAttr


class DummyIconButton(Component, ShadcnUi):
    """A dummy button that uses the same markup as the IconButton but without requesting to the URL."""

    icon: str = Field(min_length=1)
    icon_position: ButtonIconPosition = "start"
    text: str = None
    url: HttpUrl = Field(default=None)
    variant: ButtonVariant = "default"
    size: IconButtonSize = "icon"
    disabled: bool = False

    _classname = PrivateAttr(default="Button")
