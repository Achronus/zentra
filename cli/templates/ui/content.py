from cli.templates.builders import add_to_storage
from cli.templates.builders.controller import BuildController
from cli.templates.storage import JSXComponentExtras
from cli.templates.ui.attributes import alt_attribute, src_attribute
from cli.templates.utils import compress, text_content

from zentra.core import Component
from zentra.core.base import HTMLTag
from zentra.core.react import LucideIcon, LucideIconWithText
from zentra.nextjs import Link, NextJs
from zentra.ui.control import (
    Button,
    Checkbox,
    Collapsible,
    InputOTP,
    Pagination,
    RadioButton,
    RadioGroup,
    ScrollArea,
    Select,
    SelectGroup,
    Toggle,
    ToggleGroup,
)
from zentra.ui.navigation import (
    DDMCheckboxGroup,
    DDMGroup,
    DDMItem,
    DDMSeparator,
    DDMSubGroup,
    DropdownMenu,
    DDMRadioGroup,
)
from zentra.ui.notification import Alert, TextAlertDialog, Tooltip
from zentra.ui.presentation import Avatar


def controller() -> BuildController:
    """A helper function to create a `BuildController`."""
    from cli.templates.ui.mappings import CONTROLLER_MAPPINGS
    from cli.templates.details import COMPONENT_DETAILS_DICT

    return BuildController(
        mappings=CONTROLLER_MAPPINGS, details_dict=COMPONENT_DETAILS_DICT
    )


def build_icon(
    model: LucideIcon | LucideIconWithText, output_storage: bool = False
) -> list[str] | tuple[list[str], JSXComponentExtras]:
    """A helper function to create a `LucideIcon` model. Returns the content as a list of strings. Or, if `output_storage` is `True`, returns a tuple in the form: `(content, JSXComponentExtras)`."""
    content, import_str = controller().build_icon(model)

    if output_storage:
        storage = JSXComponentExtras()
        storage.imports.append(import_str)
        return content, storage

    return content


def build_component(
    component: Component, output_storage: bool = False, full_shell: bool = False
) -> list[str] | tuple[list[str], JSXComponentExtras]:
    """A helper function to create a `Component` model (including `NextJS` components). Returns the content as a list of strings. Or, if `output_storage` is `True`, returns a tuple in the form: `(content, JSXComponentExtras)`."""
    if isinstance(component, NextJs):
        content, comp_storage = controller().build_nextjs_component(component)
    else:
        content, comp_storage = controller().build_component(
            component, full_shell=full_shell
        )

    if output_storage:
        storage = JSXComponentExtras()
        storage = add_to_storage(storage, comp_storage)
        return content, storage

    return content


def build_html_tag(
    tag: HTMLTag, output_storage: bool = False
) -> list[str] | tuple[list[str], JSXComponentExtras]:
    """A helper function to create a `HTMLTag` models. Returns the content as a list of strings. Or, if `output_storage` is `True`, returns a tuple in the form: `(content, JSXComponentExtras)`."""
    content, comp_storage = controller().build_html_tag(tag)

    if output_storage:
        return content, comp_storage

    return content


def add_wrapper(name: str, content: str | list[str], attrs: str = None) -> str:
    """A helper function to create a JSX wrapper around a given set of content. Applies the `name` and `attrs` to the start wrapper. Returns the updated content as a `string`."""
    start = f"<{name}{f' {attrs}' if attrs else ''}>"
    end = f"</{name}>"

    if isinstance(content, str):
        return compress([start, content, end])

    return compress([start, *content, end])


def string_icon_content(content: str | LucideIconWithText) -> list[str]:
    """A helper function to handle the `content` attribute when it is a string or `LucideIconWithText`. Returns the content as a list of strings."""
    if isinstance(content, str):
        text = text_content(content)
    else:
        from cli.templates.builders.icon import IconBuilder
        from cli.templates.ui.mappings import ATTRIBUTE_MAPPINGS

        text, _ = IconBuilder(model=content, mappings=ATTRIBUTE_MAPPINGS).build()

    return text


