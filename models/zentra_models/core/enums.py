from enum import Enum


class LibraryType(str, Enum):
    SHADCNUI = "ui"
    UPLOADTHING = "uploadthing"
    NEXTJS = "nextjs"
    LUCIDE = "lucide"
    HTML = "html"
    JAVASCRIPT = "javascript"
    CUSTOM = "custom"
