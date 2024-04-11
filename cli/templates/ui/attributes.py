import re
from zentra.core.enums.ui import InputOTPPatterns


def calendar_attributes(name: str) -> list[str]:
    """Returns a list of strings for the Calendar attributes based on a given name value."""
    return [
        'mode="single"',
        f"selected={{{name}Date}}",
        f"onSelect={{{name}SetDate}}",
        'className="rounded-md border"',
    ]


def collapsible_attributes(name: str) -> list[str]:
    """Returns a list of strings for the Collapsible attributes based on a given name value."""
    return [
        f"open={{{name}IsOpen}}",
        f"onOpenChange={{{name}SetIsOpen}}",
        'className="w-[350px] space-y-2"',
    ]


def input_otp_attributes(pattern: str) -> list[str]:
    """Returns a list of strings for the InputOTP attributes based on a given pattern value."""
    return [
        f"pattern={{{InputOTPPatterns(pattern).name}}}"
        if pattern in InputOTPPatterns
        else f'pattern="{re.compile(pattern).pattern}"'
    ]