def checkbox_content(cb: Checkbox) -> list[str]:
    """Returns a list of strings for the `Checkbox` content based on the components attributes."""
    content = [
        '<div className="grid gap-1.5 leading-none">',
        f'<label htmlFor="{cb.id}" className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">',
        f"{cb.label}",
        "</label>",
    ]

    if cb.more_info:
        content.extend(
            ['<p className="text-sm text-muted-foreground">', cb.more_info, "</p>"]
        )

    content.append("</div>")
    return content


def collapsible_content(comp: Collapsible) -> list[str]:
    """Returns a list of strings for the `Collapsible` content based on the components attributes."""
    content = [
        '<div className="flex items-center justify-between space-x-4 px-4">',
        '<h4 className="text-sm font-semibold">',
        comp.title,
        "</h4>",
        "<CollapsibleTrigger asChild>",
        '<Button variant="ghost" size="sm" className="w-9 p-0">',
        '<ChevronsUpDown className="h-4 w-4" />',
        '<span className="sr-only">',
        "Toggle",
        "</span>",
        "</Button>",
        "</CollapsibleTrigger>",
        "</div>",
        '<div className="rounded-md border px-4 py-3 font-mono text-sm">',
        comp.items[0],
        "</div>",
        '<CollapsibleContent className="space-y-2">',
    ]

    if len(comp.items) > 1:
        for item in comp.items[1:]:
            content.extend(
                [
                    '<div className="rounded-md border px-4 py-3 font-mono text-sm">',
                    item,
                    "</div>",
                ]
            )

    content.append("</CollapsibleContent>")
    return content


def radio_button_content(rb: RadioButton) -> list[str]:
    """Returns a list of strings for the `RadioButton` content based on the components attributes."""
    return [
        '<div className="flex items-center space-x-2">',
        f'<RadioGroupItem value="{rb.value}" id="{rb.id}" />',
        f'<Label htmlFor="{rb.id}">',
        rb.text,
        "</Label>",
        "</div>",
    ]


def radio_group_content(rg: RadioGroup) -> list[str]:
    """Returns a list of strings for the `RadioGroup` content based on the components attributes."""
    content = []
    for rb in rg.items:
        content.extend(radio_button_content(rb))

    return content


def select_content(select: Select) -> list[str]:
    """Returns a list of strings for the `Select` content based on the components attributes."""
    content = [
        f'<SelectTrigger className="w-[{select.box_width}px]">',
        f'<SelectValue placeholder="{select.display_text}" />',
        "</SelectTrigger>",
    ]

    if isinstance(select.groups, SelectGroup):
        select.groups = [select.groups]

    group_content = []
    for group in select.groups:
        group_content.extend(
            ["<SelectGroup>", f"<SelectLabel>{group.label}</SelectLabel>"]
        )
        for item in group.items:
            group_content.append(
                f'<SelectItem value="{item[0]}">{item[1]}</SelectItem>'
            )
        group_content.append("</SelectGroup>")

    if len(select.groups) == 1 and not select.show_label:
        group_content.pop()
        group_content.pop(0)
        group_content.pop(0)

    content.extend(group_content)
    return content


def alert_content(alert: Alert) -> list[str]:
    """Returns a list of strings for the `Alert` content based on the components attributes."""
    content = [
        "<AlertTitle>",
        alert.title,
        "</AlertTitle>",
        "<AlertDescription>",
        alert.description,
        "</AlertDescription>",
    ]

    if alert.icon:
        content.insert(0, LucideIcon(name=alert.icon, styles="h-4 w-4").content_str)

    return content


