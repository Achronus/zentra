import re

from zentra.core import (
    LOWER_CAMELCASE_WITH_DIGITS,
    LOWERCASE_SINGLE_WORD,
    Component,
    has_valid_pattern,
)
from zentra.core.enums.ui import (
    ButtonSize,
    ButtonVariant,
    InputOTPPatterns,
    InputTypes,
    Orientation,
    TextStyle,
    ToggleSize,
    ToggleType,
    ToggleVariant,
)
from zentra.core.html import Div
from zentra.core.react import LucideIconWithText
from zentra.ui import ShadcnUi

from pydantic import Field, HttpUrl, PrivateAttr, ValidationInfo, field_validator
from pydantic_core import PydanticCustomError


class Button(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui Button](https://ui.shadcn.com/docs/components/button) component focusing on text.

    Parameters:
    - `content` (`string | zentra.core.react.LucideIconWithText`) - the information displayed inside the button. Can be a string of text or a `LucideIconWithText` Zentra model. Can include parameter variables (indicated by starting the variable name with a `$`)
    - `url` (`string, optional`) - the URL the button links to. `None` by default. When `None` removes it from `Button`
    - `variant` (`string, optional`) - the style of the button. Valid options: `['default', 'secondary', 'destructive', 'outline', 'ghost', 'link']`. `default` by default
    - `size` (`string, optional`) - the size of the button. Valid options: `['default', 'sm', 'lg', 'icon']`. `default` by default
    - `disabled` (`boolean, optional`) - adds the disabled property, preventing it from being clicked. `False` by default
    """

    content: str | LucideIconWithText
    url: HttpUrl = None
    variant: ButtonVariant = "default"
    size: ButtonSize = "default"
    disabled: bool = False


class Calendar(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui Calendar](https://ui.shadcn.com/docs/components/calendar) component.

    Parameters:
    - `name` (`string`) - an identifier for the component. Prepended to `get` and `set` for the `useState()` hook. Must be `lowercase` or `camelCase` and up to a maximum of `15` characters

    Example:
    1. `name='monthly'` ->
        `const [monthlyDate, monthlySetDate] = useState(new Date());"`
    2. `name='yearlyCalendar'` ->
        `const [yearlyCalendarDate, yearlyCalendarSetDate] = useState(new Date());"`
    """

    name: str = Field(min_length=1, max_length=15)

    @property
    def custom_common_attributes(self) -> list[str]:
        return ["name"]

    @field_validator("name")
    def validate_id(cls, name: str) -> str:
        if not has_valid_pattern(pattern=LOWER_CAMELCASE_WITH_DIGITS, value=name):
            raise PydanticCustomError(
                "string_pattern_mismatch",
                "must be lowercase or camelCase",
                dict(wrong_value=name, pattern=LOWER_CAMELCASE_WITH_DIGITS),
            )
        return name


class Checkbox(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui Checkbox](https://ui.shadcn.com/docs/components/checkbox) component.

    Parameters:
    - `id` (`string`) - an identifier for the component. Must be `lowercase` or `camelCase` and up to a maximum of `15` characters
    - `label` (`string`) - the text associated to the checkbox
    - `checked` (`boolean, optional`) - a flag that determines whether the checkbox is ticked or not. `False` by default
    - `more_info` (`string, optional`) - additional information to add under the checkbox. `None` by default. When `None` removes it from `Checkbox`
    - `disabled` (`boolean, optional`) - adds the disabled property, preventing it from being selected. `False` by default
    """

    id: str = Field(min_length=1, max_length=15)
    label: str = Field(min_length=1)
    checked: bool = False
    more_info: str = None
    disabled: bool = False

    @field_validator("id")
    def validate_id(cls, id: str) -> str:
        if not has_valid_pattern(pattern=LOWER_CAMELCASE_WITH_DIGITS, value=id):
            raise PydanticCustomError(
                "string_pattern_mismatch",
                "must be lowercase or camelCase",
                dict(wrong_value=id, pattern=LOWER_CAMELCASE_WITH_DIGITS),
            )
        return id


class MultiCheckbox(Component, ShadcnUi):
    """
    A Zentra model for multiple [Shadcn/ui Checkbox](https://ui.shadcn.com/docs/components/checkbox) components.

    Parameters:
    - `items` (`list[Checkbox]`) - a list of Checkbox components. Requires a `minimum` of `2` items
    """

    items: list[Checkbox] = Field(min_length=2)

    _container_name = PrivateAttr(default="Checkbox")

    # TODO: add logic specific to `Forms`


class Collapsible(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui Collapsible](https://ui.shadcn.com/docs/components/collapsible) component.

    Parameters:
    - `name` (`string`) - an identifier for the component. Prepended to `get` and `set` for the `useState()` hook. Must be `lowercase` or `camelCase` and up to a maximum of `15` characters
    - `title` (`string`) - the main heading of the collapsible
    - `items` (`list[str]`) - a list of strings representing the text to add into each collapsible block. Requires a `minimum` of `1` item
    """

    name: str = Field(min_length=1, max_length=15)
    title: str = Field(min_length=1)
    items: list[str] = Field(min_length=1)

    @property
    def custom_common_attributes(self) -> list[str]:
        return ["name"]

    @field_validator("name")
    def validate_id(cls, name: str) -> str:
        if not has_valid_pattern(pattern=LOWER_CAMELCASE_WITH_DIGITS, value=name):
            raise PydanticCustomError(
                "string_pattern_mismatch",
                "must be lowercase or camelCase",
                dict(wrong_value=name, pattern=LOWER_CAMELCASE_WITH_DIGITS),
            )
        return name


class Combobox(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui Combobox](https://ui.shadcn.com/docs/components/combobox) component.

    Parameters:
    - `name` (`string`) - the name of the component
    """

    # TODO: come back once 'popover' and 'command' created


class DatePicker(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui DatePicker](https://ui.shadcn.com/docs/components/date-picker) component.

    Parameters:
    - `name` (`string`) - the name of the component
    """

    # TODO: come back once 'popover' created


class Input(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui Input](https://ui.shadcn.com/docs/components/input) component.

    Inputs are extremely versatile as expressed in the [HTML Input docs](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/url). We've limited the attributes to the basics for simplicity. Once components are generated, you can edit them in the respective `.tsx` files with additional attributes if needed.

    Parameters:
    - `id` (`string`) - an identifier for the component. Must be `lowercase` or `camelCase` and up to a maximum of `15` characters
    - `type` (`string`) - the type of input field. Options `['text', 'email', 'password', 'number', 'file', 'tel', 'search', 'url', 'color']`
    - `placeholder` (`string`) - the placeholder text for the input
    - `disabled` (`boolean, optional`) - adds the disabled property, preventing it from being selected. `False` by default
    """

    id: str = Field(min_length=1, max_length=15)
    type: InputTypes
    placeholder: str
    disabled: bool = False

    @field_validator("id")
    def validate_id(cls, id: str) -> str:
        if not has_valid_pattern(pattern=LOWER_CAMELCASE_WITH_DIGITS, value=id):
            raise PydanticCustomError(
                "string_pattern_mismatch",
                "must be lowercase or camelCase",
                dict(wrong_value=id, pattern=LOWER_CAMELCASE_WITH_DIGITS),
            )
        return id


class InputOTP(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui InputOTP](https://ui.shadcn.com/docs/components/input-otp) component.

    Parameters:
    - `num_inputs` (`int`) - the length of the OTP. E.g., 6 = 6 input slots. Must be a minimum of `1`
    - `num_groups` (`int, optional`) - the number of slot groups. E.g., `InputOTP(num_inputs=6, num_groups=2)` -> 2 groups of 3 input slots. `1` by default
    - `pattern` (`string, optional`) - a regex pattern to limit the OTP input values. Options include: `['digits_only', 'chars_only', 'digits_n_chars_only']` ([official patterns](https://github.com/guilhermerodz/input-otp/blob/master/packages/input-otp/src/regexp.ts)) or a `custom` variant. `None` by default

    Examples:
    1. A basic OTP without a pattern.
    ```python
    input = InputOTP(num_inputs=6, num_groups=2)
    ```
    into ->
    ```jsx
    import { InputOTP, InputOTPGroup, InputOTPSlot, InputOTPSeparator } from '../ui/input-otp'

    <InputOTP maxLength={6}>
        <InputOTPGroup>
            <InputOTPSlot index={0} />
            <InputOTPSlot index={1} />
            <InputOTPSlot index={2} />
        </InputOTPGroup>
        <InputOTPSeparator />
        <InputOTPGroup>
            <InputOTPSlot index={3} />
            <InputOTPSlot index={4} />
            <InputOTPSlot index={5} />
        </InputOTPGroup>
    </InputOTP>
    ```

    2. A basic OTP with an official pattern and single group.
    ```python
    input = InputOTP(num_inputs=6, pattern='digits_only')
    ```
    into ->
    ```jsx
    import { InputOTP, InputOTPGroup, InputOTPSlot } from '../ui/input-otp'
    import { REGEXP_ONLY_DIGITS } from "input-otp"

    <InputOTP
        maxLength={6}
        pattern={REGEXP_ONLY_DIGITS}
    >
        <InputOTPGroup>
            <InputOTPSlot index={0} />
            <InputOTPSlot index={1} />
            <InputOTPSlot index={2} />
            <InputOTPSlot index={3} />
            <InputOTPSlot index={4} />
            <InputOTPSlot index={5} />
        </InputOTPGroup>
    </InputOTP>
    ```

    3. An OTP with a custom pattern and 3 groups.
    ```python
    input = InputOTP(num_inputs=6, num_groups=3, pattern=r"([\^$.|?*+()\[\]{}])")
    ```
    into ->
    ```jsx
    import { InputOTP, InputOTPGroup, InputOTPSlot, InputOTPSeparator } from '../ui/input-otp'

    <InputOTP
        maxLength={6}
        pattern="([\^$.|?*+()\[\]{}])"
    >
        <InputOTPGroup>
            <InputOTPSlot index={0} />
            <InputOTPSlot index={1} />
        </InputOTPGroup>
        <InputOTPSeparator />
        <InputOTPGroup>
            <InputOTPSlot index={2} />
            <InputOTPSlot index={3} />
        </InputOTPGroup>
        <InputOTPSeparator />
        <InputOTPGroup>
            <InputOTPSlot index={4} />
            <InputOTPSlot index={5} />
        </InputOTPGroup>
    </InputOTP>
    ```
    """

    num_inputs: int = Field(ge=1)
    num_groups: int = Field(default=1, ge=1)
    pattern: InputOTPPatterns | str = None

    @property
    def custom_common_attributes(self) -> list[str]:
        return ["pattern"]

    @field_validator("num_groups")
    def validate_num_groups(num_groups: int, info: ValidationInfo) -> int:
        num_inputs = info.data.get("num_inputs")
        if num_groups > num_inputs:
            raise PydanticCustomError(
                "size_out_of_bounds",
                f"cannot have more groups ({num_groups}) than input slots ({num_inputs})\n",
                dict(wrong_value=num_groups, input_size=num_inputs),
            )
        return num_groups

    @field_validator("pattern")
    def validate_pattern(pattern: str) -> str:
        if pattern not in InputOTPPatterns:
            try:
                re.compile(pattern)
            except re.error:
                official_patterns = [pattern.value for pattern in InputOTPPatterns]
                raise PydanticCustomError(
                    "invalid_regex_pattern",
                    f"must be an official pattern option ({official_patterns}) or a valid regex string\n",
                    dict(wrong_value=pattern, official_patterns=official_patterns),
                )
        return pattern


class Label(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui Label](https://ui.shadcn.com/docs/components/label) component.

    Parameters:
    - `name` (`string`) - an identifier for the component. Must be `lowercase` or `camelCase` and up to a maximum of `15` characters
    - `text` (`string`) - the descriptive text to put into the label. Can include parameter variables (indicated by starting the variable name with a `$`)
    """

    name: str = Field(min_length=1, max_length=15)
    text: str = Field(min_length=1)

    @field_validator("name")
    def validate_id(cls, name: str) -> str:
        if not has_valid_pattern(pattern=LOWER_CAMELCASE_WITH_DIGITS, value=name):
            raise PydanticCustomError(
                "string_pattern_mismatch",
                "must be lowercase or camelCase",
                dict(wrong_value=name, pattern=LOWER_CAMELCASE_WITH_DIGITS),
            )
        return name


class RadioButton(Component, ShadcnUi):
    """
    A helper Zentra model for the [Shadcn/ui RadioGroup](https://ui.shadcn.com/docs/components/radio-group) component. Cannot be used on its own, must be used inside a `RadioGroup` component.

    Parameters:
    - `id` (`string`) - an identifier for the component. Must be `lowercase` or `camelCase` and up to a maximum of `15` characters
    - `value` (`string`) - the value for the radio button. Up to a maximum of `30` characters. Must be `lowercase` and a `single word`
    - `text` (`string`) - the text to display for the radio button. Can include parameter variables (indicated by starting the variable name with a `$`)
    """

    id: str = Field(min_length=1, max_length=15)
    value: str = Field(min_length=1, max_length=30)
    text: str = Field(min_length=1)

    @field_validator("id")
    def validate_id(cls, id: str) -> str:
        if not has_valid_pattern(pattern=LOWER_CAMELCASE_WITH_DIGITS, value=id):
            raise PydanticCustomError(
                "string_pattern_mismatch",
                "must be lowercase or camelCase",
                dict(wrong_value=id, pattern=LOWER_CAMELCASE_WITH_DIGITS),
            )
        return id

    @field_validator("value")
    def validate_value(cls, value: str) -> str:
        if not has_valid_pattern(pattern=LOWERCASE_SINGLE_WORD, value=value):
            raise PydanticCustomError(
                "string_pattern_mismatch",
                "must be lowercase and a single word",
                dict(wrong_value=value, pattern=LOWERCASE_SINGLE_WORD),
            )
        return value


class RadioGroup(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui RadioGroup](https://ui.shadcn.com/docs/components/radio-group) component.

    Parameters:
    - `items` (`list[RadioButton]`) - a list of `zentra.control.RadioButton`
    - `default_value` (`string`) - the default value of the radio group. Must be a `value` assigned to a `RadioButton` in the `items` list. Must be `lowercase` and a `single word` and up to a maximum of `30` characters
    """

    items: list[RadioButton]
    default_value: str = Field(min_length=1, max_length=30)

    @field_validator("items")
    def validate_items(cls, items: list[RadioButton]) -> list[RadioButton]:
        if not items or len(items) == 0:
            raise PydanticCustomError(
                "missing_radio_button",
                "must have at least one 'RadioButton'",
                dict(wrong_value=items),
            )
        return items

    @field_validator("default_value")
    def validate_default_value(cls, default_value: str, info: ValidationInfo) -> str:
        if not has_valid_pattern(pattern=LOWERCASE_SINGLE_WORD, value=default_value):
            raise PydanticCustomError(
                "string_pattern_mismatch",
                "must be lowercase and a single word",
                dict(wrong_value=default_value, pattern=LOWERCASE_SINGLE_WORD),
            )

        present = False
        radio_buttons: list[RadioButton] = info.data.get("items")
        if radio_buttons:
            for rb in radio_buttons:
                if rb.value == default_value:
                    present = True
                    break

            if not present:
                raise PydanticCustomError(
                    "default_value_missing",
                    f"""'value="{default_value}"' missing from 'items'. Provided -> \n    '{radio_buttons}'\n""",
                    dict(wrong_value=default_value, items=radio_buttons),
                )

        return default_value


class ScrollArea(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui ScrollArea](https://ui.shadcn.com/docs/components/scroll-area) component.

    Parameters:
    - `content` (`string | zentra.core.html.Div`) - Can be either:
      1. A simple `string` of text
      2. A `zentra.core.html.Div` model (recommended)
    - `styles` (`string, optional`) - the CSS styles to apply to the `ScrollArea`. Automatically adds them to `className`. `w-96 rounded-md border` by default
    - `orientation` (`string, optional`) - the orientation of the scroll axis. Valid options: `[horizontal, vertical]`. `vertical` by default

    Example usage:
    1. A horizontal scroll area for images.
    ```python
    from zentra.core.html import Figure, FigCaption, Div, HTMLContent
    from zentra.core.js import Map
    from zentra.nextjs import Image
    from zentra.ui.control import ScrollArea

    artwork_map = Div(
        styles="flex w-max space-x-4 p-4",
        items=Map(
            obj_name="works",
            param_name="artwork",
            content=Figure(
                key="$artwork.artist",
                styles="shrink-0",
                img_container_styles="overflow-hidden rounded-md",
                img=Image(
                    src="$artwork.art",
                    alt="Photo by $artwork.artist",
                    styles="aspect-[3/4] h-fit w-fit object-cover",
                    width=300,
                    height=400
                ),
                caption=FigCaption(
                    styles="pt-2 text-xs text-muted-foreground",
                    text=[
                        'Photo by ',
                        HTMLContent(
                            tag="span",
                            styles="font-semibold text-foreground",
                            text="$artwork.artist"
                        )
                    ]
                ),
            ),
        )
    )

    ScrollArea(
        styles="w-96 whitespace-nowrap rounded-md border",
        content=artwork_map,
        orientation="horizontal",
    )
    ```
    JSX equivalent ->
    ```jsx
    <ScrollArea className="w-96 whitespace-nowrap rounded-md border">
      <div className="flex w-max space-x-4 p-4">
        {works.map((artwork) => (
          <figure key={artwork.artist} className="shrink-0">
            <div className="overflow-hidden rounded-md">
              <Image
                src={artwork.art}
                alt={`Photo by ${artwork.artist}`}
                className="aspect-[3/4] h-fit w-fit object-cover"
                width={300}
                height={400}
              />
            </div>
            <figcaption className="pt-2 text-xs text-muted-foreground">
              Photo by
              <span className="font-semibold text-foreground">
                {artwork.artist}
              </span>
            </figcaption>
          </figure>
        ))}
      </div>
      <ScrollBar orientation="horizontal" />
    </ScrollArea>
    ```

    2. A simple scroll area with text.
    ```python
    from zentra.ui.control import ScrollArea

    ScrollArea(
        content="This is some text that is extremely simple."
    )
    ```
    JSX equivalent ->
    ```jsx
    <ScrollArea className="w-96 rounded-md border">
        This is some text that is extremely simple.
        <ScrollBar orientation="vertical" />
    </ScrollArea>
    ```

    3. A vertical scroll area for a predefined set of tags.
    ```python
    from zentra.core.html import Div, HTMLContent
    from zentra.core.js import Map

    from zentra.ui.control import ScrollArea
    from zentra.ui.presentation import Separator

    tags_map = Map(
        obj_name="tags",
        param_name="tag",
        content=Div(
            shell=True,
            items=[
                Div(
                    key="$tag",
                    styles="text-sm",
                    items="$tag"
                ),
                Separator(styles="my-2"),
            ]
        )
    )

    ScrollArea(
        styles="h-72 w-48 rounded-md border",
        content=Div(
            styles="p-4",
            items=[
                HTMLContent(
                    tag="h4",
                    styles="mb-4 text-sm font-medium leading-none",
                    text="Tags"
                ),
                tags_map,
            ]
        ),
    )
    ```
    JSX equivalent ->
    ```jsx
    <ScrollArea className="h-72 w-48 rounded-md border">
        <div className="p-4">
            <h4 className="mb-4 text-sm font-medium leading-none">Tags</h4>
            {tags.map((tag) => (
                <>
                    <div key={tag} className="text-sm">
                        {tag}
                    </div>
                    <Separator className="my-2" orientation="vertical" />
                </>
            ))}
        </div>
        <ScrollBar orientation="vertical" />
    </ScrollArea>
    ```
    """

    content: str | Div
    styles: str = "w-96 rounded-md border"
    orientation: Orientation = "vertical"

    @property
    def inner_attributes(self) -> list[str]:
        return ["orientation"]


class SelectGroup(Component, ShadcnUi):
    """
    A helper Zentra model for the [Shadcn/ui Select](https://ui.shadcn.com/docs/components/select) component. Cannot be used on its own, must be used inside a `Select` component.

    Parameters:
    - `label` (`string, optional`) - a name for the group
    - `items` (`list[tuple[string, string]]`) - a list of tuple pairs of strings signifying the `(value, text)` for each `SelectItem`
    """

    label: str
    items: list[tuple[str, str]]


class Select(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui Select](https://ui.shadcn.com/docs/components/select) component.

    Parameters:
    - `display_text` (`string`) - the display text for the `Select` component. Stored in the `SelectValue` placeholder inside the `SelectTrigger`. This text is the first thing people will see
    - `groups` (`SelectGroup | list[zentra.model.control.SelectGroup]`) - a single or list of `zentra.model.control.SelectGroup` models containing the `SelectItem` values
    - `box_width` (`integer, optional`) - the size of the `Select` box width in pixels. `280` by default
    - `show_label` (`boolean, optional`) - a flag for displaying the label for the single `SelectGroup`. Only compatiable with a single `SelectGroup` (`groups=SelectGroup()`). `True` by default
    """

    display_text: str
    groups: SelectGroup | list[SelectGroup]
    box_width: int = 280
    show_label: bool = True


class Slider(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui Slider](https://ui.shadcn.com/docs/components/slider) component.

    Parameters:
    - `value` (`integer`) - the default value the slider starts at
    - `min` - (`integer | string, optional`) - the minimum value of the slider. When a string, acts as a parameter. `0` by default
    - `max` - (`integer | string, optional`) - the maximum value of the slider. When a string, acts as a parameter. `100` by default
    - `step` - (`integer | string, optional`) - the step size of the slider. When a string, acts as a parameter. `1` by default
    - `bar_size` - (`integer, optional`) - the size of the `Slider` as a percentage. Can be any value between `0 - 100`. `60` by default
    - `name` (`string, optional`) - the name of the `Slider`.  Must be `lowercase` or `camelCase` and up to a maximum of `15` characters. `None` by default
    - `disabled` (`boolean, optional`) - adds the disabled property, preventing it from being selected. `False` by default
    - `orientation` (`string, optional`) -  the orientation of the `Slider`. Valid options: `[horizontal, vertical]`. `horizontal` by default
    """

    value: int
    min: int | str = 0
    max: int | str = 100
    step: int | str = 1
    bar_size: int = 60
    name: str = None
    disabled: bool = False
    orientation: Orientation = "horizontal"

    @property
    def custom_common_attributes(self) -> list[str]:
        return ["value"]

    @field_validator("name")
    def validate_name(cls, name: str) -> str:
        if not has_valid_pattern(pattern=LOWER_CAMELCASE_WITH_DIGITS, value=name):
            raise PydanticCustomError(
                "string_pattern_mismatch",
                "must be lowercase or camelCase",
                dict(wrong_value=name, pattern=LOWER_CAMELCASE_WITH_DIGITS),
            )
        return name

    @field_validator("bar_size")
    def validate_bar_size(cls, size: int) -> int:
        if not (0 <= size <= 100):
            raise PydanticCustomError(
                "out_of_range",
                "must be between '0' and '100'",
                dict(wrong_value=size, accepted_min=0, accepted_max=100),
            )
        return size


class Switch(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui Switch](https://ui.shadcn.com/docs/components/switch) component.

    Parameters:
    - `id` (`string`) - an identifier for the component. Must be `lowercase` or `camelCase` and up to a maximum of `15` characters
    - `checked` (`boolean, optional`) - a flag that determines whether the switch is selected or not. `False` by default
    - `disabled` (`boolean, optional`) - a flag for disabling the switch component. Default is `False`
    """

    id: str = Field(min_length=1, max_length=15)
    checked: bool = False
    disabled: bool = False

    @field_validator("id")
    def validate_id(cls, id: str) -> str:
        if not has_valid_pattern(pattern=LOWER_CAMELCASE_WITH_DIGITS, value=id):
            raise PydanticCustomError(
                "string_pattern_mismatch",
                "must be lowercase or camelCase",
                dict(wrong_value=id, pattern=LOWER_CAMELCASE_WITH_DIGITS),
            )
        return id


class Tabs(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui Tabs](https://ui.shadcn.com/docs/components/tabs) component.

    Parameters:
    - `name` (`string`) - the name of the component
    """

    # TODO: complete after simple


class Textarea(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui Textarea](https://ui.shadcn.com/docs/components/textarea) component.

    Parameters:
    - `id` (`string`) - an identifier for the component. Must be `lowercase` or `camelCase` and up to a maximum of `15` characters
    - `placeholder` (`string`) - the placeholder text to put into the textarea
    """

    id: str = Field(min_length=1, max_length=15)
    placeholder: str = Field(min_length=1)

    @field_validator("id")
    def validate_id(cls, id: str) -> str:
        if not has_valid_pattern(pattern=LOWER_CAMELCASE_WITH_DIGITS, value=id):
            raise PydanticCustomError(
                "string_pattern_mismatch",
                "must be lowercase or camelCase",
                dict(wrong_value=id, pattern=LOWER_CAMELCASE_WITH_DIGITS),
            )
        return id


class Toggle(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui Toggle](https://ui.shadcn.com/docs/components/toggle) component.

    Parameters:
    - `content` (`string | zentra.core.react.LucideIconWithText`) - the information displayed inside the toggle. Can be a string of text or a `LucideIconWithText` Zentra model. Can include parameter variables (indicated by starting the variable name with a `$`)
    - `style` (`string, optional`) - the style of the toggle text (`aria-label`). Valid options: `['default', 'bold', 'outline', 'italic', 'underline']`. `default` by default
    - `size` (`string, optional`) - the size of the toggle. Valid options: `['default', 'sm', 'lg']`. `default` by default
    - `variant` (`string, optional`) - the style of the toggle. Valid options: `['default', 'outline']`. `default` by default
    - `pressed` (`boolean, optional`) - a flag for activating the toggle state. `False` by default
    - `disabled` (`boolean, optional`) - adds the disabled property, preventing it from being selected. `False` by default
    """

    content: str | LucideIconWithText
    style: TextStyle = "default"
    size: ToggleSize = "default"
    variant: ToggleVariant = "default"
    pressed: bool = False
    disabled: bool = False


class ToggleGroup(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui ToggleGroup](https://ui.shadcn.com/docs/components/toggle-group) ToggleGroup component.

    Parameters:
    - `items` (`list[zentra.ui.control.Toggle]`) - a list of `Toggle` models to display in the group
    - `type` (`string, optional`) - the type of toggle state for the models. Valid options: `['single', 'multiple']`. When `single`, only one `Toggle` can be pressed at a time. When `multiple`, all `Toggles` can be activated simultaneously. `multiple` by default
    - `disabled` (`boolean, optional`) - adds the disabled property, preventing the group from being selected. `False` by default
    - `size` (`string, optional`) - the size of the `Toggle` items in the group. Valid options: `['default', 'sm', 'lg']`. `default` by default
    - `variant` (`string, optional`) - the style of the `Toggle` items. Valid options: `['default', 'outline']`. `default` by default
    - `orientation` (`string, optional`) - the orientation of the `ToggleGroup`. Valid options: `[horizontal, vertical]`. `horizontal` by default
    """

    items: list[Toggle]
    type: ToggleType = "multiple"
    disabled: bool = False
    size: ToggleSize = "default"
    variant: ToggleVariant = "default"
    orientation: Orientation = "horizontal"
