from zentra.core import Component
from zentra.core.enums.ui import LibraryType


class Uploadthing:
    """A Zentra model for all [uploadthing](https://uploadthing.com/) components."""

    @property
    def library(self) -> str:
        return LibraryType.UPLOADTHING.value


class FileUpload(Component, Uploadthing):
    """A Zentra model for the [uploadthing](https://uploadthing.com/) FileUpload fields.

    Parameters:
    - `apiEndpoint` (`str, optional`) - the API endpoint to use. Defaults to `media`. API endpoints are stored in `frontend/src/lib/core.ts -> uploadFileRouter`. We advise you leave this as `media` until you update your `frontend` files later. You can find more information about this in the [uploadthing docs](https://docs.uploadthing.com/getting-started/appdir#set-up-a-filerouter)
    """

    apiEndpoint: str = "media"
