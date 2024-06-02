from enum import Enum
from typing import Optional

from pydantic import Field

from zentra.base import ZentraModel
from zentra.core.enums.ui import (
    ContentVariant,
    LabelVariant,
    SeparatorVariant,
    TriggerVariant,
)
from zentra.core.utils import name_to_pascal_case, str_to_list

from zentra.ui import ShadcnUi
from zentra.ui.control import Button
from zentra.ui.child.utils import full_container, simple_container, str_attr


class ChildModel(ZentraModel):
    """
    A base class for all child models.

    Parameters:
    - `variant` (`string`) - defines the type of model to create. Each option applying a different name to the model
    - `styles` (`string, optional`) - a set of custom CSS classes to apply to the model. Automatically adds them to `className`. `None` by default
    """

    variant: Enum
    styles: Optional[str] = Field(default=None, validate_default=True)

    @property
    def name_prefix(self) -> str:
        return name_to_pascal_case(self.variant)

    @property
    def custom_common_attributes(self) -> list[str]:
        return ["variant"]


class SeparatorModel(ChildModel, ShadcnUi):
    """
    A child model for `Separator` components in the [Shadcn/ui](https://ui.shadcn.com/) component library, such as `BreadcrumbSeparator` or `DropdownMenuSeparator`.

    Parameters:
    - `variant` (`string`) - defines the type of separator to create. Valid options: `['breadcrumb', 'dropdown_menu', 'menubar', 'command', 'context_menu']`. Each option applies a different name to the separator which are converted to `PascalCase` and appended with `Separator`
    - `styles` (`string, optional`) - a set of custom CSS classes to apply to the separator. Automatically adds them to `className`. `None` by default
    """

    variant: SeparatorVariant

    @property
    def container_name(self) -> str:
        return f"{self.name_prefix}Separator"

    def build(self, content: str | list[str] = None) -> list[str]:
        """Creates the JSX content for the component."""
        attrs = str_attr("className", self.styles) if self.styles else None

        if content:
            return str_to_list(
                full_container(self.container_name, content, attrs=attrs)
            )

        return str_to_list(simple_container(self.container_name, attrs=attrs))


class TriggerModel(ChildModel, ShadcnUi):
    """
    A child model for `Trigger` components in the [Shadcn/ui](https://ui.shadcn.com/) component library, such as `AccordionTrigger` or `DropdownMenuTrigger`.

    Parameters:
    - `variant` (`string`) - defines the type of trigger to create. Valid options: `['accordion', 'alert_dialog', 'collapsible', 'dropdown_menu', 'popover', 'select', 'tooltip']`. Each option applies a different name to the trigger which are converted to `PascalCase` and appended with `Trigger`
    - `styles` (`string, optional`) - a set of custom CSS classes to apply to the trigger. Automatically adds them to `className`. `None` by default
    - `content` (`zentra.ui.control.Button | string`) - the item to add to the trigger. Can be either:
      1. A Zentra `Button` model
      2. A string of text
    """

    variant: TriggerVariant
    content: Button | str

    @property
    def container_name(self) -> str:
        return f"{self.name_prefix}Trigger"

    def build(self, content: str | list[str], attrs: str = None) -> list[str]:
        """Creates the JSX content for the component."""
        return str_to_list(full_container(self.container_name, content, attrs=attrs))


class LabelModel(ChildModel, ShadcnUi):
    """
    A child model for `Label` components in the [Shadcn/ui](https://ui.shadcn.com/) component library, such as `DropdownMenuLabel`.

    Parameters:
    - `variant` (`string`) - defines the type of label to create. Valid options: `['context_menu', 'dropdown_menu']`. Each option applies a different name to the label which are converted to `PascalCase` and appended with `Label`.
    - `styles` (`string, optional`) - a set of custom CSS classes to apply to the label. Automatically adds them to `className`. `None` by default
    """

    variant: LabelVariant

    @property
    def container_name(self) -> str:
        return f"{self.name_prefix}Label"

    def build(self, content: str | list[str]) -> list[str]:
        """Creates the JSX content for the component."""
        return str_to_list(full_container(self.container_name, content))


class ContentModel(ChildModel, ShadcnUi):
    """
    A child model for `Content` components in the [Shadcn/ui](https://ui.shadcn.com/) component library, such as `DropdownMenuContent`.

    Parameters:
    - `variant` (`string`) - defines the type of content to create. Valid options: `['dropdown_menu', 'collapsible']`. Each option applies a different name to the content which are converted to `PascalCase` and appended with `Content`.
    - `styles` (`string, optional`) - a set of custom CSS classes to apply to the content. Automatically adds them to `className`. `None` by default
    - `content` (`list[ZentraModel]`) - a list of `ZentraModels` to add as children
    """

    variant: ContentVariant
    content: list[ZentraModel]

    @property
    def container_name(self) -> str:
        return f"{self.name_prefix}Content"

    def build(self, content: str | list[str] = None) -> list[str]:
        """Creates the JSX content for the component."""
        attrs = str_attr("className", self.styles) if self.styles else None

        if content:
            return str_to_list(
                full_container(self.container_name, content, attrs=attrs)
            )

        return str_to_list(simple_container(self.container_name, attrs=attrs))
