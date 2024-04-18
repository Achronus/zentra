import re
from zentra.core.enums.ui import InputOTPPatterns
from zentra.nextjs import StaticImage


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


def src_attribute(value: str | StaticImage) -> str:
    """Returns a string for the `src` attribute based on its given value."""
    attr = "src="
    if isinstance(value, str):
        if value[0] == "$":
            return f"{attr}{{{value[1:]}}}"

        return f'{attr}"{value}"'
    else:
        return f"{attr}{{{value.name}}}"


def alt_attribute(alt: str) -> str:
    """Returns a string for the `alt` attribute based on its given value."""
    values = alt.split(" ")
    param_str = False

    new_alt = []
    for word in values:
        if word and word[0] == "$":
            word = "{" + word[1:] + "}"
            param_str = True
        new_alt.append(word)

    if param_str:
        return "alt=" + "{`" + " ".join(new_alt) + "`}"

    return f'alt="{" ".join(new_alt)}"'
