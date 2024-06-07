from cli.templates.builders import add_to_storage
from cli.templates.builders.controller import BuildController
from cli.templates.storage import JSXComponentExtras
from cli.templates.ui.attributes import (
    alt_attribute,
    param_attr,
    src_attribute,
    str_attr,
)
from cli.templates.utils import compress, str_to_list, text_content

from zentra.base import ZentraModel
from zentra.ui.control import Checkbox, RadioGroup
from zentra.core import Component
from zentra.base.html import HTMLTag
from zentra.core.constants import PARAMETER_PREFIX
from zentra.core.enums.ui import CalendarMode, DDMenuType
from zentra.core.html import Div, HTMLContent
from zentra.core.react import LucideIcon, LucideIconWithText
from zentra.nextjs import Link, NextJs
from zentra.ui.control import (
    Button,
    Collapsible,
    Combobox,
    DatePicker,
    InputOTP,
    Label,
    Pagination,
    RadioButton,
    ScrollArea,
    Select,
    SelectGroup,
    Toggle,
    ToggleGroup,
)
from zentra.ui.child import (
    ActionModel,
    CancelModel,
    ContentModel,
    DescriptionModel,
    FooterModel,
    GroupModel,
    HeaderModel,
    ItemModel,
    LabelModel,
    SeparatorModel,
    TitleModel,
    TriggerModel,
    ValueModel,
)
from zentra.ui.child.ddm import DDMCheckboxGroup, DDMRadioGroup
from zentra.ui.modal import Popover
from zentra.ui.navigation import (
    BCDropdownMenu,
    BCItem,
    Breadcrumb,
    Command,
    CommandGroup,
    CommandItem,
    CommandMap,
    DDMGroup,
    DDMItem,
    DDMSeparator,
    DDMSubMenu,
    DropdownMenu,
)
from zentra.ui.notification import Alert, AlertDialog, Tooltip
from zentra.ui.presentation import (
    Accordion,
    AspectRatio,
    Avatar,
    Skeleton,
    SkeletonGroup,
    SkeletonShell,
    Table,
    TableCell,
    TableMap,
    TableRow,
)


def controller() -> BuildController:
    """A helper function to create a `BuildController`."""
    from cli.templates.ui.mappings import CONTROLLER_MAPPINGS

    return BuildController(mappings=CONTROLLER_MAPPINGS)


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


def handle_menu_item(
    item: DDMItem | CommandItem, comp_name: str
) -> tuple[list[str], JSXComponentExtras]:
    """A helper function for handling the creation of a single menu item's content."""
    content, storage = [], JSXComponentExtras()
    icon_content, shortcut_content = [None], [None]
    item_attrs = "disabled" if item.disabled else ""

    if item.icon:
        icon_content, icon_storage = build_icon(item.icon, output_storage=True)
        add_to_storage(storage, icon_storage, extend=True)

    if item.shortcut_key:
        shortcut_content = [add_wrapper(f"{comp_name}Shortcut", item.shortcut_key)]

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
            name=f"{comp_name}Item",
            content=content,
            attrs=item_attrs.lstrip(),
        )
    ]
    return content, storage


def build_trigger(
    variant: str, content: Button | str
) -> tuple[list[str], JSXComponentExtras]:
    """A helper function to build `TriggerModel` child components. Returns a tuple in the form: `(content, JSXComponentExtras)`."""
    model = TriggerModel(variant=variant)

    if isinstance(content, str):
        return model.build(content), JSXComponentExtras()
    else:
        content, storage = build_component(content, output_storage=True)
        return model.build(content, attrs="asChild"), storage


def build_label(variant: str, content: str | list[str]) -> list[str]:
    """A helper function to build `LabelModel` child components. Returns the JSX content as a `list[string]`."""
    model = LabelModel(variant=variant)
    return model.build(content)


def build_separator(
    variant: str, content: str | list[str] = None, styles: str = None
) -> list[str]:
    """A helper function to build `SeparatorModel` child components. Returns the JSX content as a `list[string]`."""
    model = SeparatorModel(variant=variant, styles=styles)
    return model.build(content)