def text_alert_dialog_content(ad: TextAlertDialog) -> list[str]:
    """Returns a list of strings for the `TextAlertDialog` content based on the components attributes."""
    return [
        "<AlertDialogTrigger asChild>",
        '<Button variant="outline">',
        ad.trigger_text,
        "</Button>",
        "</AlertDialogTrigger>",
        "<AlertDialogContent>",
        "<AlertDialogHeader>",
        "<AlertDialogTitle>",
        ad.title,
        "</AlertDialogTitle>",
        "<AlertDialogDescription>",
        ad.description,
        "</AlertDialogDescription>",
        "</AlertDialogHeader>",
        "<AlertDialogFooter>",
        "<AlertDialogCancel>",
        ad.cancel_btn_text,
        "</AlertDialogCancel>",
        "<AlertDialogAction>",
        ad.action_btn_text,
        "</AlertDialogAction>",
        "</AlertDialogFooter>",
        "</AlertDialogContent>",
    ]


def avatar_content(avatar: Avatar) -> list[str]:
    """Returns a list of strings for the `Avatar` content based on the components attributes."""
    src = src_attribute(avatar.src)
    alt = alt_attribute(avatar.alt)

    return [
        f"<AvatarImage {src} {alt} />",
        f"<AvatarFallback>{avatar.fallback_text}</AvatarFallback>",
    ]


def input_otp_content(otp: InputOTP) -> list[str]:
    """Returns a list of strings for the `InputOTP` content based on the components attributes."""
    content = []

    slot_group_size = otp.num_inputs // otp.num_groups
    slot_idx = 0

    group_tag = "InputOTPGroup>"

    for group_idx in range(otp.num_groups):
        content.append(f"<{group_tag}")
        for _ in range(slot_group_size):
            content.append(f"<InputOTPSlot index={{{slot_idx}}} />")
            slot_idx += 1
        content.append(f"</{group_tag}")

        if otp.num_groups > 1 and group_idx + 1 != otp.num_groups:
            content.append("<InputOTPSeparator />")

    return content


def button_content(btn: Button) -> list[str]:
    """Returns a list of strings for the `Button` content based on the components attributes."""
    text = string_icon_content(btn.content)

    if btn.url:
        text = build_component(Link(href=btn.url, text=compress(text)))

    return text


def toggle_content(toggle: Toggle) -> list[str]:
    """Returns a list of strings for the `Toggle` content based on the components attributes."""
    return string_icon_content(toggle.content)


def toggle_group_content(tg: ToggleGroup) -> list[str]:
    """Returns a list of strings for the `ToggleGroup` content based on the components attributes."""
    content = []

    for item in tg.items:
        inner_content = build_component(item, full_shell=True)

        # Update `<Toggle>` to `<ToggleGroupItem>`
        inner_content = (
            compress(inner_content)
            .replace("<Toggle", "<ToggleGroupItem")
            .replace("</Toggle", "</ToggleGroupItem")
        )
        content.append(inner_content)

    return content


def pagination_content(page: Pagination) -> list[str]:
    """Returns a list of strings for the `Pagination` content based on the components attributes."""

    def wrap_item(content: str | list[str]) -> list[str]:
        if isinstance(content, str):
            return ["<PaginationItem>", content, "</PaginationItem>"]
        else:
            return ["<PaginationItem>", *content, "</PaginationItem>"]

    def set_on_clicks(symbol: str) -> list[str]:
        return [
            f"{page.start_idx_name[1]}({page.start_idx_name[0]} {symbol} itemsPerPage);",
            f"{page.end_idx_name[1]}({page.end_idx_name[0]} {symbol} itemsPerPage);",
        ]

    def disable_btn_styles(name: str, idx: int | str) -> str:
        return f'className={{{name} === {idx} ? "pointer-events-none opacity-50" : undefined}}'

    content = [
        "<PaginationContent>",
        *wrap_item(
            [
                "<PaginationPrevious ",
                disable_btn_styles(page.start_idx_name[0], 0),
                " onClick={() => {",
                *set_on_clicks("-"),
                "}} />",
            ]
        ),
    ]

    for idx, link in enumerate(page.links, start=1):
        link_content = f'<PaginationLink href="{link}" isActive>{idx}</PaginationLink>'

        if idx > 1:
            link_content = link_content.replace(" isActive", "")

        content.extend(wrap_item(link_content))

    if page.ellipsis:
        content.extend(wrap_item("<PaginationEllipsis />"))

    content.extend(
        wrap_item(
            [
                "<PaginationNext ",
                disable_btn_styles(page.end_idx_name[0], "maxitems"),
                " onClick={() => {",
                *set_on_clicks("+"),
                "}} />",
            ]
        )
    )
    content.append("</PaginationContent>")
    return content


