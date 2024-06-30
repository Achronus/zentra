from enum import Enum


class ComponentFileType(str, Enum):
    BASE = "base"
    TEMPLATES = "templates"
    LIB = "lib"
