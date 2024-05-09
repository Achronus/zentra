from zentra.core.enums.ui import InputOTPPatterns
from zentra.core.react import LucideIcon, LucideIconWithText
from zentra.nextjs import Image, Link, StaticImage
from zentra.ui.control import Button, InputOTP
from zentra.ui.notification import Alert


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
