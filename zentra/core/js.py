from zentra.core import Component
from zentra.base.html import HTMLTag
from zentra.base.js import JSIterable


class Map(JSIterable):
    """
    A model dedicated to the [JavaScript map](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/map) iterable function.

    Parameters:
    - `obj_name` (`string`) - the name of the data object array to iterate over. Must be `lowercase` or `camelCase`, a `single word`, and up to a maximum of `20` characters
    - `param_name` (`string`) - the name of the parameter to iterate over inside the map. Must be `lowercase` or `camelCase`, a `single word`, and up to a maximum of `20` characters
    - `content` (`zentra.core.html.HTMLTag | zentra.core.Component`) - Can be either:
      1. Any `zentra.core.html.HTMLTag` model, such as `zentra.core.html.Div` or `zentra.core.html.Figure`
      2. Any `zentra.core.Component` model, such as `zentra.ui.control.Label`

    Example usage:
    1. A map with a predefined data array of images.
    ```python
    from zentra.core.jsx import Map
    from zentra.core.html import Figure, FigCaption, HTMLContent

    fig = Figure(
        key="$.artwork.artist",
        styles="shrink-0",
        img_container_styles="overflow-hidden rounded-md",
        img=Image(
            src="$.artwork.art",
            alt="Photo by $artwork.artist",
            styles="aspect-[3/4] h-fit w-fit object-cover",
            width=300,
            height=400
        ),
        caption=FigCaption(
            styles="pt-2 text-xs text-muted-foreground",
            text=[
                'Photo by ',
                HTMLContent(
                    tag="span",
                    styles="font-semibold text-foreground",
                    text="$.artwork.artist"
                )
            ]
        ),
    )

    Map(
        obj_name="works",
        param_name="artwork",
        content=fig
    )
    ```
    JSX equivalent ->
    ```jsx
    {works.map((artwork) => (
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
    ))}
    ```
    """

    content: HTMLTag | Component
