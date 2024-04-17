from pydantic import BaseModel


class HTMLTag(BaseModel):
    """
    A parent model for all HTML tags.

    Parameters:
    - `styles` (`string, optional`) - the CSS styles to apply to the tag. Automatically adds them to `className`. `None` by default
    """

    styles: str = None


class JSIterable(BaseModel):
    """A parent model for all JavaScript iterables."""