def build_content(
    variant: str, content: str | list[str] = None, styles: str = None
) -> list[str]:
    """A helper function to build `ContentModel` child components. Returns the JSX content as a `list[string]`."""
    model = ContentModel(variant=variant, styles=styles)
    return model.build(content)


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


def checkbox_content(cb: Checkbox) -> list[ZentraModel]:
    """Returns a `ZentraModel` for the `Checkbox` content based on the components attributes."""
    items = [
        Label(
            name=cb.id,
            text=cb.label,
            styles="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70",
        )
    ]
    items_style = "items-center"

    if cb.text:
        items_style = "items-top"
        items = [
            Div(
                styles="grid gap-1.5 leading-none",
                content=[
                    *items,
                    HTMLContent(
                        tag="p", styles="text-sm text-muted-foreground", text=cb.text
                    ),
                ],
            ),
        ]

    return [
        Div(
            styles=f"flex {items_style} space-x-2",
            content=[cb, *items],
        )
    ]


def collapsible_content(comp: Collapsible) -> list[ZentraModel]:
    """Returns a list of `ZentraModels` for the `Collapsible` content based on the components attributes."""
    items = []
    if len(comp.items) > 1:
        for text in comp.items[1:]:
            items.append(
                Div(
                    styles="rounded-md border px-4 py-3 font-mono text-sm", content=text
                )
            )

    return [
        Div(
            styles="flex items-center justify-between space-x-4 px-4",
            content=[
                HTMLContent(tag="h4", styles="text-sm font-semibold", text=comp.title),
                TriggerModel(
                    variant="collapsible",
                    content=Button(
                        variant="ghost",
                        size="sm",
                        styles="w-9 p-0",
                        content=LucideIcon(
                            name="chevrons-up-down",
                            styles="h-4 w-4",
                            text=HTMLContent(
                                tag="span", styles="sr-only", text="Toggle"
                            ),
                        ),
                    ),
                    child=True,
                ),
            ],
        ),
        Div(
            styles="rounded-md border px-4 py-3 font-mono text-sm",
            content=comp.items[0],
        ),
        ContentModel(variant="collapsible", styles="space-y-2", content=items),
    ]


def radio_button_content(rb: RadioButton) -> list[ZentraModel]:
    """Returns a list of `ZentraModels` for the `RadioButton` content based on the components attributes."""
    return [
        Div(
            styles="flex items-center space-x-2",
            content=[
                rb,
                Label(name=rb.id, text=rb.text),
            ],
        )
    ]


def radio_group_content(rg: RadioGroup) -> list[ZentraModel]:
    """Returns a list of `ZentraModels` for the `RadioGroup` content based on the components attributes."""
    content = []
    for item in rg.items:
        content.extend(radio_button_content(item))
    return content


def select_group_content(group: SelectGroup) -> list[ZentraModel]:
    """Returns a list of `ZentraModels` for the `SelectGroup` content based on the components attributes."""
    content = []
    if group.label:
        label = LabelModel(variant="select", content=group.label)
        content.append(label)

    for item in group.items:
        value = item.split()[0].lower()
        content.append(ItemModel(variant="select", value=value, content=item))

    return [GroupModel(variant="select", content=content)]


def select_content(select: Select) -> list[ZentraModel]:
    """Returns a list of `ZentraModels` for the `Select` content based on the components attributes."""
    if isinstance(select.groups, SelectGroup):
        select.groups = [select.groups]

    groups = []
    for group in select.groups:
        groups.extend(select_group_content(group))

    return [
        TriggerModel(
            variant="select",
            styles="w-[180px]",
            content=ValueModel(variant="select", placeholder=select.display_text),
        ),
        ContentModel(
            variant="select",
            content=groups,
        ),
    ]


def alert_content(alert: Alert) -> list[ZentraModel]:
    """Returns a list of `ZentraModels` for the `Alert` content based on the components attributes."""
    content = [
        TitleModel(variant="alert", content=alert.title),
        DescriptionModel(variant="alert", content=alert.description),
    ]

    if alert.icon:
        content.insert(0, LucideIcon(name=alert.icon, styles="h-4 w-4"))

    return content


