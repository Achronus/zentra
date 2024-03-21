from enum import Enum, IntEnum


class ButtonVariant(str, Enum):
    none = "none"
    primary = "primary"
    secondary = "secondary"
    destructive = "destructive"
    outline = "outline"
    ghost = "ghost"
    link = "link"


class ButtonIconPosition(str, Enum):
    start = "start"
    end = "end"


class FormFieldLayout(IntEnum):
    single = 1
    duo = 2
    triple = 3
