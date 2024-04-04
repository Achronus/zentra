import re
from zentra.core.enums.ui import InputOTPPatterns
from zentra.ui.control import Calendar, Collapsible, InputOTP, Label


# Components that have a "use client" import at the top of their file
USE_CLIENT_COMPONENTS = [
    "Calendar",
    "Checkbox",
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
            f"open={{{value}SetIsOpen}}",
            'className="w-[350px] space-y-2"',
        ],
    ),
    (
        InputOTP,
        "pattern",
        lambda pattern: [
            f'pattern="{{{InputOTPPatterns(pattern).name}}}"'
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
    ("url", lambda value: f'href="{value}"' if value else None),
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
        [
            'import { Button } from "../ui/button"',
            'import { ChevronsUpDown } from "lucide-react"',
        ],
    )
]
