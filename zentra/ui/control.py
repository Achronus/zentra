from typing import Optional

from zentra.core import Component, DataArray
from zentra.core.constants import LOWER_CAMELCASE_WITH_DIGITS, LOWERCASE_SINGLE_WORD
from zentra.core.enums.ui import (
    ButtonSize,
    ButtonVariant,
    CalendarMode,
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

from pydantic import Field, PrivateAttr, ValidationInfo, field_validator

from zentra.core.validation import check_pattern_match, url_validation
from zentra.core.validation.component import (
    calendar_validation,
    input_otp_num_groups_validation,
    input_otp_pattern_validation,
    pagination_validation,
    radio_group_default_value_validation,
    radio_group_items_validation,
    slider_validation,
)


class Button(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui Button](https://ui.shadcn.com/docs/components/button) component focusing on text.

    Parameters:
    - `content` (`string | zentra.core.react.LucideIconWithText`) - the information displayed inside the button. Can be a string of text or a `LucideIconWithText` Zentra model. Can include parameter variables (indicated by starting the variable name with a `$.`)
    - `url` (`string, optional`) - the URL the button links to. `None` by default. When `None` removes it from `Button`. Can be a path or URL starting with any of the following:
      1. Local paths - `/`, `./`, or `../`
      2. File urls - `ftp://` or `file://`
      3. Informative urls - `mailto:` or `tel:`
      4. HTTP urls - `http://` or `https://`
    - `variant` (`string, optional`) - the style of the button. Valid options: `['default', 'secondary', 'destructive', 'outline', 'ghost', 'link']`. `default` by default
    - `size` (`string, optional`) - the size of the button. Valid options: `['default', 'sm', 'lg', 'icon']`. `default` by default
    - `disabled` (`boolean, optional`) - adds the disabled property, preventing it from being clicked. `False` by default
    - `styles` (`string, optional`) - a set of custom CSS classes to apply to the button. Automatically adds them to its `className`. `None` by default
    - `other` (`dict[string, string], optional`) - a dictionary of additional attributes that can be passed into a button. Accepted in the form of: `prop_name: prop_value`. `prop_value` can be a parameter (indicated by starting the variable name with a `$.`).  `None` by default
    """

    content: str | LucideIconWithText
    url: Optional[str] = None
    variant: ButtonVariant = "default"
    size: ButtonSize = "default"
    disabled: bool = False
    styles: Optional[str] = None
    other: Optional[dict[str, str]] = None

    @field_validator("url")
    def validate_url(cls, url: str) -> str:
        return url_validation(url)


class Calendar(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui Calendar](https://ui.shadcn.com/docs/components/calendar) component.

    Parameters:
    - `name` (`string`) - an identifier for the component. Prepended to `get` and `set` for the `useState()` hook. Must be `lowercase` or `camelCase` and up to a maximum of `30` characters
    - `mode` (`string, optional`) - the selection mode for the calendar. Valid options: `['single', 'multiple', 'range']`. `single` by default
    - `styles` (`string, optional`) - a set of custom CSS classes to apply to the calendar. Automatically adds them to `className`. `rounded-md border` by default
    - `required` (`boolean, optional`) - a flag for making the date selection mandatory. Only accessible when `mode='single'`. `False` by default
    - `disable_nav` (`boolean, optional`) - a flag for disabling the navigation between months. `False` by default
    - `min` (`integer, optional`) - the minimum selectable number of dates. Only accessible when `mode='multiple'` or `mode='range'`. `None` by default
    - `max` (`integer, optional`) - the maximum selectable number of dates. Only accessible when `mode='multiple'` or `mode='range'`. `None` by default.
    - `num_months` (`integer, optional`) - the number of displayed months. Can be as low as `2` or as high as `12`. `None` by default. When `None` shows a single month
    - `default_month` (`tuple[integer, integer], optional`) - a tuple containing the `(year, month)` to set as the initial month to show in the calendar. `None` by default. When `None` sets the `current month` automatically
    - `from_year` (`integer, optional`) - the earliest year to start the navigation. `None` by default. When `None` there is no limit
    - `to_year` (`integer, optional`) - the latest year to end the navigation. `None` by default. When `None` there is no limit
    - `from_month` (`tuple[integer, integer], optional`) - the earliest month to start the navigation in the form of `(year, month)`. `None` by default. When `None` there is no limit
    - `to_month` (`tuple[integer, integer], optional`) - the latest month to end the navigation in the form of `(year, month)`. `None` by default. When `None` there is no limit
    - `from_date` (`tuple[integer, integer, integer], optional`) - the earliest day to start the navigation in the form of `(year, month, date)`. `None` by default. When `None` there is no limit
    - `to_date` (`tuple[integer, integer, integer], optional`) - the latest day to end the navigation in the form of `(year, month, date)`. `None` by default. When `None` there is no limit
    """

    name: str = Field(min_length=1, max_length=30)
    mode: CalendarMode = "single"
    styles: Optional[str] = "rounded-md border"
    required: bool = False
    disable_nav: bool = False
    min: Optional[int] = None
    max: Optional[int] = None
    num_months: Optional[int] = Field(default=None, ge=2, le=12)
    default_month: Optional[tuple[int, int]] = None
    from_year: Optional[int] = None
    to_year: Optional[int] = None
    from_month: Optional[tuple[int, int]] = None
    to_month: Optional[tuple[int, int]] = None
    from_date: Optional[tuple[int, int, int]] = None
    to_date: Optional[tuple[int, int, int]] = None

    @property
    def custom_common_attributes(self) -> list[str]:
        return ["name"]

    @property
    def use_state_names(self) -> tuple[str, str]:
        """Defines the `useState` hook `get` and `set` names."""
        get_name, set_name = [f"{self.name}Date", f"{self.name}SetDate"]

        if self.mode == CalendarMode.SINGLE.value:
            return [get_name, set_name]
        elif self.mode == CalendarMode.MULTIPLE.value:
            return [f"{self.name}SelectedDates", f"{self.name}SetSelectedDates"]
        else:
            return [f"{get_name}Range", f"{set_name}Range"]

    @field_validator("name")
    def validate_id(cls, name: str) -> str:
        return check_pattern_match(
            LOWER_CAMELCASE_WITH_DIGITS, name, err_msg="must be lowercase or camelCase"
        )

    @field_validator("required")
    def validate_required(cls, req: bool, info: ValidationInfo) -> bool:
        mode = info.data.get("mode")

        return calendar_validation(
            req,
            mode,
            condition=(mode != CalendarMode.SINGLE.value),
            err_msg_word="unless",
        )

    @field_validator("min", "max")
    def validate_min_max(cls, val: int, info: ValidationInfo) -> int:
        mode = info.data.get("mode")

        return calendar_validation(
            val,
            mode,
            condition=(mode == CalendarMode.SINGLE.value),
            err_msg_word="when",
        )


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
    more_info: Optional[str] = None
    disabled: bool = False

    @field_validator("id")
    def validate_id(cls, id: str) -> str:
        return check_pattern_match(
            LOWER_CAMELCASE_WITH_DIGITS, id, err_msg="must be lowercase or camelCase"
        )


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

    @property
    def child_names(self) -> list[str]:
        return ["CollapsibleTrigger", "CollapsibleContent"]

    @field_validator("name")
    def validate_id(cls, name: str) -> str:
        return check_pattern_match(
            LOWER_CAMELCASE_WITH_DIGITS,
            name,
            err_msg="must be lowercase or camelCase",
        )


class Combobox(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui Combobox](https://ui.shadcn.com/docs/components/combobox) component.

    Parameters:
    - `data` (`zentra.core.DataArray`) -
    - `display_text` (`string`) -
    - `search_text` (`string`) -
    - `hook_name` (`string, optional`) - the prepended name added to all `use` hook values. For example, `hook_name='combobox'` = `[comboboxOpen, comboboxSetOpen]`. `comboBox` by default
    """

    data: DataArray
    display_text: str
    search_text: str
    hook_name: str = "combobox"

    @field_validator("hook_name")
    def validate_hook_name(cls, name: str) -> str:
        return name.lower()

    @property
    def open_state_names(self) -> tuple[str, str]:
        """Defines the open `useState` hook `get` and `set` names."""
        return [f"{self.hook_name}Open", f"{self.hook_name}SetOpen"]

    @property
    def value_state_names(self) -> tuple[str, str]:
        """Defines the value `useState` hook `get` and `set` names."""
        return [f"{self.hook_name}Value", f"{self.hook_name}SetValue"]

    @property
    def composition_only(self) -> bool:
        return True


class DatePicker(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui DatePicker](https://ui.shadcn.com/docs/components/date-picker) component.

    Built using a composition of the `zentra.ui.modal.Popover` and `zentra.ui.control.Calendar` models.

    Parameters:
    - `trigger` (`string`) - the text to display in the trigger button
    - `content` (`zentra.ui.control.Calendar`) - a zentra `Calendar` model
    - `styles` (`string, optional`) - a set of custom CSS classes to apply to the `PopoverContent`. Automatically adds them to its `className`. `None` by default
    """

    trigger: str
    content: Calendar
    styles: Optional[str] = None

    @property
    def custom_common_attributes(self) -> list[str]:
        return ["styles"]

    @property
    def trigger_styles(self) -> str:
        """Defines the default trigger styles."""
        return f'cn("w-[300px] justify-start text-left font-normal", !{self.content.use_state_names[0]} && "text-muted-foreground")'

    @property
    def trigger_text(self) -> list[str]:
        """Defines the trigger text for the date picker."""
        get_name = self.content.use_state_names[0]

        if self.calendar_mode == CalendarMode.RANGE.value:
            return [
                "{",
                f"{get_name}?.from ? ({get_name}.to ? (",
                "<>{format(",
                f'{get_name}.from, "LLL dd, y")',
                '} -{" "}{format(',
                f'{get_name}.to, "LLL dd, y")' "}</>) : (format(",
                f'{get_name}.from, "LLL dd, y"))) : (',
                f"<span>{self.trigger}</span>",
                ")}",
            ]

        return [
            f'{{{get_name} ? format({get_name}, "PPP") : <span>{self.trigger}</span>}}'
        ]

    @property
    def calendar_mode(self) -> str:
        """Defines the mode of the calendar. Required for component wrapper when `mode='range'`."""
        return self.content.mode

    @property
    def composition_only(self) -> bool:
        return True


class Input(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui Input](https://ui.shadcn.com/docs/components/input) component.

    Inputs are extremely versatile as expressed in the [HTML Input docs](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/url). We've limited the attributes to the basics for simplicity. Once components are generated, you can edit them in the respective `.tsx` files with additional attributes if needed.

    Parameters:
    - `id` (`string`) - an identifier for the component. Must be `lowercase` or `camelCase` and up to a maximum of `15` characters
    - `type` (`string, optional`) - the type of input field. Options `['text', 'email', 'password', 'number', 'file', 'tel', 'search', 'url', 'color']`. `text` by default
    - `placeholder` (`string, optional`) - the placeholder text for the input. `None` by default
    - `disabled` (`boolean, optional`) - adds the disabled property, preventing it from being selected. `False` by default
    - `styles` (`string, optional`) - a set of custom CSS classes to apply to the input. Automatically adds them to `className`. `None` by default
    - `default_value` (`string, optional`) - an optional string defining the initial value of the text input. `None` by default
    """

    id: str = Field(min_length=1, max_length=15)
    type: InputTypes = "text"
    placeholder: Optional[str] = None
    disabled: bool = False
    styles: Optional[str] = None
    default_value: Optional[str] = None

    @field_validator("id")
    def validate_id(cls, id: str) -> str:
        return check_pattern_match(
            LOWER_CAMELCASE_WITH_DIGITS,
            id,
            err_msg="must be lowercase or camelCase",
        )


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
    pattern: Optional[InputOTPPatterns | str] = None

    @property
    def custom_common_attributes(self) -> list[str]:
        return ["pattern"]

    @property
    def child_names(self) -> list[str]:
        return ["InputOTPGroup", "InputOTPSlot", "InputOTPSeparator"]

    @field_validator("num_groups")
    def validate_num_groups(num_groups: int, info: ValidationInfo) -> int:
        num_inputs = info.data.get("num_inputs")
        return input_otp_num_groups_validation(num_groups, num_inputs)

    @field_validator("pattern")
    def validate_pattern(pattern: str) -> str:
        return input_otp_pattern_validation(pattern)


class Label(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui Label](https://ui.shadcn.com/docs/components/label) component.

    Parameters:
    - `name` (`string`) - an identifier for the component. Must be `lowercase` or `camelCase` and up to a maximum of `15` characters
    - `text` (`string`) - the descriptive text to put into the label. Can include parameter variables (indicated by starting the variable name with a `$.`)
    """

    name: str = Field(min_length=1, max_length=15)
    text: str = Field(min_length=1)

    @field_validator("name")
    def validate_id(cls, name: str) -> str:
        return check_pattern_match(
            LOWER_CAMELCASE_WITH_DIGITS, name, err_msg="must be lowercase or camelCase"
        )


class Pagination(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui Pagination](https://ui.shadcn.com/docs/components/pagination) component.

    Parameters:
    - `items_per_page` (`integer`) - the number of items per page. Used as an `itemsPerPage` variable in the component that is passed into the state hooks for the `next` and `previous` items
    - `links` (`list[string]`) - a list of links to add to the pagination. Up to a maximum of 5
    - `total_items` (`integer, optional`) - the maximum number of items used in the pagination. Used as a `maxItems` variable in the component. Applied to `PaginationNext` for disabling interaction when on the last page. `100` by default
    - `name` (`string, optional`) - a custom name for the pagination. Used to identify the state hooks for this component. `pag` by default
    - `ellipsis` (`boolean`) - a flag for including an ellipsis before `PaginationNext` and after `PaginationItems` to indicate more pages. `False` by default
    """

    items_per_page: int
    links: list[str]
    total_items: int = 100
    name: str = "pag"
    ellipsis: bool = False

    @property
    def custom_common_attributes(self) -> list[str]:
        return ["name"]

    @property
    def child_names(self) -> list[str]:
        return [
            "PaginationContent",
            "PaginationEllipsis",
            "PaginationItem",
            "PaginationLink",
            "PaginationNext",
            "PaginationPrevious",
        ]

    @property
    def start_idx_name(self) -> tuple[str, str]:
        """Defines the start index state hook `get` and `set` names."""
        return [f"{self.name}StartIndex", f"{self.name}SetStartIndex"]

    @property
    def end_idx_name(self) -> tuple[str, str]:
        """Defines the end index state hook `get` and `set` names."""
        return [f"{self.name}EndIndex", f"{self.name}SetEndIndex"]

    @field_validator("links")
    def validate_links(cls, links: list[str]) -> list[str]:
        return pagination_validation(links, 5)


class RadioButton(Component, ShadcnUi):
    """
    A helper Zentra model for the [Shadcn/ui RadioGroup](https://ui.shadcn.com/docs/components/radio-group) component. Cannot be used on its own, must be used inside a `RadioGroup` component.

    Parameters:
    - `id` (`string`) - an identifier for the component. Must be `lowercase` or `camelCase` and up to a maximum of `15` characters
    - `value` (`string`) - the value for the radio button. Up to a maximum of `30` characters. Must be `lowercase` and a `single word`
    - `text` (`string`) - the text to display for the radio button. Can include parameter variables (indicated by starting the variable name with a `$.`)
    """

    id: str = Field(min_length=1, max_length=15)
    value: str = Field(min_length=1, max_length=30)
    text: str = Field(min_length=1)

    @field_validator("id")
    def validate_id(cls, id: str) -> str:
        return check_pattern_match(
            LOWER_CAMELCASE_WITH_DIGITS,
            id,
            err_msg="must be lowercase or camelCase",
        )

    @field_validator("value")
    def validate_value(cls, value: str) -> str:
        return check_pattern_match(
            LOWERCASE_SINGLE_WORD,
            value,
            err_msg="must be lowercase and a single word",
        )


class RadioGroup(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui RadioGroup](https://ui.shadcn.com/docs/components/radio-group) component.

    Parameters:
    - `items` (`list[RadioButton]`) - a list of `zentra.control.RadioButton`
    - `default_value` (`string`) - the default value of the radio group. Must be a `value` assigned to a `RadioButton` in the `items` list. Must be `lowercase` and a `single word` and up to a maximum of `30` characters
    """

    items: list[RadioButton]
    default_value: str = Field(min_length=1, max_length=30)

    @property
    def child_names(self) -> list[str]:
        return ["RadioGroupItem"]

    @field_validator("items")
    def validate_items(cls, items: list[RadioButton]) -> list[RadioButton]:
        return radio_group_items_validation(items)

    @field_validator("default_value")
    def validate_default_value(cls, default_value: str, info: ValidationInfo) -> str:
        default_value = check_pattern_match(
            LOWERCASE_SINGLE_WORD,
            default_value,
            err_msg="must be lowercase and a single word",
        )

        radio_buttons: list[RadioButton] = info.data.get("items")
        return radio_group_default_value_validation(default_value, radio_buttons)


class ScrollArea(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui ScrollArea](https://ui.shadcn.com/docs/components/scroll-area) component.

    Parameters:
    - `content` (`string | zentra.core.html.Div`) - Can be either:
      1. A simple `string` of text
      2. A `zentra.core.html.Div` model (recommended)
    - `styles` (`string, optional`) - a set of custom CSS classes to apply to the `ScrollArea`. Automatically adds them to `className`. `w-96 rounded-md border` by default
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
                key="$.artwork.artist",
                styles="shrink-0",
                img_container_styles="overflow-hidden rounded-md",
                img=Image(
                    src="$.artwork.art",
                    alt="Photo by $.artwork.artist",
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
                            text="$.artwork.artist"
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
                    key="$.tag",
                    styles="text-sm",
                    items="$.tag"
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

    @property
    def child_names(self) -> list[str]:
        return ["ScrollBar"]


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

    @property
    def child_names(self) -> list[str]:
        return [
            "SelectContent",
            "SelectGroup",
            "SelectItem",
            "SelectLabel",
            "SelectTrigger",
            "SelectValue",
        ]


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
    name: Optional[str] = None
    disabled: bool = False
    orientation: Orientation = "horizontal"

    @property
    def custom_common_attributes(self) -> list[str]:
        return ["value"]

    @field_validator("name")
    def validate_name(cls, name: str) -> str:
        return check_pattern_match(
            LOWER_CAMELCASE_WITH_DIGITS,
            name,
            err_msg="must be lowercase or camelCase",
        )

    @field_validator("bar_size")
    def validate_bar_size(cls, size: int) -> int:
        return slider_validation(size, 0, 100)


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
        return check_pattern_match(
            LOWER_CAMELCASE_WITH_DIGITS,
            id,
            err_msg="must be lowercase or camelCase",
        )


class Tabs(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui Tabs](https://ui.shadcn.com/docs/components/tabs) component.

    Parameters:
    - `name` (`string`) - the name of the component
    """

    # TODO: come back once 'card' created


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
        return check_pattern_match(
            LOWER_CAMELCASE_WITH_DIGITS,
            id,
            err_msg="must be lowercase or camelCase",
        )


class Toggle(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui Toggle](https://ui.shadcn.com/docs/components/toggle) component.

    Parameters:
    - `content` (`string | zentra.core.react.LucideIconWithText`) - the information displayed inside the toggle. Can be a string of text or a `LucideIconWithText` Zentra model. Can include parameter variables (indicated by starting the variable name with a `$.`)
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

    @property
    def child_names(self) -> list[str]:
        return ["ToggleGroupItem"]