def alert_dialog_content(ad: AlertDialog) -> list[ZentraModel]:
    """Returns a list of `ZentraModels` for the `AlertDialog` content based on the components attributes."""

    def extend_or_append(item, content: list) -> list:
        if not isinstance(item, list):
            content.append(item)
        else:
            content.extend(item)
        return content

    def footer_content() -> FooterModel:
        content = []
        if ad.footer:
            content = extend_or_append(ad.footer, content)

        if ad.cancel_btn:
            content.append(CancelModel(variant="alert_dialog", content=ad.cancel_btn))

        if ad.action_btn:
            content.append(ActionModel(variant="alert_dialog", content=ad.action_btn))

        return FooterModel(variant="alert_dialog", content=content)

    def header_content() -> HeaderModel:
        content = []

        if ad.title:
            content.append(TitleModel(variant="alert_dialog", content=ad.title))

        if ad.header:
            content = extend_or_append(ad.header, content)

        if ad.description:
            content.append(
                DescriptionModel(variant="alert_dialog", content=ad.description)
            )

        return HeaderModel(variant="alert_dialog", content=content)

    as_child = True if isinstance(ad.trigger, Button) else False

    main_content = []

    if ad.header or ad.title or ad.description:
        main_content.append(header_content())

    output = [
        TriggerModel(variant="alert_dialog", content=ad.trigger, child=as_child),
    ]

    if ad.footer or ad.cancel_btn or ad.action_btn:
        main_content.append(footer_content())

    output.append(ContentModel(variant="alert_dialog", content=main_content))
    return output


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


def accordion_content(acc: Accordion) -> list[str]:
    """Returns a list of strings for the `Accordion` content based on the components attributes."""
    content = []

    for idx, item in enumerate(acc.items, start=1):
        item_attrs = compress(
            [
                f'value="item-{idx}"',
                "disabled" if item.disabled else "",
            ],
            chars=" ",
        )

        item_content = [
            add_wrapper("AccordionTrigger", item.title),
            add_wrapper("AccordionContent", item.content),
        ]

        item_content = add_wrapper(
            "AccordionItem", item_content, attrs=item_attrs.strip()
        )
        content.append(item_content)

    return content


def skeleton_content(skel: Skeleton) -> list[str]:
    """Returns a list of strings for the `Skeleton` content based on the components attributes."""

    def shell(shell: SkeletonShell) -> str:
        return f"<Skeleton{f' {str_attr("className", shell.styles) if shell.styles else ''}'} />"

    def group(g: SkeletonGroup) -> list[str]:
        content = []
        for item in g.items:
            content.append(shell(item))

        return [add_wrapper("div", content, str_attr("className", g.styles))]

    def handle_list(items_list: list[SkeletonShell | SkeletonGroup]) -> list[str]:
        inner_content = []
        for item in items_list:
            if isinstance(item, SkeletonShell):
                inner_content.append(shell(item))
            elif isinstance(item, SkeletonGroup):
                inner_content.extend(group(item))
        return inner_content

    def testimonial_content() -> list[str]:
        return build_component(
            Skeleton(
                preset="custom",
                items=[
                    SkeletonShell(styles="h-12 w-12 rounded-full"),
                    SkeletonGroup(
                        styles="space-y-2",
                        items=[
                            SkeletonShell(styles="h-4 w-[250px]"),
                            SkeletonShell(styles="h-4 w-[250px]"),
                        ],
                    ),
                ],
            )
        )[1:-1]

    def card_content() -> list[str]:
        return build_component(
            Skeleton(
                preset="custom",
                items=[
                    SkeletonShell(styles="h-[125px] w-[250px] rounded-xl"),
                    SkeletonGroup(
                        styles="space-y-2",
                        items=[
                            SkeletonShell(styles="h-4 w-[250px]"),
                            SkeletonShell(styles="h-4 w-[200px]"),
                        ],
                    ),
                ],
            )
        )[1:-1]

    def custom_content() -> list[str]:
        if isinstance(skel.items, (SkeletonShell, SkeletonGroup)):
            skel.items = [skel.items]
        return handle_list(skel.items)

    content_options = {
        "custom": custom_content,
        "testimonial": testimonial_content,
        "card": card_content,
    }
    return content_options[skel.preset]()


