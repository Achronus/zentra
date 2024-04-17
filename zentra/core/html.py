from zentra.core import Component
from zentra.core.enums.html import HTMLContentTagType
from zentra.core.js import Iterable
from zentra.nextjs import Image

from pydantic import BaseModel


class HTMLTag(BaseModel):
    """
    A parent model for all HTML tags.

    Parameters:
    - `styles` (`string, optional`) - the CSS styles to apply to the tag. Automatically adds them to `className`. `None` by default
    """

    styles: str = None


class HTMLContent(HTMLTag):
    """
    A model dedicated to HTML content tags, including `headings`, `paragraphs`, and `span`.

    Parameters:
    - `text` (`string`) - the text inside the tag. Can also include parameters, signified by a `$` at the start of the parameter name. This is useful when using the `Image` inside an `iterable` function like `map`
    - `tag` (`string`) - the type of tag to wrap around the `text` attribute. Valid options: `['h1', 'h2', 'h3', 'h4', 'h5', h6', 'p', 'span']`
    - `styles` (`string, optional`) - the CSS styles to apply to the tag. `None` by default
    """

    text: str
    tag: HTMLContentTagType


class Div(HTMLTag):
    """
    A model dedicated to the `<div>` HTML tag.

    Parameters:
    - `items` (`string | zentra.core.Component | zentra.core.js.Iterable | list[string | zentra.core.html.HTMLContent | zentra.core.Component]`) - Can be either:
      1. A simple `string` of text
      2. Any `zentra.core.Component` model, such as `zentra.ui.control.Label`
      3. Any `zentra.core.js.Iterable` model, such as `zentra.core.js.Map`
      4. A `list` of a combination of `strings` of text, `zentra.core.html.HTMLContent` items, or `zentra.core.Component` models
    - `styles` (`string, optional`) - the CSS styles to apply to the tag. `None` by default
    """

    items: str | Component | Iterable | list[str | HTMLContent | Component]


class FigCaption(HTMLTag):
    """
    A model dedicated to the `<figcaption>` HTML tag used within the `<figure>` tag.

    Parameters:
    - `text` (`string | zentra.core.html.HTMLContent | list[string | zentra.core.html.HTMLContent]`) - the text to put into the caption. Can either be:
      1. A single or multi-line `string` of text without any tags wrapped around it
      2. A `zentra.core.html.HTMLContent` object for wrapping the text in a `heading`, `paragraph`, or `span` tag
      3. A `list` of combined `string` and `zentra.core.html.HTMLContent` objects for more advanced captions
    - `styles` (`string, optional`) - the CSS styles to apply to the tag. `None` by default

    Example Usage:
    1. Advanced captioning.
    ```python
    from zentra.core.html import FigCaption, HTMLContent

    FigCaption(
        text=[
            'Photo by{" "}',
            HTMLContent(
                tag="span",
                text="{artwork.artist}",
                styles="font-semibold text-foreground",
            ),
        ],
        styles="pt-2 text-xs text-muted-foreground",
    )
    ```
    JSX equivalent ->
    ```jsx
    <figcaption className="pt-2 text-xs text-muted-foreground">
        Photo by{" "}
        <span className="font-semibold text-foreground">
            {artwork.artist}
        </span>
    </figcaption>
    ```
    """

    text: str | HTMLContent | list[str | HTMLContent]


class Figure(HTMLTag):
    """
    A model dedicated to the `<figure>` HTML tag.

    Parameters:
    - `img` (`zentra.nextjs.Image`) - a NextJS `Image` component defining the image to display in the figure
    - `caption` (`zentra.core.html.FigCaption`) - a `FigCaption` component representing the caption of the Image
    - `styles` (`string, optional`) - the CSS styles to apply to the tag. `None` by default
    - `key` (`string, optional`) - the key to add to the figure if using in a `map` or related iterable function. `None` by default. When declaring parameter values, start the variable name with a `$`
    - `img_container_styles` (`string, optional`) - a string of CSS styles to apply to a `div` tag around the image. When provided, a `div` tag is automatically wrapped around the image with the styles supplied to its `className` attribute. `None` by default

    Example usage:
    1. A detailed figure with variables.
    ```python
    from zentra.core.html import Figure, FigCaption, HTMLContent
    from zentra.nextjs import Image

    Figure(
        img=Image(
            src="$artwork.art",
            alt="Photo by $artwork.artist",
            width=300,
            height=400,
            styles="aspect-[3/4] h-fit w-fit object-cover",
        ),
        caption=FigCaption(
            text=[
                'Photo by{" "}',
                HTMLContent(
                    tag="span",
                    text="$artwork.artist",
                    styles="font-semibold text-foreground",
                )
            ],
            styles="pt-2 text-xs text-muted-foreground",
        ),
        key="$artwork.art",
        img_container_styles="overflow-hidden rounded-md",
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
            Photo by{" "}
            <span className="font-semibold text-foreground">
            {artwork.artist}
            </span>
        </figcaption>
    </figure>
    ```
    """

    img: Image
    caption: FigCaption
    key: str = None
    img_container_styles: str = None
