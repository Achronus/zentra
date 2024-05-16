from typing import Optional

from pydantic import ValidationInfo, field_validator
from pydantic_core import PydanticCustomError

from zentra.core import Component
from zentra.core.react import LucideIcon
from zentra.custom.ui import SeparatorModel
from zentra.nextjs import Link
from zentra.ui import ShadcnUi
from zentra.ui.control import Button


class Menubar(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui Menubar](https://ui.shadcn.com/docs/components/menubar) component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class NavigationMenu(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui NavigationMenu](https://ui.shadcn.com/docs/components/navigation-menu) component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class DDMItem(Component, ShadcnUi):
    """
    A helper Zentra model for the [Shadcn/ui DropdownMenu](https://ui.shadcn.com/docs/components/dropdown-menu) component. Represents a single menu item.

    Cannot be used on its own, must be used inside a `zentra.ui.navigation.DDMGroup` or `zentra.ui.navigation.DDMSubGroup` model.

    Parameters:
    - `text` (`string | zentra.nextjs.Link`) - the text or `Link` model to display in the menu item. When `Link` model, `Link.text` and `Link.href` attributes are required
    - `icon` (`zentra.core.react.LucideIcon, optional`) - a [Lucide React Icon](https://lucide.dev/icons) added before the text. `None` by default
    - `shortcut_key` (`string, optional`) - the shortcut key for the menu item. `None` by default
    - `disabled` (`boolean, optional`) - adds the disabled property, preventing it from being clicked. `False` by default
    """

    text: str | Link
    icon: Optional[LucideIcon] = None
    shortcut_key: Optional[str] = None
    disabled: bool = False

    @field_validator("text")
    def validate_link(cls, text: str | Link) -> str | Link:
        if isinstance(text, Link) and not text.text:
            raise PydanticCustomError(
                "link_text_required",
                f"cannot have 'text=None' for 'Link' model in 'DDMItems'. Model error: '{repr(text)}'\n",
                dict(wrong_value=text.text, wrong_model=repr(text)),
            )

        return text


class DDMSeparator(Component, ShadcnUi):
    """
    A helper Zentra model for the [Shadcn/ui DropdownMenu](https://ui.shadcn.com/docs/components/dropdown-menu) component. Represents a dropdown menu separator (`DropdownMenuSeparator`) child component.

    Cannot be used on its own, must be used inside a `zentra.ui.navigation.DDMGroup`, or `zentra.ui.navigation.DDMSubGroup` model.
    """

    @property
    def content_str(self) -> str:
        """Provides the JSX content for the component."""
        return SeparatorModel(variant="dropdown_menu").content_str


class DDMSubGroup(Component, ShadcnUi):
    """
    A helper Zentra model for the [Shadcn/ui DropdownMenu](https://ui.shadcn.com/docs/components/dropdown-menu) component. Represents a single sub-menu group for the `DropdownMenuSub` child component.

    Cannot be used on its own, must be used inside a `zentra.ui.navigation.DDMGroup` model.

    Parameters:
    - `trigger` (`zentra.ui.navigation.DDMItem`) - the main `DDMItem` that acts as the entry point to the sub-menu
    - `items` (`list[string | zentra.ui.navigation.DDMSeparator] | list[zentra.ui.navigation.DDMItem | zentra.ui.navigation.DDMSeparator]`) - Can be either:
      1. A list of `strings` and/or a `DDMSeparator` model
      2. A list of `DDMItem` models and/or a `DDMSeparator` model
    - `label` (`string, optional`) - The label displayed at the top of the menu group. `None` by default
    """

    trigger: DDMItem
    items: list[str | DDMSeparator] | list[DDMItem | DDMSeparator]
    label: Optional[str] = None


class DDMGroup(Component, ShadcnUi):
    """
    A helper Zentra model for the [Shadcn/ui DropdownMenu](https://ui.shadcn.com/docs/components/dropdown-menu) component. Represents a single menu group.

    Cannot be used on its own, must be used inside a `zentra.ui.navigation.DropdownMenu` model.

    Parameters:
    - `items` (`list[string | zentra.ui.navigation.DDMSeparator] | list[zentra.ui.navigation.DDMItem | zentra.ui.navigation.DDMSubGroup | zentra.ui.navigation.DDMSeparator]`) - Can be either:
      1. A list of `strings` and/or `DDMSeparator` models
      2. A list of `DDMItem` models, `DDMSubGroup` models, and/or `DDMSeparator` models
    - `label` (`string, optional`) - The label displayed at the top of the menu group. `None` by default
    """

    items: list[str | DDMSeparator] | list[DDMItem | DDMSubGroup | DDMSeparator]
    label: Optional[str] = None


class DDMCheckboxGroup(Component, ShadcnUi):
    """
    A helper Zentra model for the [Shadcn/ui DropdownMenu](https://ui.shadcn.com/docs/components/dropdown-menu) component with checkboxes. Represents a single checkbox item.

    Cannot be used on its own, must be used inside a `zentra.ui.navigation.DropdownMenu` model.

    Parameters:
    - `texts` (`list[string]`) - a list of strings for each `DropdownMenuCheckboxItem`. Acts as the text displayed in the `RadioItem`
    """

    texts: list[str]

    @property
    def state_name_pairs(self) -> list[tuple[str, str]]:
        """Defines the hook state name pairs `(get, set)` for each `CheckboxItem` based on the given text. Uses the first two words as a unique identifier for each one."""
        pairs = []
        for item in self.texts:
            name = "".join([item.capitalize() for item in item.split(" ")[:2]])
            pairs.append((f"ddCheckboxShow{name}", f"ddCheckboxSetShow{name}"))

        return pairs


class DDMRadioGroup(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui DropdownMenu](https://ui.shadcn.com/docs/components/dropdown-menu#radio-group) component with a radio group. Represents a complete radio group.

    Cannot be used on its own, must be used inside a `zentra.ui.navigation.DropdownMenu` model.

    Parameters:
    - `texts` (`list[string]`) - a list of strings for each `DropdownMenuRadioItem`. Acts as the text displayed in the `RadioItem`
    - `values` (`list[string], optional`) - an optional list of values for each `item` in the `items` list. Adds the `value` prop to each item in the respective index. `None` by default. When `None` automatically uses a lowercase variant of the first word in each `item`

    Note: `items` and `values` must match in size if `values` is provided.
    """

    texts: list[str]
    values: Optional[list[str]] = None

    @property
    def state_name_pairs(self) -> list[tuple[str, str]]:
        """Defines the hook state name pairs `(get, set)` for each `RadioItem` based on the given text. Uses the first two words as a unique identifier for each one."""
        pairs = []
        for item in self.texts:
            name = "".join([item.capitalize() for item in item.split(" ")[:2]])
            pairs.append((f"dd{name}", f"ddSet{name}"))

        return pairs

    @field_validator("values")
    def validate_items_values(
        cls, values: list[str], info: ValidationInfo
    ) -> list[str]:
        items = info.data.get("items")
        if values is not None and len(items) != len(values):
            raise PydanticCustomError(
                "size_mismatch",
                f"'items' and 'values' must match in size -> 'items={len(items)} != values={len(values)}'\n",
                dict(items_size=len(items), values_size=len(values)),
            )
        return items


class DropdownMenu(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui DropdownMenu](https://ui.shadcn.com/docs/components/dropdown-menu) component.

    Parameters:
    - `trigger` (`zentra.ui.control.Button | string`) - The item to activate the dropdown menu. Can be either:
      1. A Zentra `Button` model
      2. A string of text
    - `items` (`zentra.ui.navigation.DDMGroup | zentra.ui.navigation.DDMRadioGroup | zentra.ui.navigation.DDMCheckboxGroup | list[zentra.ui.navigation.DDMGroup]`) - Can be either:
      1. A `DDMGroup` model. For a single group of dropdown menu items. These can be either `strings` or `DDMItem` models
      2. A `DDMRadioGroup` model containing a list of radio items
      3. A `DDMCheckboxGroup` model containing a list of checkbox items
      4. A list of `DDMGroup` models. For multiple groups of dropdown items, automatically separated by a `DropdownMenuSeparator`
    - `label` (`string, optional`) - The main label displayed at the top of the dropdown menu. `None` by default
    """

    trigger: Button | str
    items: DDMGroup | DDMRadioGroup | DDMCheckboxGroup | list[DDMGroup]
    label: Optional[str] = None


class ContextMenu(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui ContextMenu](https://ui.shadcn.com/docs/components/context-menu) component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class Command(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui Command](https://ui.shadcn.com/docs/components/command) component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class Breadcrumb(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui Breadcrumb](https://ui.shadcn.com/docs/components/breadcrumb) component.

    Parameters:
    - `name` (`str`) - the name of the component
    """