def table_content(table: Table) -> list[str]:
    """Returns a list of strings for the `Table` content based on the components attributes."""

    def cell(name: str, item: TableCell) -> str:
        attrs = [
            param_attr("colSpan", item.col_span) if item.col_span else None,
            str_attr("className", item.styles) if item.styles else None,
        ]
        attrs = compress([item for item in attrs if item is not None], chars=" ")
        return add_wrapper(name, text_content(item.text), attrs=attrs)

    def handle_list(
        wrap_name: str, cell_name: str, cell_list: list[str | TableCell]
    ) -> str:
        content = []

        for item in cell_list:
            if isinstance(item, str):
                content.append(add_wrapper(cell_name, text_content(item)))
            else:
                content.append(cell(cell_name, item))

        return add_wrapper(wrap_name, content)

    def handle_prefix(item: str) -> str:
        if item.startswith(PARAMETER_PREFIX):
            item = item.split(".")[len(PARAMETER_PREFIX) :]
            item = ".".join(item) if len(item) > 1 else item[0]
            return item

        return item

    def handle_cell_reformatting(
        param_name: str,
        row_cells: list[str | TableCell],
    ) -> list[str | TableCell]:
        param_text_cells = []

        for item in row_cells:
            if isinstance(item, str):
                item = handle_prefix(item)
                param_text_cells.append(f"$.{param_name}.{item}")
            else:
                item.text = handle_prefix(item.text)
                item.text = f"$.{param_name}.{item.text}"
                param_text_cells.append(item)

        return param_text_cells

    def handle_table_map(wrap_name: str, cell_name: str, map: TableMap) -> str:
        map_attrs = f"{map.param_name}{', mapIdx' if map.map_idx else ''}"
        map.row.cells = handle_cell_reformatting(map.param_name, map.row.cells)

        content = compress(
            [
                "{" + f"{map.obj_name}.map(({map_attrs}) => (",
                handle_list(wrap_name, cell_name, map.row.cells),
                "))}",
            ]
        )

        if map.row.key is not None or map.map_idx:
            if map.map_idx:
                key_attr = param_attr("key", "mapIdx")
            else:
                key_val = handle_prefix(map.row.key)
                key_attr = param_attr("key", f"$.{map.param_name}.{key_val}")

            content = content.replace("<TableRow>", f"<TableRow {key_attr}>")

        return content

    def handle_body(
        wrap_name: str, cell_name: str, cell_list: list[TableRow] | TableMap
    ) -> str:
        content = []
        if isinstance(cell_list, list):
            for item in cell_list:
                content.append(handle_list(wrap_name, cell_name, item.cells))
        else:
            content.append(handle_table_map(wrap_name, cell_name, cell_list))

        return content

    content = []

    if table.caption:
        content.append(add_wrapper("TableCaption", table.caption))

    content.extend(
        [
            add_wrapper(
                "TableHeader", handle_list("TableRow", "TableHead", table.headings)
            ),
            add_wrapper("TableBody", handle_body("TableRow", "TableCell", table.body)),
        ]
    )

    if table.footer:
        content.append(
            add_wrapper(
                "TableFooter", handle_list("TableRow", "TableCell", table.footer)
            )
        )

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
    setAsChild = True

    if isinstance(tt.trigger, str):
        trigger_content = [tt.trigger]
        setAsChild = False
        storage = JSXComponentExtras()
    elif isinstance(tt.trigger, (LucideIcon, LucideIconWithText)):
        trigger_content, storage = build_icon(tt.trigger, output_storage=True)
    else:
        trigger_content, storage = build_component(tt.trigger, output_storage=True)

    return [
        add_wrapper(
            "Tooltip",
            [
                add_wrapper(
                    "TooltipTrigger",
                    trigger_content,
                    attrs=f'{"asChild" if setAsChild else ''}',
                ),
                add_wrapper("TooltipContent", f"<p>{tt.text}</p>"),
            ],
        ),
    ], storage


