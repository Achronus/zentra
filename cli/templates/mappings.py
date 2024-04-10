import re
from typing import Callable

from pydantic import BaseModel
from tests.templates.dummy import DummyIconButton
from zentra.core.enums.ui import InputOTPPatterns
from zentra.ui.control import (
    Button,
    Calendar,
    Checkbox,
    Collapsible,
    IconButton,
    InputOTP,
    Label,
)


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
    (
        Calendar,
        "name",
        lambda value: [
            'mode="single"',
            f"selected={{{value}Date}}",
            f"onSelect={{{value}SetDate}}",
            'className="rounded-md border"',
        ],
    ),
    (
        Collapsible,
        "name",
        lambda value: [
            f"open={{{value}IsOpen}}",
            f"onOpenChange={{{value}SetIsOpen}}",
            'className="w-[350px] space-y-2"',
        ],
    ),
    (
        InputOTP,
        "pattern",
        lambda pattern: [
            f"pattern={{{InputOTPPatterns(pattern).name}}}"
            if pattern in InputOTPPatterns
            else f'pattern="{re.compile(pattern).pattern}"',
        ],
    ),
    (
        Label,
        "name",
        lambda value: [
            f'htmlFor="{value}"',
        ],
    ),
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
    (
        Collapsible,
        "name",
        lambda value: [
            'import { Button } from "@/components/ui/button"',
            'import { ChevronsUpDown } from "lucide-react"',
        ],
    ),
    (
        InputOTP,
        "pattern",
        lambda pattern: [
            "import { " + InputOTPPatterns(pattern).name + ' } from "input-otp"'
        ]
        if pattern in InputOTPPatterns
        else None,
    ),
    (
        Button,
        "url",
        lambda url: ['import Link from "next/link"'] if url else None,
    ),
    (
        IconButton,
        "icon",
        lambda icon: ["import { " + icon + ' } from "lucide-react"'],
    ),
    (
        IconButton,
        "url",
        lambda url: ['import Link from "next/link"'] if url else None,
    ),
    (
        DummyIconButton,
        "icon",
        lambda icon: ["import { " + icon + ' } from "lucide-react"'],
    ),
    (
        DummyIconButton,
        "url",
        lambda url: ['import Link from "next/link"'] if url else None,
    ),
]


COMPONENT_CONTENT_MAPPING = [
    (
        Checkbox,
        "label",
        lambda comp: [
            '<div className="grid gap-1.5 leading-none">',
            f'<label htmlFor="{comp.id}" className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">',
            f"{comp.label}",
            "</label>",
            *[
                f'<p className="text-sm text-muted-foreground">{comp.more_info}</p>',
                "</div>" if comp.more_info else "</div>",
            ],
        ],
    ),
    (
        Collapsible,
        "title",
        lambda comp: [
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
        ],
    ),
    (
        Collapsible,
        "items",
        lambda comp: [
            '<div className="rounded-md border px-4 py-3 font-mono text-sm">',
            comp.items[0],
            "</div>",
            '<CollapsibleContent className="space-y-2">',
            *[
                f'<div className="rounded-md border px-4 py-3 font-mono text-sm">\n{item}\n</div>'
                for item in comp.items[1:]
                if len(comp.items) > 1
            ],
            "</CollapsibleContent>",
        ],
    ),
    (
        Button,
        "text",
        lambda comp: [f'<Link href="{comp.url}">', comp.text, "</Link>"]
        if comp.url
        else [comp.text],
    ),
]


COMMON_CONTENT_MAPPING = [
    ("text", lambda value: value),
]


COMMON_LOGIC_MAPPING = [
    (
        Calendar,
        "name",
        lambda name: [
            f"const [{name}Date, {name}SetDate] = useState<Date | undefined>(new Date());"
        ],
    ),
    (
        Collapsible,
        "name",
        lambda name: [f"const [{name}IsOpen, {name}SetIsOpen] = useState(false);"],
    ),
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
