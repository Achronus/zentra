from zentra_models.core.enums import LibraryType


class HTML:
    """A library base for all HTML models."""

    @property
    def library(self) -> str:
        return LibraryType.HTML.value


class JavaScript:
    """A library base for all JavaScript models."""

    @property
    def library(self) -> str:
        return LibraryType.JAVASCRIPT.value


class CustomModel:
    """A library base for all custom component models."""

    @property
    def library(self) -> str:
        return LibraryType.CUSTOM.value


class Lucide:
    """A library base for all [Lucide React](https://lucide.dev/) components."""

    @property
    def library(self) -> str:
        return LibraryType.LUCIDE.value


class NextJs:
    """A library base for all [NextJS](https://nextjs.org/docs/app/api-reference/components) components."""

    @property
    def library(self) -> str:
        return LibraryType.NEXTJS.value


class ShadcnUi:
    """A library base for all [shadcn/ui](https://ui.shadcn.com/) components."""

    @property
    def library(self) -> str:
        return LibraryType.SHADCNUI.value
