from pydantic_core import Url

from zentra_models.cli.templates.ui.attributes import (
    accordion_attributes,
    alt_attribute,
    other_attribute,
    calendar_attributes,
    input_otp_attributes,
    param_attr,
    nextjs_link_attributes,
    progress_attributes,
    size_attribute,
    slider_attributes,
    src_attribute,
    str_attr,
    style_attribute,
    toggle_attributes,
)
from zentra_models.cli.templates.ui.content import (
    accordion_content,
    alert_content,
    aspect_ratio_content,
    avatar_content,
    breadcrumb_content,
    checkbox_content,
    collapsible_content,
    combobox_content,
    command_content,
    date_picker_content,
    dropdown_menu_content,
    input_otp_content,
    pagination_content,
    popover_content,
    radio_button_content,
    radio_group_content,
    scroll_area_content,
    select_content,
    select_group_content,
    skeleton_content,
    table_content,
    alert_dialog_content,
    text_content,
    tooltip_content,
)
from zentra_models.cli.templates.ui.imports import (
    alert_imports,
    button_imports,
    calendar_imports,
    collapsible_imports,
    date_picker_imports,
    image_imports,
    input_opt_imports,
    radio_group_imports,
    slider_imports,
    static_img_imports,
    toggle_group_imports,
    toggle_imports,
)
from zentra_models.cli.templates.ui.logic import (
    calendar_logic,
    collapsible_logic,
    combobox_logic,
    pagination_logic,
    progress_logic,
)


# Dictionary of components with containers around them
# (classname, attributes)
COMPONENTS_TO_WRAP = {
    "Checkbox": 'className="flex items-top space-x-2"',
}


# Unique components that need a "use client" import but don't use hooks
USE_CLIENT_COMPONENTS = [
    "Checkbox",
]


COMPONENT_ATTR_MAPPING = {
    "Calendar": lambda comp: calendar_attributes(comp),
    "InputOTP": lambda comp: input_otp_attributes(comp),
    "Link": lambda comp: nextjs_link_attributes(comp),
    "Slider": lambda comp: slider_attributes(comp),
    "Toggle": lambda comp: toggle_attributes(comp),
    "Accordion": lambda comp: accordion_attributes(comp),
    "Progress": lambda comp: progress_attributes(comp),
}


COMMON_ATTR_MAPPING = {
    "id": lambda value: str_attr("id", value),
    "url": lambda value: "asChild" if value else None,
    "href": lambda value: str_attr("href", value)
    if isinstance(value, (str, Url))
    else None,
    "name": lambda value: str_attr("htmlFor", value),
    "type": lambda value: str_attr("type", value),
    "placeholder": lambda value: str_attr("placeholder", value),
    "variant": lambda value: str_attr("variant", value) if value != "default" else None,
    "size": lambda value: size_attribute(value),
    "disabled": lambda value: "disabled" if value else None,
    "apiEndpoint": lambda value: str_attr("apiEndpoint", value),
    "num_inputs": lambda value: param_attr("maxLength", value),
    "key": lambda key: param_attr("key", key),
    "new_tab": lambda value: str_attr("target", "_blank") if value else None,
    "styles": lambda value: style_attribute(value),
    "src": lambda value: src_attribute(value),
    "alt": lambda alt: alt_attribute(alt),
    "width": lambda width: param_attr("width", width),
    "height": lambda height: param_attr("height", height),
    "checked": lambda checked: param_attr("checked", checked) if checked else None,
    "pressed": lambda pressed: param_attr("pressed", pressed),
    "color": lambda value: str_attr("color", value),
    "stroke_width": lambda value: param_attr("strokeWidth", value),
    "min": lambda value: param_attr("min", value),
    "max": lambda value: param_attr("max", value),
    "step": lambda value: param_attr("step", value),
    "orientation": lambda value: str_attr("orientation", value),
    "default_value": lambda value: str_attr("defaultValue", value),
    "fill": lambda value: "fill" if value else None,
    "ratio": lambda value: param_attr("ratio", value),
    "mode": lambda value: str_attr("mode", value),
    "open": lambda value: param_attr("open", value),
    "open_change": lambda value: param_attr("onOpenChange", value),
    "other": lambda value: other_attribute(value),
    "value": lambda value: str_attr("value", value),
    "child": lambda value: "asChild" if value else None,
    "index": lambda value: param_attr("index", value),
    "is_active": lambda value: "isActive" if value else None,
    "on_click": lambda value: param_attr("onClick", value),
}


