import re

from zentra.core.enums.ui import InputOTPPatterns
from zentra.nextjs import Link, StaticImage, UrlQuery
from zentra.ui.control import Calendar, Collapsible, InputOTP, Slider, Toggle
from zentra.ui.presentation import Accordion


def str_attr(name: str, value: str) -> str:
    """A helper function for creating string attribute strings, such as `color="red"`."""
    return f'{name}="{value}"'


def param_attr(name: str, value: int | str | bool, backticks: bool = False) -> str:
    """A helper function for creating parameter attribute strings, such as `size={48}`, `checked={false}`, or ```alt={`I have a {param} here`}```."""
    if isinstance(value, bool):
        value = str(value).lower()
    elif isinstance(value, str) and value.startswith("$"):
        value = value[1:]

    if backticks:
        return f"{name}={{`{value}`}}"

    return f"{name}={{{value}}}"


def query_attr(values: dict[str, str | dict[str, str]]) -> str:
    """A helper function for creating query attribute strings, such as:
    ```jsx
    {
        pathname: "/dashboard",
        query: {
            name: "test", second: "test2"
        },
    }
    ```
    Returned as a compressed string like so:
    `{ pathname: "/dashboard", query: { name: "test", second: "test2" }, }`.

    Values are wrapped in `{ }` automatically.

    Example usage:
    ```python
    query_attr(values=)
    ```
    """

    def query_items(values: dict[str, str]) -> list[str]:
        query_list = ["{", "}"]
        for name, vals in values.items():
            query_list.insert(-1, f'{name}: "{vals}",')
        return query_list

    query_list = []
    for name, vals in values.items():
        if isinstance(vals, str):
            query_list.append(f'{name}: "{vals}",')
        else:
            queries = " ".join(query_items(vals))
            query_list.append(f"{name}: {queries},")

    return " ".join(["{"] + query_list + ["}"])


def size_attribute(value: str | int, attr_name: str = "size") -> str:
    """Returns a string for the `size` attribute based on its given value."""
    if isinstance(value, str) and value != "default":
        return str_attr(attr_name, value)

    elif isinstance(value, int):
        return param_attr(attr_name, value)


def src_attribute(value: str | StaticImage, attr_name: str = "src") -> str:
    """Returns a string for the `src` attribute based on its given value."""
    if isinstance(value, str):
        if value.startswith("$"):
            return param_attr(attr_name, value[1:])
        else:
            return str_attr(attr_name, value)

    else:
        return param_attr(attr_name, value.name)


def alt_attribute(alt: str, attr_name: str = "alt") -> str:
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
        return param_attr(attr_name, " ".join(new_alt), backticks=True)

    return str_attr(attr_name, " ".join(new_alt))


def calendar_attributes(cal: Calendar) -> list[str]:
    """Returns a list of strings for the `Calendar` attributes based on a given name value."""
    return [
        str_attr("mode", "single"),
        param_attr("selected", f"{cal.name}Date"),
        param_attr("onSelect", f"{cal.name}SetDate"),
        str_attr("className", "rounded-md border"),
    ]


def collapsible_attributes(comp: Collapsible) -> list[str]:
    """Returns a list of strings for the `Collapsible` attributes based on a given name value."""
    return [
        param_attr("open", f"{comp.name}IsOpen"),
        param_attr("onOpenChange", f"{comp.name}SetIsOpen"),
        str_attr("className", "w-[350px] space-y-2"),
    ]


def input_otp_attributes(comp: InputOTP) -> list[str] | None:
    """Returns a list of strings for the `InputOTP` attributes based on a given pattern value."""
    if comp.pattern:
        return [
            param_attr("pattern", InputOTPPatterns(comp.pattern).name)
            if comp.pattern in InputOTPPatterns
            else str_attr("pattern", re.compile(comp.pattern).pattern)
        ]

    return None


def nextjs_link_attributes(link: Link) -> list[str]:
    """Returns a list of strings for the `Link` attributes based on its given values."""
    attributes = []

    if isinstance(link.href, UrlQuery) and not isinstance(link.href, str):
        queries = {
            "pathname": link.href.pathname,
            "query": link.href.query,
        }
        attributes.append(param_attr("href", query_attr(queries)))

    if link.replace:
        attributes.append("replace")

    if not link.scroll:
        attributes.append(param_attr("scroll", link.scroll))

    if link.prefetch is not None:
        attributes.append(param_attr("prefetch", link.prefetch))

    return attributes


def slider_attributes(slider: Slider) -> list[str]:
    """Returns a list of strings for the `Slider` attributes based on its given values."""
    return [
        param_attr("defaultValue", f"[{slider.value}]"),
        param_attr("className", f'cn("w-[{str(slider.bar_size)}%]", className)'),
    ]


def toggle_attributes(toggle: Toggle) -> list[str]:
    """Returns a list of strings for the `Toggle` attributes based on its given values."""
    return [
        str_attr(
            "aria-label",
            f'Toggle{f' {toggle.style}' if toggle.style != "default" else ''}',
        )
    ]


def accordion_attributes(acc: Accordion) -> list[str]:
    """Returns a list of strings for the `Accordion` attributes based on its given values."""
    attrs = []
    if acc.type == "single":
        attrs.append("collapsible")

    if acc.orientation != "vertical":
        attrs.append(str_attr("orientation", acc.orientation))

    return attrs
