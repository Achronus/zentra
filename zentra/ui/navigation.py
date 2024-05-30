from typing import Optional

from pydantic import Field, ValidationInfo, field_validator
from pydantic_core import PydanticCustomError

from zentra.core import Component
from zentra.core.constants import LOWER_CAMELCASE_SINGLE_WORD
from zentra.core.enums.ui import BCTriggerVariant
from zentra.core.react import LucideIcon, LucideIconWithText
from zentra.custom.ui import SeparatorModel
from zentra.nextjs import Link
from zentra.ui import ShadcnUi
from zentra.ui.control import Button
from zentra.validation import (
    check_kebab_case,
    check_pattern_match,
    local_url_validation,
)
from zentra.validation.component import ddm_radio_group_validation


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
    A helper Zentra model for the [Shadcn/ui DropdownMenu](https://ui.shadcn.com/docs/components/dropdown-menu) component. Represents a single sub-menu group.

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
        texts = info.data.get("texts")
        return ddm_radio_group_validation(values, texts)


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

    @property
    def child_names(self) -> list[str]:
        return [
            "DropdownMenuTrigger",
            "DropdownMenuContent",
            "DropdownMenuItem",
            "DropdownMenuCheckboxItem",
            "DropdownMenuRadioItem",
            "DropdownMenuLabel",
            "DropdownMenuSeparator",
            "DropdownMenuShortcut",
            "DropdownMenuGroup",
            "DropdownMenuPortal",
            "DropdownMenuSub",
            "DropdownMenuSubContent",
            "DropdownMenuSubTrigger",
            "DropdownMenuRadioGroup",
        ]


class ContextMenu(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui ContextMenu](https://ui.shadcn.com/docs/components/context-menu) component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class CommandItem(DDMItem, ShadcnUi):
    """
    A helper Zentra model for the [Shadcn/ui Command](https://ui.shadcn.com/docs/components/command) component. Represents a single menu item.

    Cannot be used on its own, must be used inside a `zentra.ui.navigation.CommandGroup` model.

    Parameters:
    - `text` (`string | zentra.nextjs.Link`) - the text or `Link` model to display in the menu item. When `Link` model, `Link.text` and `Link.href` attributes are required
    - `icon` (`zentra.core.react.LucideIcon, optional`) - a [Lucide React Icon](https://lucide.dev/icons) added before the text. `None` by default
    - `shortcut_key` (`string, optional`) - the shortcut key for the menu item. `None` by default
    - `disabled` (`boolean, optional`) - adds the disabled property, preventing it from being clicked. `False` by default
    """


class CommandMap(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui Command](https://ui.shadcn.com/docs/components/command) component. Represents a `CommandItem` mapping for a single `CommandGroup`.

    Cannot be used on its own, must be used inside a `zentra.ui.navigation.Command` model.

    Parameters:
    - `obj_name` (`string`) - the name of the data object array to iterate over. Must be `lowercase` or `camelCase`, a `single word`, and up to a maximum of `20` characters
    - `param_name` (`string`) - the name of the parameter to iterate over inside the map. Must be `lowercase` or `camelCase`, a `single word`, and up to a maximum of `20` characters
    - `text` (`string`) - the descriptive text to put into the `CommandItem`. Can include parameter variables (indicated by starting the variable name with a `$.`)
    """

    obj_name: str = Field(min_length=1, max_length=20)
    param_name: str = Field(min_length=1, max_length=20)
    text: str

    @field_validator("obj_name", "param_name")
    def validate_name(cls, v: str) -> str:
        return check_pattern_match(
            LOWER_CAMELCASE_SINGLE_WORD,
            v,
            err_msg=f"'{v}'. Must be 'lowercase' or 'camelCase', a single word and a maximum of '20' characters\n",
        )


class CommandGroup(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui Command](https://ui.shadcn.com/docs/components/command) component. Represents a single menu group.

    Cannot be used on its own, must be used inside a `zentra.ui.navigation.Command` model.

    Parameters:
    - `items` (`list[string | zentra.ui.navigation.CommandItem]`) - a list of `strings` and/or `CommandItem` models
    - `heading` (`string, optional`) - The title displayed at the top of the menu group. `None` by default
    """

    items: list[str | CommandItem]
    heading: Optional[str] = None


class Command(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui Command](https://ui.shadcn.com/docs/components/command) component.

    Parameters:
    - `items` (`zentra.ui.navigation.CommandGroup | list[zentra.ui.navigation.CommandGroup] | zentra.ui.navigation.CommandMap`) - can be either:
      1. A single `CommandGroup` model
      2. A list of `CommandGroup` models
      3. A `CommandMap` model. Use for iterating over an array of data
    - `input_text` (`string, optional`) - the placeholder text to display in the `CommandInput` search box. `Type a command or search...` by default
    - `styles` (`string, optional`) - a set of custom CSS classes to apply to the command component. Automatically adds them to `className`. `rounded-lg border shadow-md` by default
    """

    items: CommandGroup | list[CommandGroup] | CommandMap
    input_text: str = "Type a command or search..."
    styles: Optional[str] = "rounded-lg border shadow-md"

    @property
    def child_names(self) -> list[str]:
        return [
            "CommandDialog",
            "CommandInput",
            "CommandList",
            "CommandEmpty",
            "CommandGroup",
            "CommandItem",
            "CommandShortcut",
            "CommandSeparator",
        ]


class BCTrigger(Component, ShadcnUi):
    """
    A helper Zentra model that represents a unique dropdown menu trigger for the [Shadcn/ui Breadcrumb](https://ui.shadcn.com/docs/components/breadcrumb) component.

    Cannot be used on its own, must be used inside a `zentra.ui.navigation.BCDropdownMenu` model.

    Parameter:
    - `variant` (`string, optional`) - the type of trigger to use. Valid options: `['ellipsis', 'text']`. `ellipsis` by default
    - `text` (`string, optional`) - the text to use inside the trigger. Only usable when `variant='text'`. Populates the `DropdownMenuTrigger` with text and a `ChevronDown` icon after it. `None` by default
    """

    variant: BCTriggerVariant = "ellipsis"
    text: Optional[str] = None

    @field_validator("text")
    def validate_text(cls, text: str | None, info: ValidationInfo) -> str | None:
        variant = info.data.get("variant")
        if text and variant != "text":
            raise PydanticCustomError(
                "invalid_variant",
                "Cannot use the 'text' attribute without 'variant=" + "text" + "'\n",
                dict(wrong_value=variant),
            )

        return text

    @property
    def content_str(self) -> str | LucideIconWithText:
        """Defines the JSX content for the component."""
        styles = "h-4 w-4"

        if self.variant == "ellipsis":
            return f'<BreadcrumbEllipsis className="{styles}" />\n<span className="sr-only">Toggle menu</span>'
        elif self.variant == "text":
            return LucideIconWithText(
                name="chevron-down", text=self.text, position="end", styles=styles
            )


class BCItem(Component, ShadcnUi):
    """
    A helper Zentra model for the [Shadcn/ui Breadcrumb](https://ui.shadcn.com/docs/components/breadcrumb) component. Represents a single breadcrumb item (`BreadcrumbItem`).

    Cannot be used on its own, must be used inside a `zentra.ui.navigation.Breadcrumb`, or a `zentra.ui.navigation.BCDropdownMenu` model.

    Parameters:
    - `text` (`string`) - The text to display inside the link
    - `href` (`string`) - The URL to display inside the `href` property. Can only be a local URL and must start with a `/`
    """

    text: str
    href: str

    @field_validator("href")
    def validate_url(cls, href: str) -> str:
        return local_url_validation(href)


class BCDropdownMenu(Component, ShadcnUi):
    """
    A helper Zentra model for the [Shadcn/ui Breadcrumb](https://ui.shadcn.com/docs/components/breadcrumb) component. Represents a dropdown menu unique to the breadcrumb component.

    Cannot be used on its own, must be used inside a `zentra.ui.navigation.Breadcrumb` model.

    Parameters:
    - `trigger` (`zentra.ui.navigation.BCTrigger`) - a Zentra `BCTrigger` model
    - `items` (`list[zentra.ui.navigation.BCItem]`) - a list of breadcrumb items
    """

    trigger: BCTrigger
    items: list[BCItem]


class Breadcrumb(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui Breadcrumb](https://ui.shadcn.com/docs/components/breadcrumb) component.

    Parameters:
    - `page_name` (`str`) - the name of the current resource, added as the last item inside a `BreadcrumbPage` child component
    - `items` (`list[zentra.ui.navigation.BCItem | zentra.ui.navigation.BCDropdownMenu]`) - a list of `BCItem` models and/or `BCDropdownMenu` models. Automatically adds a separator between each item
    - `custom_sep` (`string, optional`) - the name of a custom separator pulled from [Lucide React Icons](https://lucide.dev/icons). Must be in kebab-case format. E.g., `slash` or `move-right`. `None` by default
    """

    page_name: str
    items: list[BCItem | BCDropdownMenu]
    custom_sep: Optional[str] = None

    @property
    def child_names(self) -> list[str]:
        return [
            "BreadcrumbList",
            "BreadcrumbItem",
            "BreadcrumbLink",
            "BreadcrumbPage",
            "BreadcrumbSeparator",
            "BreadcrumbEllipsis",
        ]

    @property
    def separator_content(self) -> str | list[str]:
        """Defines the separator content for the component."""
        if self.custom_sep:
            return SeparatorModel(variant="breadcrumb", full=True).content_str

        return SeparatorModel(variant="breadcrumb").content_str

    @field_validator("custom_sep")
    def validate_custom_sep(cls, name: str) -> str:
        return check_kebab_case(name)
