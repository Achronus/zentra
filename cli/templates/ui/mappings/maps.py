from pydantic_core import Url

from cli.templates.ui.attributes import (
    alt_attribute,
    calendar_attributes,
    collapsible_attributes,
    input_otp_attributes,
    param_attr,
    nextjs_link_attributes,
    size_attribute,
    slider_attributes,
    src_attribute,
    str_attr,
    toggle_attributes,
)
from cli.templates.ui.content import (
    alert_content,
    avatar_content,
    button_content,
    checkbox_content,
    collapsible_content,
    input_otp_content,
    pagination_content,
    radio_group_content,
    scroll_area_content,
    select_content,
    text_alert_dialog_content,
    text_content,
    toggle_content,
    toggle_group_content,
    tooltip_content,
)
from cli.templates.ui.imports import (
    alert_imports,
    button_imports,
    collapsible_imports,
    image_imports,
    input_opt_imports,
    radio_group_imports,
    slider_imports,
    static_img_imports,
    toggle_group_imports,
    toggle_imports,
)
from cli.templates.ui.logic import calendar_logic, collapsible_logic, pagination_logic


# Components made up of other Zentra models using a 'content' or 'items' attribute
PARENT_COMPONENTS = [
    "ScrollArea",
    "Tooltip",
]

# Dictionary of components with containers around them
# (classname, attributes)
COMPONENTS_TO_WRAP = {
    "Checkbox": 'className="flex items-top space-x-2"',
}


# Components that have a "use client" import at the top of their file
USE_CLIENT_COMPONENTS = [
    "Calendar",
    "Checkbox",
    "Collapsible",
    "Image",
]

# Components that have "useState"
USE_STATE_COMPONENTS = [
    "Calendar",
    "Collapsible",
]


COMPONENT_ATTR_MAPPING = {
    "Calendar": lambda comp: calendar_attributes(comp),
    "Collapsible": lambda comp: collapsible_attributes(comp),
    "InputOTP": lambda comp: input_otp_attributes(comp),
    "Link": lambda comp: nextjs_link_attributes(comp),
    "Slider": lambda comp: slider_attributes(comp),
    "Toggle": lambda comp: toggle_attributes(comp),
}


COMMON_ATTR_MAPPING = {
    "id": lambda value: str_attr("id", value),
    "url": lambda _: "asChild",
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
    "target": lambda value: str_attr("target", value),
    "styles": lambda value: str_attr("className", value),
    "src": lambda value: src_attribute(value),
    "alt": lambda alt: alt_attribute(alt),
    "width": lambda width: param_attr("width", width),
    "height": lambda height: param_attr("height", height),
    "checked": lambda checked: param_attr("checked", checked),
    "pressed": lambda pressed: param_attr("pressed", pressed),
    "color": lambda value: str_attr("color", value),
    "stroke_width": lambda value: param_attr("strokeWidth", value),
    "min": lambda value: param_attr("min", value),
    "max": lambda value: param_attr("max", value),
    "step": lambda value: param_attr("step", value),
    "orientation": lambda value: str_attr("orientation", value),
    "default_value": lambda value: str_attr("defaultValue", value),
}


EXTRA_IMPORTS_MAPPING = {
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
}


COMPONENT_CONTENT_MAPPING = {
    "Checkbox": lambda cb: checkbox_content(cb),
    "Collapsible": lambda comp: collapsible_content(comp),
    "RadioGroup": lambda rg: radio_group_content(rg),
    "Select": lambda select: select_content(select),
    "Alert": lambda alert: alert_content(alert),
    "TextAlertDialog": lambda ad: text_alert_dialog_content(ad),
    "Avatar": lambda avatar: avatar_content(avatar),
    "InputOTP": lambda otp: input_otp_content(otp),
    "Button": lambda btn: button_content(btn),
    "Toggle": lambda comp: toggle_content(comp),
    "ToggleGroup": lambda comp: toggle_group_content(comp),
    "Pagination": lambda comp: pagination_content(comp),
    # Parent components
    "ScrollArea": lambda sa: scroll_area_content(sa),
    "Tooltip": lambda tt: tooltip_content(tt),
}


COMMON_CONTENT_MAPPING = {
    "text": lambda value: text_content(value),
}


LOGIC_MAPPING = {
    "Calendar": lambda comp: calendar_logic(comp),
    "Collapsible": lambda comp: collapsible_logic(comp),
    "Pagination": lambda comp: pagination_logic(comp),
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
    "use_state_map": USE_STATE_COMPONENTS,
    "parent_components": PARENT_COMPONENTS,
}

ATTR_DICT = {
    "common": COMMON_ATTR_MAPPING,
    "model": COMPONENT_ATTR_MAPPING,
}

CONTENT_DICT = {
    "common": COMMON_CONTENT_MAPPING,
    "model": COMPONENT_CONTENT_MAPPING,
}

IMPORT_DICT = {
    "extra": EXTRA_IMPORTS_MAPPING,
    "use_state": USE_STATE_COMPONENTS,
}
