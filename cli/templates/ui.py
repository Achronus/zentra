import re
from pydantic import HttpUrl

from zentra.core import Component, Icon
from zentra.core.enums.ui import (
    ButtonIconPosition,
    ButtonSize,
    ButtonVariant,
    IconButtonSize,
    InputOTPPatterns,
)


class JSXContainer:
    """A base JSX storage container for Zentra models."""

    @classmethod
    def attributes(cls) -> str:
        """Generates a string of JSX containing the attributes of the component's root."""
        return None

    @classmethod
    def unique_logic(cls) -> str:
        """Generates a string of JSX for the unique logic of the component."""
        return None

    @classmethod
    def main_content(cls) -> str:
        """Generates a string of JSX with the main content of the component."""
        return None

    @classmethod
    def extra_parts(cls) -> str:
        """Generates a string used inside the 'core' import string, defining the name of the sub-component pieces needed for the full component."""
        return None

    @classmethod
    def imports(cls, core: str) -> str:
        """Generates a string of JSX with imports required by the component."""
        return core


class ButtonJSX(JSXContainer):
    """A JSX storage container for the Zentra Button model."""

    @classmethod
    def attributes(
        cls, url: HttpUrl, variant: ButtonVariant, size: ButtonSize, disabled: bool
    ) -> str:
        attr_map = [
            (disabled, "disabled"),
            (url, f'href="{url}"'),
            (variant != ButtonVariant.DEFAULT, f'variant="{variant}"'),
            (size != ButtonSize.DEFAULT, f'size="{size}"'),
        ]
        return Component.map_to_str(attr_map)

    @classmethod
    def main_content(cls, text: str) -> str:
        return text


class IconButtonJSX(JSXContainer):
    """A JSX storage container for the Zentra IconButton model."""

    @classmethod
    def attributes(
        cls, url: HttpUrl, variant: ButtonVariant, size: IconButtonSize, disabled: bool
    ) -> str:
        """Generates a string of JSX containing the attributes of the component's root."""
        attr_map = [
            (disabled, "disabled"),
            (url, f'href="{url}"'),
            (variant != ButtonVariant.DEFAULT, f'variant="{variant}"'),
            (size != IconButtonSize.DEFAULT, f'size="{size}"'),
        ]
        return Component.map_to_str(attr_map)

    @classmethod
    def main_content(
        cls, text: str, icon: Icon, icon_position: ButtonIconPosition
    ) -> str:
        """Generates a string of JSX with the main content of the component."""
        contents = []

        if text:
            contents.append(text)

        if icon:
            icon_html = f'<{icon.name} className="mr-2 h-4 w-4"/>'
            if icon_position == "start":
                contents.insert(0, icon_html)
            else:
                contents.append(icon_html)

        return " ".join(contents)


class CalendarJSX(JSXContainer):
    """A JSX storage container for the Zentra Calendar model."""

    @classmethod
    def state_names(cls, id: str) -> tuple[str, str]:
        """A helper function for assigning the `get` and `set` names for the `useState()` hook."""
        return (
            f"{id}Date",
            f"{id}SetDate",
        )

    @classmethod
    def unique_logic(cls, id: str) -> str:
        get_name, set_name = cls.state_names(id)
        return f"const [{get_name}, {set_name}] = useState(new Date());"

    @classmethod
    def attributes(cls, id: str) -> str:
        get_name, set_name = cls.state_names(id)
        return f'mode="single" selected={{{get_name}}} onSelect={{{set_name}}} className="rounded-md border"'


class CheckboxJSX(JSXContainer):
    """A JSX storage container for the Zentra Checkbox model."""

    @classmethod
    def attributes(cls, id: str, disabled: bool) -> str:
        return f'id="{id}"{" disabled" if disabled else ""}'

    @classmethod
    def main_content(cls, id: str, label: str) -> str:
        return f'<div className="grid gap-1.5 leading-none"><label htmlFor="{id}" className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">{label}</label>'

    @classmethod
    def more_info(cls, info: str) -> str:
        """Generates a string of JSX for the `more_info` optional argument."""
        return f'<p className="text-sm text-muted-foreground">{info}</p>'


