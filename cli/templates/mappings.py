from typing import Callable

from pydantic_core import Url

from cli.templates.ui.attributes import (
    alt_attribute,
    calendar_attributes,
    collapsible_attributes,
    input_otp_attributes,
    nextjs_link_attributes,
    slider_attributes,
    src_attribute,
    toggle_attributes,
)
from cli.templates.ui.content import (
    checkbox_content,
    collapsible_content,
    div_content,
    radio_group_content,
    scroll_area_content,
    select_content,
    text_content,
)
from cli.templates.ui.imports import (
    collapsible_imports,
    image_imports,
    input_opt_imports,
    radio_group_imports,
    slider_imports,
    static_img_imports,
)
from cli.templates.ui.logic import calendar_logic, collapsible_logic
from zentra.core.html import Div
from zentra.nextjs import Image, Link, StaticImage
from zentra.ui.control import (
    Calendar,
    Checkbox,
    Collapsible,
    InputOTP,
    Label,
    RadioGroup,
    ScrollArea,
    Select,
    Slider,
    Toggle,
)
from zentra.ui.presentation import Separator

from pydantic import BaseModel


# Components made up of other Zentra models using a 'content' attribute
PARENT_COMPONENTS = [
    "Button",
    "ScrollArea",
    "Toggle",
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

# (component_type, attribute_name, lambda_expression)
COMPONENT_ATTR_MAPPING = [
    (Calendar, "name", lambda name: calendar_attributes(name)),
    (Collapsible, "name", lambda name: collapsible_attributes(name)),
    (InputOTP, "pattern", lambda pattern: input_otp_attributes(pattern)),
    (Label, "name", lambda name: [f'htmlFor="{name}"']),
    (RadioGroup, "default_value", lambda dv: [f'defaultValue="{dv}"']),
    (Separator, "orientation", lambda val: [f'orientation="{val}"']),
    (Link, "all", lambda comp: nextjs_link_attributes(comp)),
    (Slider, "all", lambda slider: slider_attributes(slider)),
    (Toggle, "all", lambda toggle: toggle_attributes(toggle)),
]

# (attribute_name, lambda_expression)
COMMON_ATTR_MAPPING = [
    ("id", lambda value: f'id="{value}"'),
    ("url", lambda value: "asChild" if value else None),
    (
        "href",
        lambda value: f'href="{value}"' if isinstance(value, (str, Url)) else None,
    ),
    ("type", lambda value: f'type="{value}"'),
    ("placeholder", lambda value: f'placeholder="{value}"'),
    ("variant", lambda value: f'variant="{value}"' if value != "default" else None),
    ("size", lambda value: f'size="{value}"' if value != "default" else None),
    ("disabled", lambda value: "disabled" if value else None),
    ("apiEndpoint", lambda value: f'apiEndpoint="{value}"'),
    ("num_inputs", lambda value: f"maxLength={{{value}}}"),
    ("key", lambda key: f"key={{{key[1:]}}}" if key else None),
    ("target", lambda value: f'target="{value}"' if value else None),
    ("styles", lambda value: f'className="{value}"' if value else None),
    ("src", lambda value: src_attribute(value) if value else None),
    ("alt", lambda alt: alt_attribute(alt) if alt else None),
    ("width", lambda width: f"width={{{width}}}" if width else None),
    ("height", lambda height: f"height={{{height}}}" if height else None),
    ("checked", lambda checked: f"checked={{{str(checked).lower()}}}"),
    ("pressed", lambda pressed: f"pressed={{{str(pressed).lower()}}}"),
]


ADDITIONAL_IMPORTS_MAPPING = [
    (Collapsible, "name", lambda _: collapsible_imports()),
    (InputOTP, "pattern", lambda pattern: input_opt_imports(pattern)),
    (RadioGroup, "default_value", lambda _: radio_group_imports()),
    (StaticImage, "all", lambda img: static_img_imports(img)),
    (Image, "src", lambda src: image_imports(src)),
    (Slider, "value", lambda _: slider_imports()),
]


COMPONENT_CONTENT_MAPPING = [
    (Div, lambda div: div_content(div)),
    (Checkbox, lambda cb: checkbox_content(cb)),
    (Collapsible, lambda comp: collapsible_content(comp)),
    (RadioGroup, lambda rg: radio_group_content(rg)),
    (ScrollArea, lambda sa: scroll_area_content(sa)),
    (Select, lambda select: select_content(select)),
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

    common_attrs: list[tuple[str, Callable]]
    component_attrs: list[tuple]
    common_content: list[tuple]
    component_content: list[tuple]
    common_logic: list[tuple]
    use_client_map: list[str]
    use_state_map: list[str]
    additional_imports: list[tuple]
    wrappers: dict[str, str]


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
}

JSX_MAPPINGS = JSXMappings(**MAPPING_DICT)
