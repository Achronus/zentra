from enum import StrEnum


class ComponentFileType(StrEnum):
    BASE = "base"
    TEMPLATES = "templates"
    LIB = "lib"


class FileType(StrEnum):
    COMPONENT = "component"
    LAYOUT = "layout"
    PAGE = "page"
