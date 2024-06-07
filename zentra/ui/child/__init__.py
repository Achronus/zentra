from enum import Enum
from typing import Optional, Union

from pydantic import Field, PrivateAttr, field_validator

from zentra.base import ZentraModel
from zentra.core import Component
from zentra.core.enums.child import (
    ContentVariant,
    DescriptionVariant,
    GroupVariant,
    ItemVariant,
    LabelVariant,
    SeparatorVariant,
    TitleVariant,
    TriggerVariant,
    ValueVariant,
)
from zentra.core.utils import name_to_pascal_case, str_to_list

from zentra.ui import ShadcnUi
from zentra.ui.control import Button
from zentra.ui.child.utils import full_container, simple_container, str_attr


class ChildModel(Component, ShadcnUi):
    """
    A base class for all child models.

    Parameters:
    - `variant` (`string`) - defines the type of model to create. Each option applying a different name to the model
    - `styles` (`string, optional`) - a set of custom CSS classes to apply to the model. Automatically adds them to `className`. `None` by default
    """

    variant: Enum
    styles: Optional[str] = Field(default=None, validate_default=True)

    _custom_common_attrs = PrivateAttr(default=["variant"])

    @property
    def name_prefix(self) -> str:
        return name_to_pascal_case(self.variant)


class SeparatorModel(ChildModel):
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


class ValueModel(ChildModel):
    """
    A child model for `Value` components in the [Shadcn/ui](https://ui.shadcn.com/) component library, such as `SelectValue`.

    Parameters:
    - `variant` (`string`) - defines the value of label to create. Valid options: `['select']`. Each option applies a different name to the label which are converted to `PascalCase` and appended with `Value`.
    - `placeholder` (`string`) - the placeholder text to display inside the label
    - `styles` (`string, optional`) - a set of custom CSS classes to apply to the label. Automatically adds them to `className`. `None` by default
    """

    variant: ValueVariant
    placeholder: str

    @property
    def container_name(self) -> str:
        return f"{self.name_prefix}Value"


class TriggerModel(ChildModel):
    """
    A child model for `Trigger` components in the [Shadcn/ui](https://ui.shadcn.com/) component library, such as `AccordionTrigger` or `DropdownMenuTrigger`.

    Parameters:
    - `variant` (`string`) - defines the type of trigger to create. Valid options: `['accordion', 'alert_dialog', 'collapsible', 'dropdown_menu', 'popover', 'select', 'tooltip']`. Each option applies a different name to the trigger which are converted to `PascalCase` and appended with `Trigger`
    - `styles` (`string, optional`) - a set of custom CSS classes to apply to the trigger. Automatically adds them to `className`. `None` by default
    - `content` (`zentra.ui.control.Button | string | zentra.ui.child.ValueModel`) - the item to add to the trigger. Can be either:
      1. A Zentra `Button` model
      2. A string of text
      3. A Zentra child `ValueModel` model
    - `child` (`boolean, optional`) - a flag to add the `asChild` prop to the trigger. `False` by default
    """

    variant: TriggerVariant
    content: Union[Button, str, ValueModel]
    child: bool = False

    @property
    def container_name(self) -> str:
        return f"{self.name_prefix}Trigger"

    @field_validator("content")
    def validate_content(
        cls, content: Union[Button, str, ValueModel]
    ) -> Union[list[Button | ValueModel], str]:
        if isinstance(content, str):
            return content
        else:
            return [content]

    def build(self, content: str | list[str], attrs: str = None) -> list[str]:
        """Creates the JSX content for the component."""
        return str_to_list(full_container(self.container_name, content, attrs=attrs))


