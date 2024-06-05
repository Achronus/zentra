from typing import Optional, Union
from zentra.base import ZentraModel
from zentra.base.html import HTMLTag
from zentra.core.enums.html import HTMLContentTagType
from zentra.core.validation import key_attr_validation

from zentra.nextjs import Image

from pydantic import PrivateAttr, field_validator


class HTMLContent(HTMLTag):
    """
    A model dedicated to HTML content tags, including `headings`, `paragraphs`, and `span`.

    Parameters:
    - `tag` (`string`) - the type of tag to wrap around the `text` attribute. Valid options: `['h1', 'h2', 'h3', 'h4', 'h5', h6', 'p', 'span']`
    - `text` (`string`) - the text inside the tag. Can also include parameters, signified by a `$.` at the start of the parameter name. This is useful when using the `Image` inside an `iterable` function like `map`
    - `styles` (`string, optional`) - the CSS styles to apply to the tag. `None` by default
    """

    tag: HTMLContentTagType
    text: str

    _content_attr = PrivateAttr(default="text")

    @property
    def classname(self) -> str:
        return self.tag


class Div(HTMLTag):
    """
    A model dedicated to the `<div>` HTML tag.

    Parameters:
    - `content` (`string | ZentraModel | list[string | ZentraModel]`) - Can be either:
      1. A `string` of text. Can include parameter variables (indicated by starting the variable name with a `$.`) or be one specifically
      2. Any `zentra.core.Component` model, such as `zentra.ui.control.Label`
      3. Any `zentra.core.js.JSIterable` model, such as `zentra.core.js.Map`
      4. A `list` of a combination of `strings` of text, `zentra.core.html.HTMLTag` models, `zentra.core.js.JSIterable` models, or `zentra.core.Component` models
    - `fragment` (`boolean, optional`) - A flag to switch the div to a React fragment (`<>`, `</>`). Often used in JSX when a single parent container is needed. `False` by default
    - `key` (`string, optional`) - A unique identifier added to the container. Needed when using JS iterables like `map`. When provided, must be a parameter (start with a `$.`). `None` by default
    - `styles` (`string, optional`) - the CSS styles to apply to the tag. `None` by default
    """

    content: Union[str, ZentraModel, list[str | ZentraModel]]
    fragment: bool = False
    key: Optional[str] = None

    @field_validator("key")
    def validate_key(cls, key: str) -> str:
        return key_attr_validation(key)


class FigCaption(HTMLTag):
    """
    A model dedicated to the `<figcaption>` HTML tag used within the `<figure>` tag.

    Parameters:
    - `text` (`string | zentra.core.html.HTMLContent | list[string | zentra.core.html.HTMLContent]`) - the text to put into the caption. Can either be:
      1. A single or multi-line `string` of text without any tags wrapped around it. Can include parameter variables (indicated by starting the variable name with a `$.`)
      2. A `zentra.core.html.HTMLContent` object for wrapping the text in a `heading`, `paragraph`, or `span` tag
      3. A `list` of combined `string` and `zentra.core.html.HTMLContent` objects for more advanced captions
    - `styles` (`string, optional`) - the CSS styles to apply to the tag. `None` by default

    Example Usage:
    1. Advanced captioning.
    ```python
    from zentra.core.html import FigCaption, HTMLContent

    FigCaption(
        text=[
            'Photo by ',
            HTMLContent(
                tag="span",
                text="$.artwork.artist",
                styles="font-semibold text-foreground",
            ),
        ],
        styles="pt-2 text-xs text-muted-foreground",
    )
    ```
    JSX equivalent ->
    ```jsx
    <figcaption className="pt-2 text-xs text-muted-foreground">
        Photo by
        <span className="font-semibold text-foreground">
            {artwork.artist}
        </span>
    </figcaption>
    ```
    """

    text: Union[str, HTMLContent] | list[Union[str, HTMLContent]]

    _content_attr = PrivateAttr(default="text")


class Figure(HTMLTag):
    """
    A model dedicated to the `<figure>` HTML tag.

    Parameters:
    - `img` (`zentra.nextjs.Image`) - a NextJS `Image` component defining the image to display in the figure
    - `caption` (`zentra.core.html.FigCaption`) - a `FigCaption` component representing the caption of the Image
    - `styles` (`string, optional`) - the CSS styles to apply to the tag. `None` by default
    - `key` (`string, optional`) -A unique identifier added to the figure. Needed if using a JS iterable like `map`. When provided, must be a parameter (start with a `$.`). `None` by default

    Example usage:
    1. A detailed figure with variables.
    ```python
    from zentra.core.html import Figure, FigCaption, HTMLContent
    from zentra.nextjs import Image

    Figure(
        img=Image(
            src="$.artwork.art",
            alt="Photo by $.artwork.artist",
            width=300,
            height=400,
            styles="aspect-[3/4] h-fit w-fit object-cover",
        ),
        caption=FigCaption(
            text=[
                'Photo by ',
                HTMLContent(
                    tag="span",
                    text="$.artwork.artist",
                    styles="font-semibold text-foreground",
                )
            ],
            styles="pt-2 text-xs text-muted-foreground",
        ),
        key="$.artwork.art",
    )
    ```
    JSX equivalent ->
    ```jsx
    <figure key={artwork.artist} className="shrink-0">
        <div className="overflow-hidden rounded-md">
            <Image
            src={artwork.art}
            alt={`Photo by ${artwork.artist}`}
            className="aspect-[3/4] h-fit w-fit object-cover"
            width={300}
            height={400}
            />
        </div>
        <figcaption className="pt-2 text-xs text-muted-foreground">
            Photo by
            <span className="font-semibold text-foreground">
            {artwork.artist}
            </span>
        </figcaption>
    </figure>
    ```
    """

    img: Image
    caption: FigCaption
    key: Optional[str] = None

    _content_attrs = PrivateAttr(default=["img", "caption"])

    @field_validator("key")
    def validate_key(cls, key: str) -> str:
        return key_attr_validation(key)

    @field_validator("img")
    def validate_img(cls, img: Image) -> Div:
        return Div(styles="overflow-hidden rounded-md", content=img)