class CollapsibleJSX(JSXContainer):
    """A JSX storage container for the Zentra Collapsible model."""

    @classmethod
    def state_names(cls, id: str) -> tuple[str, str]:
        """A helper function for assigning the `get` and `set` names for the `useState()` hook."""
        return (
            f"{id}IsOpen",
            f"{id}SetIsOpen",
        )

    @classmethod
    def unique_logic(cls, id: str) -> str:
        get_name, set_name = cls.state_names(id)
        return f"const [{get_name}, {set_name}] = useState(false);"

    @classmethod
    def attributes(cls, id: str) -> str:
        get_name, set_name = cls.state_names(id)
        return f'open={{{get_name}}} onOpenChange={{{set_name}}} className="w-[350px] space-y-2"'

    @classmethod
    def title(cls, title: str) -> str:
        """Generates a string of JSX for the `title` attribute of the component."""
        return f'<div className="flex items-center justify-between space-x-4 px-4"><h4 className="text-sm font-semibold">{title}</h4><CollapsibleTrigger asChild><Button variant="ghost" size="sm" className="w-9 p-0"><ChevronsUpDown className="h-4 w-4" /><span className="sr-only">Toggle</span></Button></CollapsibleTrigger></div>'

    @classmethod
    def items(cls, items: list[str]) -> str:
        """Generates a string of JSX for the `items` attribute of the component."""
        items_str = f'<div className="rounded-md border px-4 py-3 font-mono text-sm">{items[0]}</div><CollapsibleContent className="space-y-2">'

        if len(items) > 1:
            for item in items:
                items_str += f'<div className="rounded-md border px-4 py-3 font-mono text-sm">{item}</div>'

        items_str += "</CollapsibleContent>"
        return items_str

    @classmethod
    def extra_parts(cls) -> str:
        return ", CollapsibleContent, CollapsibleTrigger "

    @classmethod
    def imports(cls, core: str) -> str:
        additional = 'import { Button } from "../ui/button"\nimport { ChevronsUpDown } from "lucide-react"'
        return core + additional


class InputJSX(JSXContainer):
    """A JSX storage container for the Zentra Input model."""

    @classmethod
    def attributes(cls, id: str, type: str, placeholder: str, disabled: bool) -> str:
        """Generates a string of JSX containing the attributes of the component's root."""
        return f'id="{id}" type="{type}" placeholder="{placeholder}"{' disabled' if disabled else ''}'


class InputOTPJSX(JSXContainer):
    """A JSX storage container for the Zentra InputOTP model."""

    @classmethod
    def get_pattern_key(cls, pattern: str) -> str:
        """A helper function for retrieving a patterns key name."""
        for key, value in InputOTPPatterns.__members__.items():
            if value == pattern:
                return key

    @classmethod
    def assign_pattern(cls, pattern: str) -> str | None:
        """A helper function for assigning the correct pattern value."""
        if pattern in InputOTPPatterns:
            return f"pattern={{{cls.get_pattern_key(pattern)}}}"
        elif pattern:
            return f'pattern="{re.compile(pattern).pattern}"'

        return None

    @classmethod
    def attributes(cls, num_inputs: int, pattern: str) -> str:
        p_val = cls.assign_pattern(pattern)
        return f'maxLength={{{num_inputs}}}{f' {p_val}' if pattern else ''}'

    @classmethod
    def main_content(cls, num_inputs: int, num_groups: int) -> str:
        content = ""
        slot_group_size = num_inputs // num_groups
        slot_idx = 0

        for g_idx in range(num_groups):
            content += "<InputOTPGroup>"
            for _ in range(slot_group_size):
                content += f"<InputOTPSlot index={{{slot_idx}}} />"
                slot_idx += 1
            content += "</InputOTPGroup>"

            if num_groups > 1 and g_idx + 1 != num_groups:
                content += "<InputOTPSeparator />"

        return content

    @classmethod
    def extra_parts(cls, num_groups: int) -> str:
        if num_groups > 1:
            return ", InputOTPGroup, InputOTPSeparator, InputOTPSlot "

        return ", InputOTPGroup, InputOTPSlot "

    @classmethod
    def imports(cls, core: str, pattern: str) -> str:
        if pattern in InputOTPPatterns:
            p_val = cls.get_pattern_key(pattern)
            additional = f'import { {p_val} } from "input-otp"'.replace("'", " ")
            return core + additional
        return core


class LabelJSX(JSXContainer):
    """A JSX storage container for the Zentra Label model."""

    @classmethod
    def attributes(cls, id: str) -> str:
        return f'htmlForm="{id}"'

    @classmethod
    def main_content(cls, text: str) -> str:
        return text