EXTRA_IMPORTS_MAPPING = {
    "Calendar": lambda comp: calendar_imports(comp),
    "Collapsible": lambda _: collapsible_imports(),
    "InputOTP": lambda comp: input_opt_imports(comp),
    "RadioGroup": lambda _: radio_group_imports(),
    "StaticImage": lambda img: static_img_imports(img),
    "Image": lambda comp: image_imports(comp),
    "Avatar": lambda comp: image_imports(comp),
    "Slider": lambda _: slider_imports(),
    "Alert": lambda comp: alert_imports(comp),
    "Button": lambda comp: button_imports(comp),
    "Toggle": lambda comp: toggle_imports(comp),
    "ToggleGroup": lambda comp: toggle_group_imports(comp),
    "DatePicker": lambda _: date_picker_imports(),
}


COMPONENT_CONTENT_MAPPING = {
    "Checkbox": lambda cb: checkbox_content(cb),
    "Collapsible": lambda comp: collapsible_content(comp),
    "RadioButton": lambda rb: radio_button_content(rb),
    "RadioGroup": lambda rg: radio_group_content(rg),
    "SelectGroup": lambda gp: select_group_content(gp),
    "Select": lambda select: select_content(select),
    "Alert": lambda alert: alert_content(alert),
    "AlertDialog": lambda ad: alert_dialog_content(ad),
    "Avatar": lambda avatar: avatar_content(avatar),
    "InputOTP": lambda otp: input_otp_content(otp),
    "Pagination": lambda comp: pagination_content(comp),
    "Accordion": lambda comp: accordion_content(comp),
    "Skeleton": lambda comp: skeleton_content(comp),
    "Table": lambda comp: table_content(comp),
    # Parent components
    "ScrollArea": lambda sa: scroll_area_content(sa),
    "Tooltip": lambda tt: tooltip_content(tt),
    "DropdownMenu": lambda dd: dropdown_menu_content(dd),
    "Breadcrumb": lambda bc: breadcrumb_content(bc),
    "AspectRatio": lambda ar: aspect_ratio_content(ar),
    "Popover": lambda pop: popover_content(pop),
    "DatePicker": lambda dp: date_picker_content(dp),
    "Command": lambda cmd: command_content(cmd),
    "Combobox": lambda box: combobox_content(box),
}


COMMON_CONTENT_MAPPING = {
    "text": lambda value: text_content(value),
}


LOGIC_MAPPING = {
    "Calendar": lambda comp: calendar_logic(comp),
    "Collapsible": lambda comp: collapsible_logic(comp),
    "Pagination": lambda comp: pagination_logic(comp),
    "Progress": lambda comp: progress_logic(comp),
    "Combobox": lambda comp: combobox_logic(comp),
}


MAPPING_DICT = {
    "common_attrs": COMMON_ATTR_MAPPING,
    "component_attrs": COMPONENT_ATTR_MAPPING,
    "common_content": COMMON_CONTENT_MAPPING,
    "component_content": COMPONENT_CONTENT_MAPPING,
    "common_logic": LOGIC_MAPPING,
    "additional_imports": EXTRA_IMPORTS_MAPPING,
    "wrappers": COMPONENTS_TO_WRAP,
    "use_client_map": USE_CLIENT_COMPONENTS,
}

ATTR_DICT = {
    "common": COMMON_ATTR_MAPPING,
    "model": COMPONENT_ATTR_MAPPING,
}

CONTENT_DICT = {
    "common": COMMON_CONTENT_MAPPING,
    "model": COMPONENT_CONTENT_MAPPING,
}
