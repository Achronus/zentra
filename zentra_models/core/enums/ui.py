from enum import Enum, IntEnum


class LibraryType(str, Enum):
    SHADCNUI = "ui"
    UPLOADTHING = "uploadthing"
    NEXTJS = "nextjs"
    LUCIDE = "lucide"
    HTML = "html"
    JAVASCRIPT = "javascript"
    CUSTOM = "custom"


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


class InputOTPPatterns(str, Enum):
    REGEXP_ONLY_DIGITS = "digits_only"
    REGEXP_ONLY_CHARS = "chars_only"
    REGEXP_ONLY_DIGITS_AND_CHARS = "digits_n_chars_only"


class Orientation(str, Enum):
    VERTICAL = "vertical"
    HORIZONTAL = "horizontal"


class TextStyle(str, Enum):
    DEFAULT = "default"
    BOLD = "bold"
    OUTLINE = "outline"
    ITALIC = "italic"
    UNDERLINE = "underline"


class ToggleType(str, Enum):
    SINGLE = "single"
    MULTIPLE = "multiple"


class ToggleVariant(str, Enum):
    DEFAULT = "default"
    OUTLINE = "outline"


class ToggleSize(str, Enum):
    DEFAULT = "default"
    SM = "sm"
    LG = "lg"


class AlertVariant(str, Enum):
    DEFAULT = "default"
    DESTRUCTIVE = "destructive"


class BadgeVariant(str, Enum):
    DEFAULT = "default"
    SECONDARY = "secondary"
    DESTRUCTIVE = "destructive"
    OUTLINE = "outline"


class BCTriggerVariant(str, Enum):
    ELLIPSIS = "ellipsis"
    TEXT = "text"


class SkeletonPreset(str, Enum):
    CUSTOM = "custom"
    TESTIMONIAL = "testimonial"
    CARD = "card"


class CalendarMode(str, Enum):
    SINGLE = "single"
    MULTIPLE = "multiple"
    RANGE = "range"


class DDMenuType(str, Enum):
    DEFAULT = "default"
    RADIO = "radio"
    CHECKBOX = "checkbox"