def dropdown_menu_content(dd: DropdownMenu) -> tuple[list[str], JSXComponentExtras]:
    """Returns a list of strings and component storage for the `DropdownMenu` content based on the components attributes."""

    def create_str_item(item: str) -> list[str]:
        return [add_wrapper("DropdownMenuItem", item)]

    def ddm_group_iteration(
        item: str | DDMSubMenu | DDMItem | DDMSeparator,
    ) -> tuple[list[str], JSXComponentExtras]:
        item_storage = JSXComponentExtras()

        if isinstance(item, str):
            item_content = create_str_item(item)
        elif isinstance(item, DDMSubMenu):
            item_content, item_storage = ddm_sub_group(item)
        elif isinstance(item, DDMSeparator):
            item_content = build_separator("dropdown_menu")
        else:
            item_content, item_storage = handle_menu_item(item, "DropdownMenu")

        return item_content, item_storage

    def ddm_sub_group(sub: DDMSubMenu) -> tuple[list[str], JSXComponentExtras]:
        inner_content, storage = handle_menu_item(sub.trigger, "DropdownMenu")
        inner_content[0] = inner_content[0].replace(
            "DropdownMenuItem", "DropdownMenuSubTrigger"
        )

        if sub.label:
            inner_content.append(build_label("dropdown_menu", sub.label))

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
        inner_content, storage = [], JSXComponentExtras()

        if group.label:
            inner_content.extend(build_label("dropdown_menu", group.label))

        for item in group.items:
            item_content, item_storage = ddm_group_iteration(item)

            if item_storage:
                storage = add_to_storage(storage, item_storage, extend=True)

            inner_content.extend(item_content)

        content = [add_wrapper("DropdownMenuGroup", inner_content)]
        return content, storage

    def handle_groups(items: list[DDMGroup]) -> tuple[list[str], JSXComponentExtras]:
        content, storage = [], JSXComponentExtras()

        for item in items:
            item_content, item_storage = ddm_group(item)
            content.extend(item_content)
            storage = add_to_storage(storage, item_storage, extend=True)
            content.extend(build_separator("dropdown_menu"))

        content.pop()  # Remove trailing separator
        return content, storage

    content, storage = build_trigger("dropdown_menu", dd.trigger)
    inner_content = []

    if dd.label:
        inner_content.extend(
            [
                *build_label("dropdown_menu", dd.label),
                *build_separator("dropdown_menu"),
            ]
        )

    if dd.type == DDMenuType.CHECKBOX.value:
        cbg = DDMCheckboxGroup(items=dd.items)
        group_content = cbg.content()
        storage.logic.extend(cbg.logic())

    elif dd.type == DDMenuType.RADIO.value:
        rg = DDMRadioGroup(items=dd.items)
        group_content = rg.content()
        storage.logic.extend(rg.logic())

    elif isinstance(dd.items, (DDMGroup, list)):
        if isinstance(dd.items, DDMGroup):
            dd.items = [dd.items]
        group_content, group_storage = handle_groups(dd.items)

        if group_storage:
            storage = add_to_storage(storage, group_storage, extend=True)

    inner_content.extend(group_content)
    content = [
        *content,
        *build_content("dropdown_menu", inner_content, styles="w-56"),
    ]
    return content, storage