# Parent Components
def scroll_area_content(sa: ScrollArea) -> tuple[list[str], JSXComponentExtras]:
    """Returns a list of strings and component storage for the `ScrollArea` content based on the components attributes."""
    if isinstance(sa.content, str):
        content = [sa.content]
        storage = JSXComponentExtras()
    else:
        content, storage = build_html_tag(sa.content, output_storage=True)

    return [*content, f'<ScrollBar orientation="{sa.orientation}" />'], storage


def tooltip_content(tt: Tooltip) -> tuple[list[str], JSXComponentExtras]:
    """Returns a list of strings and component storage for the `Tooltip` content based on the components attributes."""

    if isinstance(tt.trigger, str):
        trigger_content = [tt.trigger]
        storage = JSXComponentExtras()
    elif isinstance(tt.trigger, (LucideIcon, LucideIconWithText)):
        trigger_content, storage = build_icon(tt.trigger, output_storage=True)
    else:
        trigger_content, storage = build_component(tt.trigger, output_storage=True)

    return [
        "<Tooltip>",
        "<TooltipTrigger asChild>",
        *trigger_content,
        "</TooltipTrigger>",
        "<TooltipContent>",
        f"<p>{tt.text}</p>",
        "</TooltipContent>",
        "</Tooltip>",
    ], storage


