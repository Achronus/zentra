from tests.templates.dummy import DummyIconButton
from zentra.core.enums.ui import InputOTPPatterns
from zentra.ui.control import Button, IconButton


def collapsible_imports() -> list[str]:
    """Returns a list of strings for the Collapsible imports."""
    return [
        'import { Button } from "@/components/ui/button"',
        'import { ChevronsUpDown } from "lucide-react"',
    ]


def input_opt_imports(pattern: str) -> list[str]:
    """Returns a list of strings for the InputOTP imports based on a given pattern value."""
    if pattern in InputOTPPatterns:
        return ["import { " + InputOTPPatterns(pattern).name + ' } from "input-otp"']

    return None


def button_imports(btn: Button | IconButton | DummyIconButton) -> list[str]:
    """Returns a list of strings for the Button imports based on the components attributes."""
    imports = []

    if hasattr(btn, "url") and btn.url:
        imports.append('import Link from "next/link"')

    if hasattr(btn, "icon") and btn.icon:
        imports.append("import { " + btn.icon + ' } from "lucide-react"')

    return imports