class LabelModel(ChildModel):
    """
    A child model for `Label` components in the [Shadcn/ui](https://ui.shadcn.com/) component library, such as `DropdownMenuLabel`.

    Parameters:
    - `variant` (`string`) - defines the type of label to create. Valid options: `['context_menu', 'dropdown_menu', 'select']`. Each option applies a different name to the label which are converted to `PascalCase` and appended with `Label`.
    - `content` (`string`) - the content to display inside the label
    - `styles` (`string, optional`) - a set of custom CSS classes to apply to the label. Automatically adds them to `className`. `None` by default
    """

    variant: LabelVariant
    content: str

    @property
    def container_name(self) -> str:
        return f"{self.name_prefix}Label"

    def build(self, content: str | list[str]) -> list[str]:
        """Creates the JSX content for the component."""
        return str_to_list(full_container(self.container_name, content))


class ItemModel(ChildModel):
    """
    A child model for `Item` components in the [Shadcn/ui](https://ui.shadcn.com/) component library, such as `SelectItem`.

    Parameters:
    - `variant` (`string`) - defines the type of item to create. Valid options: `['select']`. Each option applies a different name to the item which are converted to `PascalCase` and appended with `Item`
    - `content` (`string`) - the content to display inside the item
    - `value` (`string, optional`) - the value to pass to the `value` prop. `None` by default
    - `styles` (`string, optional`) - a set of custom CSS classes to apply to the item. Automatically adds them to `className`. `None` by default
    """

    variant: ItemVariant
    content: str
    value: Optional[str] = None

    @property
    def container_name(self) -> str:
        return f"{self.name_prefix}Item"

    def build(self, content: str | list[str]) -> list[str]:
        """Creates the JSX content for the component."""
        return str_to_list(full_container(self.container_name, content))


class GroupModel(ChildModel):
    """
    A child model for `Group` components in the [Shadcn/ui](https://ui.shadcn.com/) component library, such as `SelectGroup`.

    Parameters:
    - `variant` (`string`) - defines the type of group to create. Valid options: `['dropdown_menu', 'select']`. Each option applies a different name to the group which are converted to `PascalCase` and appended with `Group`
    - `content` (`list[ZentraModel]`) - a list of `ZentraModels` to add as children
    - `styles` (`string, optional`) - a set of custom CSS classes to apply to the group. Automatically adds them to `className`. `None` by default
    """

    variant: GroupVariant
    content: list[ZentraModel]

    @property
    def container_name(self) -> str:
        return f"{self.name_prefix}Group"

    def build(self, content: str | list[str]) -> list[str]:
        """Creates the JSX content for the component."""
        return str_to_list(full_container(self.container_name, content))


class ContentModel(ChildModel):
    """
    A child model for `Content` components in the [Shadcn/ui](https://ui.shadcn.com/) component library, such as `DropdownMenuContent`.

    Parameters:
    - `variant` (`string`) - defines the type of content to create. Valid options: `['dropdown_menu', 'collapsible', 'select']`. Each option applies a different name to the content which are converted to `PascalCase` and appended with `Content`
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


class TitleModel(ChildModel):
    """
    A child model for `Title` components in the [Shadcn/ui](https://ui.shadcn.com/) component library, such as `AlertTitle`.

    Parameters:
    - `variant` (`string`) - defines the type of title to create. Valid options: `['alert']`. Each option applies a different name to the title which are converted to `PascalCase` and appended with `Content`
    - `styles` (`string, optional`) - a set of custom CSS classes to apply to the title. Automatically adds them to `className`. `None` by default
    - `content` (`string`) - the text to display inside the title
    """

    variant: TitleVariant
    content: str

    @property
    def container_name(self) -> str:
        return f"{self.name_prefix}Title"


class DescriptionModel(ChildModel):
    """
    A child model for `Description` components in the [Shadcn/ui](https://ui.shadcn.com/) component library, such as `AlertDescription`.

    Parameters:
    - `variant` (`string`) - defines the type of description to create. Valid options: `['alert']`. Each option applies a different name to the description which are converted to `PascalCase` and appended with `Content`
    - `styles` (`string, optional`) - a set of custom CSS classes to apply to the description. Automatically adds them to `className`. `None` by default
    - `content` (`string`) - the text to display inside the description
    """

    variant: DescriptionVariant
    content: str

    @property
    def container_name(self) -> str:
        return f"{self.name_prefix}Description"