def dropdown_menu_content(dd: DropdownMenu) -> tuple[list[str], JSXComponentExtras]:
    """Returns a list of strings and component storage for the `DropdownMenu` content based on the components attributes."""

    def trigger() -> tuple[list[str], JSXComponentExtras]:
        if isinstance(dd.trigger, str):
            return [
                add_wrapper("DropdownMenuTrigger", dd.trigger),
            ], JSXComponentExtras()
        else:
            trigger_content, storage = build_component(dd.trigger, output_storage=True)

            return [
                add_wrapper("DropdownMenuTrigger", trigger_content, attrs="asChild")
            ], storage

    def radio_group(rg: DDMRadioGroup) -> list[str]:
        if rg.values:
            item_content = [
                add_wrapper("DropdownMenuRadioItem", text, f'value="{value}"')
                for text, value in zip(rg.texts, rg.values)
            ]
        else:
            item_content = [
                add_wrapper(
                    "DropdownMenuRadioItem",
                    text,
                    f'value="{text.split(" ")[0].lower()}"',
                )
                for text in rg.texts
            ]

        return [
            add_wrapper(
                "DropdownMenuRadioGroup",
                item_content,
                "value={position} onValueChange={setPosition}",
            )
        ]

    def checkbox_group(cbg: DDMCheckboxGroup) -> list[str]:
        content = []
        for item, (start_name, end_name) in zip(cbg.texts, cbg.state_name_pairs):
            content.extend(
                [
                    add_wrapper(
                        "DropdownMenuCheckboxItem",
                        item,
                        f"checked={{{start_name}}} onCheckedChange={{{end_name}}}",
                    )
                ]
            )

        return content

    def create_ddm_item(item: DDMItem) -> tuple[list[str], JSXComponentExtras]:
        """Handles the creation of the `DDMItem` model content."""
        content, storage = [], JSXComponentExtras()
        icon_content, shortcut_content = [None], [None]
        item_attrs = "disabled" if item.disabled else ""

        if item.icon:
            icon_content, icon_storage = build_icon(item.icon, output_storage=True)
            add_to_storage(storage, icon_storage, extend=True)

        if item.shortcut_key:
            shortcut_content = [add_wrapper("DropdownMenuShortcut", item.shortcut_key)]

        if isinstance(item.text, str):
            text_content = [
                *icon_content,
                f"<span>{item.text}</span>",
                *shortcut_content,
            ]
        else:
            link_content, link_storage = build_component(item.text, output_storage=True)
            start, middle, end = link_content
            text_content = [
                start,
                *icon_content,
                f"<span>{middle}</span>",
                *shortcut_content,
                end,
            ]
            item_attrs += " asChild"
            add_to_storage(storage, link_storage, extend=True)

        content.extend([text_str for text_str in text_content if text_str is not None])
        content = [
            add_wrapper(
                name="DropdownMenuItem",
                content=content,
                attrs=item_attrs.lstrip(),
            )
        ]
        return content, storage

    def create_str_item(item: str) -> list[str]:
        return [add_wrapper("DropdownMenuItem", item)]

    def ddm_group_iteration(
        item: str | DDMSubGroup | DDMItem | DDMSeparator,
    ) -> tuple[list[str], JSXComponentExtras]:
        if isinstance(item, str):
            item_content = create_str_item(item)
            item_storage = None
        elif isinstance(item, DDMSubGroup):
            item_content, item_storage = ddm_sub_group(item)
        elif isinstance(item, DDMSeparator):
            item_content = [item.content_str]
            item_storage = None
        else:
            item_content, item_storage = create_ddm_item(item)

        return item_content, item_storage

    def ddm_sub_group(sub: DDMSubGroup) -> tuple[list[str], JSXComponentExtras]:
        inner_content, storage = create_ddm_item(sub.trigger)
        inner_content[0] = inner_content[0].replace(
            "DropdownMenuItem", "DropdownMenuSubTrigger"
        )

        if sub.label:
            inner_content.append(add_wrapper("DropdownMenuLabel", sub.label))

        inner_item_content = []
        for item in sub.items:
            item_content, item_storage = ddm_group_iteration(item)

            if item_storage:
                storage = add_to_storage(storage, item_storage, extend=True)

            inner_item_content.extend(item_content)

        inner_content = [
            *inner_content,
            add_wrapper(
                "DropdownMenuPortal",
                add_wrapper("DropdownMenuSubContent", inner_item_content),
            ),
        ]

        content = [add_wrapper("DropdownMenuSub", inner_content)]
        return content, storage

    def ddm_group(group: DDMGroup) -> tuple[list[str], JSXComponentExtras]:
        inner_content = []
        storage = JSXComponentExtras()

        if group.label:
            inner_content.append(add_wrapper("DropdownMenuLabel", group.label))

        for item in group.items:
            item_content, item_storage = ddm_group_iteration(item)

            if item_storage:
                storage = add_to_storage(storage, item_storage, extend=True)

            inner_content.extend(item_content)

        content = [add_wrapper("DropdownMenuGroup", inner_content)]
        return content, storage

    def handle_groups(items: list[DDMGroup]) -> tuple[list[str], JSXComponentExtras]:
        content = []
        storage = JSXComponentExtras()

        for item in items:
            item_content, item_storage = ddm_group(item)
            content.extend(item_content)
            storage = add_to_storage(storage, item_storage, extend=True)
            content.append(DDMSeparator().content_str)

        content.pop()  # Remove trailing separator
        return content, storage

    content, storage = trigger()
    inner_content = []

    if dd.label:
        inner_content.extend(
            [add_wrapper("DropdownMenuLabel", dd.label), DDMSeparator().content_str]
        )

    group_storage = None
    if isinstance(dd.items, DDMRadioGroup):
        group_content = radio_group(dd.items)
    elif isinstance(dd.items, DDMCheckboxGroup):
        group_content = checkbox_group(dd.items)
    elif isinstance(dd.items, (DDMGroup, list)):
        if isinstance(dd.items, DDMGroup):
            dd.items = [dd.items]
        group_content, group_storage = handle_groups(dd.items)

    if group_storage:
        storage = add_to_storage(storage, group_storage, extend=True)

    inner_content.extend(group_content)
    content = [
        *content,
        add_wrapper("DropdownMenuContent", inner_content, 'className="w-56"'),
    ]
    return content, storage
