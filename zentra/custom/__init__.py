from zentra.core.enums.ui import LibraryType


class CustomModel:
    """A Zentra model for all custom component models."""

    @property
    def library(self) -> str:
        return LibraryType.CUSTOM.value
