from zentra.core import Component
from zentra.core.base import JSIterable
from zentra.core.html import Div, HTMLContent
from zentra.ui.control import (
    Button,
    Checkbox,
    Collapsible,
    RadioButton,
    RadioGroup,
    ScrollArea,
)


def param_reformat_helper(text: str) -> list[str]:
    """A helper function to reformat a string of text with parameter values. Returns the new version as a list of strings."""
    new_text = []
    for word in text.split(" "):
        if word:
            if word.startswith("$"):
                new_text.append(f"{{{word[1:]}}}")
            else:
                new_text.append(word)

    return [" ".join(new_text)]


def div_content(div: Div) -> Component | JSIterable | list:
    """Returns the required format for Div content based on the components attributes. For example, if `div.items` is a string, it converts it to a list and reformats its `parameter` values if required. If no formatting is required, will return the `Component` model, `JSIterable` model, or `list` of items provided."""
    if isinstance(div.items, str):
        return param_reformat_helper(div.items)

    return div.items


def checkbox_content(cb: Checkbox) -> list[str]:
    """Returns a list of strings for the Checkbox content based on the components attributes."""
    content = [
        '<div className="grid gap-1.5 leading-none">',
        f'<label htmlFor="{cb.id}" className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">',
        f"{cb.label}",
        "</label>",
    ]

    if cb.more_info:
        content.extend(
            ['<p className="text-sm text-muted-foreground">', cb.more_info, "</p>"]
        )

    content.append("</div>")
    return content


def collapsible_content(comp: Collapsible) -> list[str]:
    """Returns a list of strings for the Collapsible content based on the components attributes."""
    content = [
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
        '<div className="rounded-md border px-4 py-3 font-mono text-sm">',
        comp.items[0],
        "</div>",
        '<CollapsibleContent className="space-y-2">',
    ]

    if len(comp.items) > 1:
        for item in comp.items[1:]:
            content.extend(
                [
                    '<div className="rounded-md border px-4 py-3 font-mono text-sm">',
                    item,
                    "</div>",
                ]
            )

    content.append("</CollapsibleContent>")
    return content


def button_content(btn: Button) -> list[str]:
    """Returns a list of strings for the Button content based on the components attributes."""
    if btn.url:
        return [f'<Link href="{btn.url}">', btn.text, "</Link>"]

    return [btn.text]


def radio_button_content(rb: RadioButton) -> list[str]:
    """Returns a list of strings for the RadioButton content based on the components attributes."""
    return [
        '<div className="flex items-center space-x-2">',
        f'<RadioGroupItem value="{rb.value}" id="{rb.id}" />',
        f'<Label htmlFor="{rb.id}">',
        rb.text,
        "</Label>",
        "</div>",
    ]


def radio_group_content(rg: RadioGroup) -> list[str]:
    """Returns a list of strings for the RadioGroup content based on the components attributes."""
    content = []
    for rb in rg.items:
        content.extend(radio_button_content(rb))

    return content


def scroll_area_content(sa: ScrollArea) -> list[str]:
    """Returns a list of strings for the ScrollArea content based on the components attributes."""
    content = []
    if isinstance(sa.content, str):
        content.append(sa.content)

    content.append(f'<ScrollBar orientation="{sa.orientation}" />')
    return content


def text_content(
    text: str | HTMLContent | list[str | HTMLContent],
) -> list[str] | HTMLContent:
    """Returns a list of strings of text content with variable preprocessing (if required) or a HTMLContent model."""
    if isinstance(text, str):
        return param_reformat_helper(text)

    return text
