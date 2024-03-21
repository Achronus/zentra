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
