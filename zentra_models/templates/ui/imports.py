from zentra_models.templates.utils import compress_imports

from zentra_models.core.enums.ui import CalendarMode, InputOTPPatterns
from zentra_models.core.react import LucideIcon, LucideIconWithText
from zentra_models.nextjs import Image, Link, StaticImage
from zentra_models.ui.control import (
    Button,
    Calendar,
    InputOTP,
    Toggle,
    ToggleGroup,
)
from zentra_models.ui.notification import Alert


def calendar_imports(cal: Calendar) -> list[str]:
    """Returns a list of strings for the additional `Calendar` imports."""

    if cal.mode == CalendarMode.RANGE.value:
        return [
            'import { addDays } from "date-fns"',
            'import { DateRange } from "react-day-picker"',
        ]

    return []


def collapsible_imports() -> list[str]:
    """Returns a list of strings for the additional `Collapsible` imports."""
    return [
        'import { Button } from "@/components/ui/button"',
        'import { ChevronsUpDown } from "lucide-react"',
    ]


def input_opt_imports(comp: InputOTP) -> list[str] | None:
    """Returns a list of strings for the additional `InputOTP` imports based on a given pattern value."""
    if comp.pattern in InputOTPPatterns:
        return [
            "import { " + InputOTPPatterns(comp.pattern).name + ' } from "input-otp"'
        ]

    return None


def radio_group_imports() -> list[str]:
    """Returns a list of strings for the additional `RadioGroup` imports."""
    return ['import { Label } from "@/components/ui/label"']


def static_img_imports(img: StaticImage) -> list[str]:
    """Returns a list of strings for the additional `StaticImage` imports based on its attributes."""
    return [f"import {img.name} from '{img.path}'"]


def image_imports(img: Image) -> list[str] | None:
    """Returns a list of strings for the additional `Image` imports based on its attributes."""
    if isinstance(img.src, StaticImage):
        return static_img_imports(img.src)

    return None


def slider_imports() -> list[str]:
    """Returns a list of strings for the additional `Slider` imports."""
    return ['import { cn } from "@/lib/utils"']


def alert_imports(alert: Alert) -> list[str] | None:
    """Returns a list of strings for the additional `Alert` imports based on its attributes."""
    if alert.icon:
        return [LucideIcon(name=alert.icon).import_str]

    return None


def button_imports(btn: Button) -> list[str]:
    """Returns a list of strings for the additional `Button` imports based on its attributes."""
    imports = []
    if btn.url:
        imports.append(Link(href=btn.url).import_str)

    if isinstance(btn.content, LucideIconWithText):
        imports.append(btn.content.import_str)

    return imports


def toggle_imports(toggle: Toggle) -> list[str]:
    """Returns a list of strings for the additional `Toggle` imports based on its attributes."""
    if isinstance(toggle.content, LucideIcon):
        return [toggle.content.import_str]

    return []


def toggle_group_imports(tg: ToggleGroup) -> list[str]:
    """Returns a list of strings for the additional `ToggleGroup` imports based on its attributes."""
    imports = []

    for item in tg.items:
        imports.extend(toggle_imports(item))

    return compress_imports(imports)


def date_picker_imports() -> list[str]:
    """Returns a list of strings for the additional `DatePicker` imports."""
    return [
        'import { format } from "date-fns"',
        'import { cn } from "@/lib/utils"',
    ]
