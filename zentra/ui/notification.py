import requests

from cli.conf.format import name_from_camel_case

from zentra.core import Component
from zentra.core.enums.ui import AlertVariant
from zentra.ui import ShadcnUi

from pydantic import Field, field_validator
from pydantic_core import PydanticCustomError


class Alert(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui Alert](https://ui.shadcn.com/docs/components/alert) component.

    Parameters:
    - `title` (`string`) - the text for the `AlertTitle`
    - `description` (`string`) - the text for the `AlertDescription`
    - `icon` (`string, optional`) - the name of the [Lucide React Icon](https://lucide.dev/icons). Must be in React format (Capitalised camelCase). E.g., `CircleArrowDown` or `Loader`. When provided, adds the icon to the start of the `Alert`. `None` by default
    - `variant` (`string, optional`) - the style of the alert. Valid options: `['default', 'destructive']`. `default` by default
    """

    title: str = Field(min_length=1)
    description: str = Field(min_length=1)
    icon: str = None
    variant: AlertVariant = "default"

    @field_validator("icon")
    def validate_icon(cls, icon: str) -> str:
        icon_name = name_from_camel_case(icon)
        response = requests.get(f"https://lucide.dev/icons/{icon_name}")

        if response.status_code != 200:
            raise PydanticCustomError(
                "invalid_icon",
                f"'{icon}' at '{response.url}' does not exist",
                dict(wrong_value=icon, error_code=response.status_code),
            )

        return icon


class AlertDialog(Component, ShadcnUi):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) AlertDialog component.

    Parameters:
    - `name` (`str`) - the name of the component
    """

    title: str = None
    description: str = None
    content: list[Component] | str = None
    footer: list[Component] | str = None
    trigger: list[Component] | str = None


class Sonner(Component, ShadcnUi):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Sonner component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class Toast(Component, ShadcnUi):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Toast component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class Tooltip(Component, ShadcnUi):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Tooltip component.

    Parameters:
    - `name` (`str`) - the name of the component
    """
