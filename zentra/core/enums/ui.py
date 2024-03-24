from enum import Enum, IntEnum


class ButtonVariant(str, Enum):
    DEFAULT = "default"
    SECONDARY = "secondary"
    DESTRUCTIVE = "destructive"
    OUTLINE = "outline"
    GHOST = "ghost"
    LINK = "link"


class ButtonSize(str, Enum):
    DEFAULT = "default"
    SM = "sm"
    LG = "lg"


class IconButtonSize(str, Enum):
    DEFAULT = "default"
    SM = "sm"
    LG = "lg"
    ICON = "icon"


class ButtonIconPosition(str, Enum):
    START = "start"
    END = "end"


class FormFieldLayout(IntEnum):
    DUO = 2
    TRIPLE = 3


class InputTypes(str, Enum):
    TEXT = "text"
    EMAIL = "email"
    PASSWORD = "password"
    NUMBER = "number"
    FILE = "file"
    TEL = "tel"
    SEARCH = "search"
    URL = "url"
    COLOR = "colour"