def breadcrumb_content(bc: Breadcrumb) -> tuple[list[str], JSXComponentExtras]:
    """Returns a list of strings and component storage for the `Breadcrumb` content based on the components attributes."""

    def bc_item(item: BCItem) -> str:
        return add_wrapper("BreadcrumbLink", item.text, attrs=f'href="{item.href}"')

    def tidy_ddm_menu_content(content: str) -> str:
        """Format content into the required format."""
        return (
            compress(content)
            .replace(
                "DropdownMenuTrigger asChild",
                'DropdownMenuTrigger className="flex items-center gap-1"',
            )
            .replace("<Button>\n", "")
            .replace("</Button>\n", "")
            .replace(
                'DropdownMenuContent className="w-56"',
                'DropdownMenuContent align="start"',
            )
        )

    def bc_menu(ddm: BCDropdownMenu) -> tuple[str, JSXComponentExtras]:
        item_content: list[DDMItem] = []
        for item in ddm.items:
            item_content.append(DDMItem(text=Link(href=item.href, text=item.text)))

        bc_ddm = DropdownMenu(
            trigger=Button(content=ddm.trigger.content_str),
            items=DDMGroup(items=item_content),
        )

        menu_content, ddm_storage = build_component(bc_ddm, output_storage=True)
        menu_content = tidy_ddm_menu_content(menu_content)

        # Remove 'Button' import
        storage.imports.extend(
            [
                imp_str
                for imp_str in str_to_list(ddm_storage.imports[0])
                if "Button" not in imp_str
            ]
        )

        return menu_content, storage

    def bc_seperator() -> tuple[str, JSXComponentExtras]:
        if bc.custom_sep:
            content, storage = build_icon(
                LucideIcon(name=bc.custom_sep, styles=None), output_storage=True
            )
            content = compress(build_separator("breadcrumb", content))
            return content, storage

        return compress(build_separator("breadcrumb")), JSXComponentExtras()

    content, storage = [], JSXComponentExtras()

    sep_content, sep_storage = bc_seperator()
    storage = add_to_storage(storage, sep_storage, extend=True)

    for item in bc.items:
        if isinstance(item, BCItem):
            item_content = bc_item(item)
        else:
            item_content, menu_storage = bc_menu(item)
            storage = add_to_storage(storage, menu_storage, extend=True)

        content.append(add_wrapper("BreadcrumbItem", item_content))
        content.append(sep_content)

    content.append(
        add_wrapper("BreadcrumbItem", add_wrapper("BreadcrumbPage", bc.page_name))
    )
    content = [add_wrapper("BreadcrumbList", content)]
    return content, storage


def aspect_ratio_content(ar: AspectRatio) -> tuple[list[str], JSXComponentExtras]:
    """Returns a list of strings for the `AspectRatio` content based on the components attributes."""
    img_content, storage = build_component(ar.img, output_storage=True)
    return img_content, storage


def popover_content(pop: Popover) -> tuple[list[str], JSXComponentExtras]:
    """Returns a list of strings for the `Popover` content based on the components attributes."""
    if isinstance(pop.content, str):
        inner_content, storage = [pop.content], JSXComponentExtras()
    else:
        inner_content, storage = build_html_tag(pop.content, output_storage=True)

    if isinstance(pop.trigger, str):
        trigger_content = [pop.trigger]
        setAsChild = False
    else:
        trigger_content, trigger_storage = build_component(
            pop.trigger, output_storage=True
        )
        setAsChild = True
        storage = add_to_storage(storage, trigger_storage, extend=True)

    content = [
        add_wrapper(
            "PopoverTrigger",
            trigger_content,
            attrs=f'{"asChild" if setAsChild else ''}',
        ),
        add_wrapper(
            "PopoverContent",
            inner_content,
            attrs=f'{str_attr("className", pop.styles) if pop.styles else ''}',
        ),
    ]
    return content, storage


def date_picker_content(dp: DatePicker) -> tuple[list[str], JSXComponentExtras]:
    """Returns a list of strings for the `DatePicker` content based on the components attributes."""

    def handle_range_mode_content(content: list[str]) -> list[str]:
        for idx, item in enumerate(reversed(content)):
            if "<Calendar " in item:
                content[-(idx + 1)] = item.replace(
                    "/>", "defaultMonth={datePickerDateRange?.from} />"
                )

            if "<PopoverContent" in item:
                content[-(idx + 1)] = item.replace(">", ' align="start">')
                break

        return str_to_list(add_wrapper("div", content, attrs='className="grid gap-2"'))

    btn = Button(
        variant="outline",
        content=LucideIconWithText(
            name="calendar-days", text=compress(dp.trigger_text)
        ),
        styles=dp.trigger_styles,
    )

    calendar_content, cal_storage = build_component(dp.content, output_storage=True)
    popover = Popover(
        trigger=btn,
        content=calendar_content[0],
        styles=dp.styles,
    )

    content, storage = build_component(popover, output_storage=True)
    storage = add_to_storage(storage, cal_storage, extend=True)

    if dp.calendar_mode == CalendarMode.RANGE.value:
        content = handle_range_mode_content(content)

    return content, storage


