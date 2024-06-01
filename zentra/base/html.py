from typing import Optional

from zentra.base import ZentraBase
from zentra.base.library import HTML


class HTMLTag(ZentraBase, HTML):
    """
    A parent model for all HTML tags.

    Parameters:
    - `styles` (`string, optional`) - a set of custom CSS classes to apply to the tag. Automatically adds them to `className`. `None` by default
    """

    styles: Optional[str] = None

    @property
    def classname(self) -> str:
        """Stores the classname for the JSX builder."""
        return self.__class__.__name__.lower()
