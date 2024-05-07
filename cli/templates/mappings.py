from typing import Callable
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
    checkbox_content,
    collapsible_content,
    div_content,
    radio_group_content,
    scroll_area_content,
    select_content,
    text_alert_dialog_content,
    text_content,
    tooltip_content,
)
from cli.templates.ui.imports import (
    alert_imports,
    collapsible_imports,
    image_imports,
    input_opt_imports,
    radio_group_imports,
    slider_imports,
    static_img_imports,
)
from cli.templates.ui.logic import calendar_logic, collapsible_logic
from zentra.core.html import Div
from zentra.nextjs import Image, StaticImage
from zentra.ui.control import (
    Calendar,
    Checkbox,
    Collapsible,
    InputOTP,
    RadioGroup,
    ScrollArea,
    Select,
    Slider,
)
from zentra.ui.notification import Alert, TextAlertDialog, Tooltip
from zentra.ui.presentation import Avatar

from pydantic import BaseModel


# Components made up of other Zentra models using a 'content' or 'items' attribute
PARENT_COMPONENTS = [
    "Button",
    "ScrollArea",
    "Toggle",
    "ToggleGroup",
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


ADDITIONAL_IMPORTS_MAPPING = [
    (Collapsible, "name", lambda _: collapsible_imports()),
    (InputOTP, "pattern", lambda pattern: input_opt_imports(pattern)),
    (RadioGroup, "default_value", lambda _: radio_group_imports()),
    (StaticImage, "all", lambda img: static_img_imports(img)),
    (Image | Avatar, "src", lambda src: image_imports(src)),
    (Slider, "value", lambda _: slider_imports()),
    (Alert, "icon", lambda icon: alert_imports(icon)),
]


COMPONENT_CONTENT_MAPPING = [
    (Div, lambda div: div_content(div)),
    (Checkbox, lambda cb: checkbox_content(cb)),
    (Collapsible, lambda comp: collapsible_content(comp)),
    (RadioGroup, lambda rg: radio_group_content(rg)),
    (ScrollArea, lambda sa: scroll_area_content(sa)),
    (Select, lambda select: select_content(select)),
    (Alert, lambda alert: alert_content(alert)),
    (TextAlertDialog, lambda ad: text_alert_dialog_content(ad)),
    (Tooltip, lambda tt: tooltip_content(tt)),
    (Avatar, lambda avatar: avatar_content(avatar)),
]


COMMON_CONTENT_MAPPING = [
    ("text", lambda value: text_content(value)),
]


COMMON_LOGIC_MAPPING = [
    (Calendar, "name", lambda name: calendar_logic(name)),
    (Collapsible, "name", lambda name: collapsible_logic(name)),
]


class JSXMappings(BaseModel):
    """A storage container for JSX mappings."""

    common_attrs: dict[str, Callable]
    component_attrs: dict[str, Callable]
    common_content: list[tuple]
    component_content: list[tuple]
    common_logic: list[tuple]
    use_client_map: list[str]
    use_state_map: list[str]
    additional_imports: list[tuple]
    wrappers: dict[str, str]
    parent_components: list[str]


MAPPING_DICT = {
    "common_attrs": COMMON_ATTR_MAPPING,
    "component_attrs": COMPONENT_ATTR_MAPPING,
    "common_content": COMMON_CONTENT_MAPPING,
    "component_content": COMPONENT_CONTENT_MAPPING,
    "common_logic": COMMON_LOGIC_MAPPING,
    "use_client_map": USE_CLIENT_COMPONENTS,
    "use_state_map": USE_STATE_COMPONENTS,
    "additional_imports": ADDITIONAL_IMPORTS_MAPPING,
    "wrappers": COMPONENTS_TO_WRAP,
    "parent_components": PARENT_COMPONENTS,
}

JSX_MAPPINGS = JSXMappings(**MAPPING_DICT)
