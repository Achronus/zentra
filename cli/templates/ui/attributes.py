import re

from pydantic import HttpUrl
from zentra.core.enums.ui import InputOTPPatterns
from zentra.nextjs import Link, StaticImage, Url


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


def nextjs_link_attributes(link: Link) -> list[str]:
    """Returns a list of strings for the Link attributes based on its given values."""
    attributes = []

    if isinstance(link.href, Url):
        queries = ", ".join(
            [f'{key}: "{value}"' for key, value in link.href.query.items()]
        )
        print(queries)

        attributes.extend(
            [
                "href={{",
                f'pathname: "{link.href.pathname}",',
                "query: { " + queries + " },",
                "}}",
            ]
        )
    elif isinstance(link.href, str):
        attributes.append(f'href="{link.href}"')

    if link.replace:
        attributes.append("replace")

    if not link.scroll:
        attributes.append(f"scroll={{{str(link.scroll).lower()}}}")

    if link.prefetch is not None:
        attributes.append(f"prefetch={{{str(link.prefetch).lower()}}}")

    return attributes


def src_attribute(value: str | HttpUrl | StaticImage) -> str:
    """Returns a string for the `src` attribute based on its given value."""
    attr = "src="
    if isinstance(value, str):
        if value.startswith("http"):
            return f'{attr}"{value}"'
        elif value.startswith("$"):
            return f"{attr}{{{value[1:]}}}"

    else:
        return f"{attr}{{{value.name}}}"


def alt_attribute(alt: str) -> str:
    """Returns a string for the `alt` attribute based on its given value."""
    values = alt.split(" ")
    param_str = False

    new_alt = []
    for word in values:
        if word and word.startswith("$"):
            word = "{" + word[1:] + "}"
            param_str = True
        new_alt.append(word)

    if param_str:
        return "alt=" + "{`" + " ".join(new_alt) + "`}"

    return f'alt="{" ".join(new_alt)}"'