def command_content(cmd: Command) -> tuple[list[str], JSXComponentExtras]:
    """Returns a list of strings for the `Command` content based on the components attributes."""

    def handle_map(map: CommandMap) -> tuple[list[str], JSXComponentExtras]:
        item_attrs = compress(
            [
                param_attr("key", f"{map.param_name}.value"),
                param_attr("value", f"{map.param_name}.value"),
            ],
            chars=" ",
        )
        item_content, storage = build_icon(
            LucideIcon(
                name="check",
                styles=f'cn("mr-2 h-4 w-4", value === {map.param_name}.value ? "opacity-100" : "opacity-0")',
            ),
            output_storage=True,
        )
        item_content.extend(text_content(map.text))

        content = [
            f'<CommandInput placeholder="{cmd.input_text}" />',
            add_wrapper("CommandEmpty", "No results found."),
            add_wrapper(
                "CommandGroup",
                [
                    "{" + f"{map.obj_name}.map(({map.param_name}) => (",
                    add_wrapper("CommandItem", item_content, attrs=item_attrs),
                    "))}",
                ],
            ),
        ]
        return content, storage

    def handle_list(items: list[CommandGroup]) -> tuple[list[str], JSXComponentExtras]:
        content, storage = [], JSXComponentExtras()

        for group in items:
            group_content, group_storage = cmd_group(group)
            content.extend(group_content)
            storage = add_to_storage(storage, group_storage, extend=True)

        content.pop(-1)  # remove extra separator

        cmd_list_content = add_wrapper(
            "CommandList",
            [add_wrapper("CommandEmpty", "No results found."), *content],
        )

        content = [
            f'<CommandInput placeholder="{cmd.input_text}" />',
            *str_to_list(cmd_list_content),
        ]
        return content, storage

    def cmd_group(group: CommandGroup) -> tuple[list[str], JSXComponentExtras]:
        content, storage = [], JSXComponentExtras()

        for item in group.items:
            if isinstance(item, str):
                content.append(add_wrapper("CommandItem", item))
            else:
                item_content, item_storage = handle_menu_item(item, "Command")
                storage = add_to_storage(storage, item_storage, extend=True)
                content.extend(item_content)

        group_attrs = f'heading="{group.heading}"' if group.heading else ""
        content = str_to_list(add_wrapper("CommandGroup", content, attrs=group_attrs))
        content.extend(build_separator("command"))
        return content, storage

    if isinstance(cmd.items, CommandMap):
        return handle_map(cmd.items)

    if isinstance(cmd.items, CommandGroup):
        cmd.items = [cmd.items]

    return handle_list(cmd.items)


def combobox_content(box: Combobox) -> tuple[list[str], JSXComponentExtras]:
    """Returns a list of strings for the `Combobox` content based on the components attributes."""

    def handle_cmd_content(content: list[str]) -> list[str]:
        for idx, item in enumerate(content):
            if "<CommandItem" in item:
                content[idx] = item.replace(
                    ">",
                    compress(
                        [
                            " onSelect={(currentValue) => {",
                            f'{box.value_state_names[1]}(currentValue === value ? "" : currentValue)',
                            f"{box.open_state_names[1]}(false)",
                            "}}>",
                        ]
                    ),
                )
                break

        return content

    content, storage = [], JSXComponentExtras()

    param_name = box.data.name[:2]
    cmd = Command(
        items=CommandMap(
            obj_name=box.data.name,
            param_name=param_name,
            text=f"{PARAMETER_PREFIX}{param_name}.label",
        ),
        input_text=box.search_text,
        styles=None,
    )

    cmd_content, cmd_storage = build_component(cmd, output_storage=True)
    cmd_content = handle_cmd_content(cmd_content)

    trigger = Button(
        content=LucideIconWithText(
            name="chevrons-up-down",
            styles="ml-2 h-4 w-4 shrink-0 opacity-50",
            text="{"
            + f'value ? {box.data.name}.find(({param_name}) => {param_name}.value === value)?.label : "{box.display_text}"'
            + "}",
            position="end",
        ),
        variant="outline",
        styles="w-[200px] justify-between",
        other={"role": "combobox", "aria-expanded": f"{PARAMETER_PREFIX}open"},
    )
    pop = Popover(
        trigger=trigger,
        content=compress(cmd_content),
        styles="w-[200px] p-0",
        open="open",
        open_change=box.open_state_names[1],
    )
    content, storage = build_component(pop, output_storage=True)
    storage = add_to_storage(storage, cmd_storage, extend=True)
    return content, storage
