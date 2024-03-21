from zentra.core import Component, Icon
from zentra.core.enums.ui import ButtonVariant, ButtonIconPosition, InputTypes


class Button(Component):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Button component.

    Parameters:
    - `name` (`str`) - the name of the component
    - `text` (`str, optional`) - the text displayed inside the button. `None` by default. When `None` removes it from `Button`
    - `url` (`str, optional`) - the URL the button links to. `None` by default. When `None` removes it from `Button`
    - `variant` (`str, optional`) - the style of the button. Valid options: `['none', 'primary', 'secondary', 'destructive', 'outline', 'ghost', 'link']`. `none` by default.
    - `icon` (`Icon, optional`) - the [Radix UI Icon](https://www.radix-ui.com/icons) to add inside the button. `None` by default. When `None` removes it from `Button`
    - `icon_position` (`str, optional`) - the position of the icon inside the button. When set to `start`, icon appears before the text. When `end`, it appears after the text. `start` by default. Valid options: `['start', 'end']`
    - `icon_only` (`bool, optional`) - converts the button to an icon only button. Ignores text parameter. `False` by default
    - `disabled` (`bool, optional`) - adds the disabled property, preventing it from being clicked. `False` by default
    """

    text: str = None
    url: str = None
    variant: ButtonVariant = "none"
    icon: Icon = None
    icon_position: ButtonIconPosition = "start"
    icon_only: bool = False
    disabled: bool = False


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
    - `name` (`str`) - the name of the component
    """


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
