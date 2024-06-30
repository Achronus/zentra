from typing import Optional, Union

from zentra_models.base import ZentraModel
from zentra_models.core import Component
from zentra_models.core.enums.ui import AlertVariant
from zentra_models.core.react import LucideIcon, LucideIconWithText
from zentra_models.core.validation import check_kebab_case

from zentra_models.ui import ShadcnUi
from zentra_models.ui.control import Button

from pydantic import Field, PrivateAttr, field_validator


Flexible = Union[list[ZentraModel], ZentraModel, str]


class Alert(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui Alert](https://ui.shadcn.com/docs/components/alert) component.

    Parameters:
    - `title` (`string`) - the text for the `AlertTitle`
    - `description` (`string`) - the text for the `AlertDescription`
    - `icon` (`string, optional`) - the name of the [Lucide React Icon](https://lucide.dev/icons). Must be in kebab-case format. E.g., `circle-arrow-down` or `loader`. When provided, adds the icon to the start of the `Alert`. `None` by default
    - `variant` (`string, optional`) - the style of the alert. Valid options: `['default', 'destructive']`. `default` by default
    """

    title: str = Field(min_length=1)
    description: str = Field(min_length=1)
    icon: Optional[str] = None
    variant: AlertVariant = "default"

    @property
    def child_names(self) -> list[str]:
        return ["AlertTitle", "AlertDescription"]

    @field_validator("icon")
    def validate_icon(cls, icon: str) -> str:
        return check_kebab_case(icon)


class AlertDialog(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui AlertDialog](https://ui.shadcn.com/docs/components/alert-dialog) component.

    Parameters:
    - `trigger` (`zentra.models.ui.control.Button | string`) - the text or `Button` model to display in the `AlertDialogTrigger`
    - `header` (`list[ZentraModel] | ZentraModel | string, optional`) - content to add to the `AlertDialogHeader`. Can be a list of a single or combined set of the following `ZentraModels` or a string of text. Wrapped in a `AlertDialogContent` model automatically
    - `title` (`list[ZentraModel] | ZentraModel | string, optional`) - the text for the `AlertDialogTitle`. Acts the same as the `content` attribute, but in a different wrapper. Added above the `header`. `None` by default
    - `description` (`list[ZentraModel] | ZentraModel | string, optional`) - the text for the `AlertDialogDescription`. Acts the same as the `content` attribute, but in a different wrapper. Added under the `header`. `None` by default
    - `footer` (`list[ZentraModel] | ZentraModel | string, optional`) - the content to add to the `AlertDialogFooter`. Acts the same as the `content` attribute, but in a different wrapper. Added below the `header`. `None` by default
    - `cancel_btn` (`string, optional`) - the text to add inside the `AlertDialogCancel` added to the `AlertDialogFooter`. Usable with `footer`, appended after it, and `action_btn`, appended before it. `None` by default
    - `action_btn` (`string, optional`) - the text to add inside the `AlertDialogAction` added to the `AlertDialogFooter`. Usable with `footer`, appended after it, and `cancel_btn`, appended after it. `None` by default
    """

    trigger: Union[Button, str]
    header: Optional[Flexible] = None
    title: Optional[Flexible] = None
    description: Optional[Flexible] = None
    footer: Optional[Flexible] = None
    cancel_btn: Optional[str] = None
    action_btn: Optional[str] = None

    _content_attr = PrivateAttr(default="header")

    _child_names = PrivateAttr(
        default=[
            "AlertDialogPortal",
            "AlertDialogOverlay",
            "AlertDialogTrigger",
            "AlertDialogContent",
            "AlertDialogHeader",
            "AlertDialogFooter",
            "AlertDialogTitle",
            "AlertDialogDescription",
            "AlertDialogAction",
            "AlertDialogCancel",
        ]
    )


class Sonner(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui Sonner](https://ui.shadcn.com/docs/components/sonner) component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class Toast(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui Toast](https://ui.shadcn.com/docs/components/toast) component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class Tooltip(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui Tooltip](https://ui.shadcn.com/docs/components/tooltip) component.

    Parameters:
    - `text` (`str`) - the text to display inside the tooltip
    - `trigger` (`zentra.models.ui.control.Button | zentra.models.core.react.LucideIcon | zentra.models.core.react.LucideIconWithText | string`) - An item to apply the tooltip to. Can be either:
      1. A Zentra `Button` model
      2. A Zentra `LucideIcon` model
      3. A Zentra `LucideIconWithText` model
      4. A string of text
    """

    text: str
    trigger: Button | LucideIcon | LucideIconWithText | str

    _container_name = PrivateAttr(default="TooltipProvider")

    @property
    def custom_common_content(self) -> list[str]:
        return ["text"]

    @property
    def child_names(self) -> list[str]:
        return ["TooltipTrigger", "TooltipContent", "TooltipProvider"]
