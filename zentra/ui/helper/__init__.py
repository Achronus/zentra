from typing import Optional

from zentra.core import Component
from zentra.core.enums.ui import (
    ContentVariant,
    LabelVariant,
    SeparatorVariant,
    TriggerVariant,
)
from zentra.core.utils import name_to_pascal_case, str_to_list

from zentra.ui import ShadcnUi
from zentra.ui.helper.utils import full_container, simple_container, str_attr


class SeparatorModel(Component, ShadcnUi):
    """
    A helper model that acts as a drop in replacement for `Separator` components in the [Shadcn/ui](https://ui.shadcn.com/) component library, such as `BreadcrumbSeparator` or `DropdownMenuSeparator`.

    Parameters:
    - `variant` (`string`) - defines the type of separator to create. Valid options: `['breadcrumb', 'dropdown_menu', 'menubar', 'command', 'context_menu']`. Each option applies a different name to the separator which are converted to `PascalCase` and appended with `Separator`.
    - `styles` (`string, optional`) - a set of custom CSS classes to apply to the separator. Automatically adds them to `className`. `None` by default
    """

    variant: SeparatorVariant
    styles: Optional[str] = None

    @property
    def container_name(self) -> str:
        return f"{name_to_pascal_case(self.variant)}Separator"

    def build(self, content: str | list[str] = None) -> list[str]:
        """Creates the JSX content for the component."""
        attrs = str_attr("className", self.styles) if self.styles else None

        if content:
            return str_to_list(
                full_container(self.container_name, content, attrs=attrs)
            )

        return str_to_list(simple_container(self.container_name, attrs=attrs))


class TriggerModel(Component, ShadcnUi):
    """
    A helper model that acts as a drop in replacement for `Trigger` components in the [Shadcn/ui](https://ui.shadcn.com/) component library, such as `AccordionTrigger` or `DropdownMenuTrigger`.

    Parameters:
    - `variant` (`string`) - defines the type of separator to create. Valid options: `['accordion', 'alert_dialog', 'collapsible', 'dropdown_menu', 'popover', 'select', 'tooltip']`. Each option applies a different name to the separator which are converted to `PascalCase` and appended with `Trigger`.
    """

    variant: TriggerVariant

    @property
    def container_name(self) -> str:
        return f"{name_to_pascal_case(self.variant)}Trigger"

    def build(self, content: str | list[str], attrs: str = None) -> list[str]:
        """Creates the JSX content for the component."""
        return str_to_list(full_container(self.container_name, content, attrs=attrs))


class LabelModel(Component, ShadcnUi):
    """
    A helper model that acts as a drop in replacement for `Label` components in the [Shadcn/ui](https://ui.shadcn.com/) component library, such as `DropdownMenuLabel`.

    Parameters:
    - `variant` (`string`) - defines the type of separator to create. Valid options: `['context_menu', 'dropdown_menu']`. Each option applies a different name to the separator which are converted to `PascalCase` and appended with `Label`.
    """

    variant: LabelVariant

    @property
    def container_name(self) -> str:
        return f"{name_to_pascal_case(self.variant)}Label"

    def build(self, content: str | list[str]) -> list[str]:
        """Creates the JSX content for the component."""
        return str_to_list(full_container(self.container_name, content))


class ContentModel(Component, ShadcnUi):
    """
    A helper model that acts as a drop in replacement for `Content` components in the [Shadcn/ui](https://ui.shadcn.com/) component library, such as `DropdownMenuContent`.

    Parameters:
    - `variant` (`string`) - defines the type of separator to create. Valid options: `['context_menu', 'dropdown_menu']`. Each option applies a different name to the separator which are converted to `PascalCase` and appended with `Content`.
    - `styles` (`string, optional`) - a set of custom CSS classes to apply to the separator. Automatically adds them to `className`. `None` by default
    """

    variant: ContentVariant
    styles: Optional[str] = None

    @property
    def container_name(self) -> str:
        return f"{name_to_pascal_case(self.variant)}Content"

    def build(self, content: str | list[str] = None) -> list[str]:
        """Creates the JSX content for the component."""
        attrs = str_attr("className", self.styles) if self.styles else None

        if content:
            return str_to_list(
                full_container(self.container_name, content, attrs=attrs)
            )

        return str_to_list(simple_container(self.container_name, attrs=attrs))
