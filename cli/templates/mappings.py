from typing import Callable

from cli.templates.ui.attributes import (
    calendar_attributes,
    collapsible_attributes,
    input_otp_attributes,
)
from cli.templates.ui.content import (
    button_content,
    checkbox_content,
    collapsible_content,
    radio_group_content,
)
from cli.templates.ui.imports import (
    button_imports,
    collapsible_imports,
    input_opt_imports,
    radio_group_imports,
)
from cli.templates.ui.logic import calendar_logic, collapsible_logic
from tests.templates.dummy import DummyIconButton
from zentra.ui.control import (
    Button,
    Calendar,
    Checkbox,
    Collapsible,
    IconButton,
    InputOTP,
    Label,
    RadioGroup,
)

from pydantic import BaseModel


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
]

# (attribute_name, lambda_expression)
COMMON_ATTR_MAPPING = [
    ("id", lambda value: f'id="{value}"'),
    ("url", lambda value: "asChild" if value else None),
    ("type", lambda value: f'type="{value}"'),
    ("placeholder", lambda value: f'placeholder="{value}"'),
    ("variant", lambda value: f'variant="{value}"' if value != "default" else None),
    ("size", lambda value: f'size="{value}"' if value != "default" else None),
    ("disabled", lambda value: "disabled" if value else None),
    ("apiEndpoint", lambda value: f'apiEndpoint="{value}"'),
    ("num_inputs", lambda value: f"maxLength={{{value}}}"),
]


ADDITIONAL_IMPORTS_MAPPING = [
    (Collapsible, "name", lambda _: collapsible_imports()),
    (InputOTP, "pattern", lambda pattern: input_opt_imports(pattern)),
    (Button, "all", lambda btn: button_imports(btn)),
    (IconButton, "all", lambda btn: button_imports(btn)),
    (DummyIconButton, "all", lambda btn: button_imports(btn)),
    (RadioGroup, "default_value", lambda _: radio_group_imports()),
]


COMPONENT_CONTENT_MAPPING = [
    (Checkbox, lambda cb: checkbox_content(cb)),
    (Collapsible, lambda comp: collapsible_content(comp)),
    (Button, lambda btn: button_content(btn)),
    (RadioGroup, lambda rg: radio_group_content(rg)),
]


COMMON_CONTENT_MAPPING = [
    ("text", lambda value: value),
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


JSX_MAPPINGS = JSXMappings(
    common_attrs=COMMON_ATTR_MAPPING,
    component_attrs=COMPONENT_ATTR_MAPPING,
    common_content=COMMON_CONTENT_MAPPING,
    component_content=COMPONENT_CONTENT_MAPPING,
    common_logic=COMMON_LOGIC_MAPPING,
    use_client_map=USE_CLIENT_COMPONENTS,
    use_state_map=USE_STATE_COMPONENTS,
    additional_imports=ADDITIONAL_IMPORTS_MAPPING,
    wrappers=COMPONENTS_TO_WRAP,
)
