from enum import Enum, IntEnum


class ButtonVariant(str, Enum):
    NONE = "none"
    PRIMARY = "primary"
    SECONDARY = "secondary"
    DESTRUCTIVE = "destructive"
    OUTLINE = "outline"
    GHOST = "ghost"
    LINK = "link"


class ButtonIconPosition(str, Enum):
    START = "start"
    END = "end"


class FormFieldLayout(IntEnum):
    SINGLE = 1
    DUO = 2
    TRIPLE = 3
