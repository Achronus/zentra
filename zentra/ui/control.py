from pydantic import Field, HttpUrl
from zentra.core import Component, Icon
from zentra.core.enums.ui import (
    ButtonSize,
    ButtonVariant,
    ButtonIconPosition,
    IconButtonSize,
    InputTypes,
)


class Button(Component):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Button component focusing on text.

    Parameters:
    - `text` (`str`) - the text displayed inside the button
    - `url` (`str, optional`) - the URL the button links to. `None` by default. When `None` removes it from `Button`
    - `variant` (`str, optional`) - the style of the button. Valid options: `['default', 'secondary', 'destructive', 'outline', 'ghost', 'link']`. `default` by default
    - `size` (`str, optional`) - the size of the button. Valid options: `['default', 'sm', 'lg']`. `default` by default
    - `disabled` (`bool, optional`) - adds the disabled property, preventing it from being clicked. `False` by default
    """

    text: str = Field(min_length=1)
    url: HttpUrl = None
    variant: ButtonVariant = "default"
    size: ButtonSize = "default"
    disabled: bool = False

    def attr_str(self) -> str:
        attr_map = [
            (self.disabled, "disabled"),
            (self.url, f'href="{self.url}"'),
            (self.variant != ButtonVariant.DEFAULT, f'variant="{self.variant}"'),
            (self.size != ButtonSize.DEFAULT, f'size="{self.size}"'),
        ]
        return " " + Component.map_to_str(attr_map)

    def content_str(self) -> str:
        return self.text


class IconButton(Component):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Button component with a [Radix UI Icon](https://www.radix-ui.com/icons).

    Parameters:
    - `icon` (`Icon`) - the [Radix UI Icon](https://www.radix-ui.com/icons) to add inside the button
    - `icon_position` (`str, optional`) - the position of the icon inside the button. When set to `start`, icon appears before the text. When `end`, it appears after the text. `start` by default. Valid options: `['start', 'end']`
    - `text` (`str, optional`) - the text displayed inside the button. `None` by default. When `None` removes it from `Button`
    - `url` (`str, optional`) - the URL the button links to. `None` by default. When `None` removes it from `Button`
    - `variant` (`str, optional`) - the style of the button. Valid options: `['default', 'secondary', 'destructive', 'outline', 'ghost', 'link']`. `default` by default
    - `size` (`str, optional`) - the size of the button. Valid options: `['default', 'sm', 'lg', 'icon']`. `icon` by default
    - `disabled` (`bool, optional`) - adds the disabled property, preventing it from being clicked. `False` by default
    """

    icon: Icon
    icon_position: ButtonIconPosition = "start"
    text: str = None
    url: HttpUrl = Field(default=None)
    variant: ButtonVariant = "default"
    size: IconButtonSize = "icon"
    disabled: bool = False

    def attr_str(self) -> str:
        attr_map = [
            (self.disabled, "disabled"),
            (self.url, f'href="{self.url}"'),
            (self.variant != ButtonVariant.DEFAULT, f'variant="{self.variant}"'),
            (self.size != IconButtonSize.DEFAULT, f'size="{self.size}"'),
        ]
        return " " + Component.map_to_str(attr_map)

    def content_str(self) -> str:
        contents = []

        if self.text:
            contents.append(self.text)

        if self.icon:
            icon_html = f'<{self.icon.name} className="mr-2 h-4 w-4"/>'
            if self.icon_position == "start":
                contents.insert(0, icon_html)
            else:
                contents.append(icon_html)

        return " ".join(contents)


class Calendar(Component):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Calendar component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class Checkbox(Component):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Checkbox component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class Collapsible(Component):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Collapsible component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class Combobox(Component):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Combobox component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class DatePicker(Component):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) DatePicker component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class Input(Component):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Input component.

    Inputs are extremely versatile as expressed in the [HTML Input docs](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/url). We've limited the attributes to the basics for simplicity. Once components are generated, you can edit them in the respective `.tsx` files with additional attributes if needed.

    Parameters:
    - `type` (`str`) - the type of input field. Options `['text', 'email', 'password', 'number', 'file', 'tel', 'search', 'url', 'color']`
    - `placeholder` (`str`) - the placeholder text for the input
    - `read_only` (`bool, optional`) - a flag for setting the input to read only. Default is `False`
    """

    type: InputTypes
    placeholder: str
    read_only: bool = False


class Label(Component):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Label component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class RadioGroup(Component):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) RadioGroup component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class ScrollArea(Component):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) ScrollArea component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class Select(Component):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Select component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class Slider(Component):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Slider component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class Switch(Component):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Switch component.

    Parameters:
    - `disabled` (`bool, optional`) - a flag for disabling the switch component. Default is `False`
    - `read_only` (`bool, optional`) - a flag for making the switch read only. Default is `False`. Indicates that the element is not editable, but is otherwise operable. More information on [Read only](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Attributes/aria-readonly)
    """

    disabled: bool = False
    read_only: bool = False


class Tabs(Component):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Tabs component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class Textarea(Component):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Textarea component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class Toggle(Component):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Toggle component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class ToggleGroup(Component):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) ToggleGroup component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class InputOtp(Component):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) InputOtp component.

    Parameters:
    - `name` (`str`) - the name of the component
    """
