from pydantic import Field, HttpUrl, field_validator
from pydantic_core import PydanticCustomError
from zentra.core import Component
from zentra.core.enums.ui import BadgeVariant, Orientation
from zentra.nextjs import StaticImage
from zentra.ui import ShadcnUi


class Accordion(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui Accordion](https://ui.shadcn.com/docs/components/accordion) component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class AspectRatio(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui AspectRatio](https://ui.shadcn.com/docs/components/aspect-ratio) component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class Avatar(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui Avatar](https://ui.shadcn.com/docs/components/avatar) component.

    Parameters:
    - `src` (`string | HttpUrl | zentra.nextjs.StaticImage`) - can be either:
        1. A path string (e.g., `/profile.png`)
        2. A statically imported image file represented by a `StaticImage` model
        3. An absolute external URL denoted by `http`
        4. Or a parameter, signified by a `$` at the start of the parameter name
    - `alt` (`string`) - an `alt` tag used to describe the image for screen readers and search engines. Also, acts as fallback text if the image is disabled, errors, or fails to load. Can also include parameters, signified by a `$` at the start of the parameter name
    - `fallback_text` (`string`) - the fallback text if the avatar image doesn't load. Up to a maximum of `2` characters
    """

    src: str | HttpUrl | StaticImage
    alt: str
    fallback_text: str = Field(min_length=1, max_length=2)

    @property
    def inner_attributes(self) -> list[str]:
        return ["src", "alt"]

    @field_validator("src")
    def validate_src(
        cls, src: str | HttpUrl | StaticImage
    ) -> str | HttpUrl | StaticImage:
        if isinstance(src, str) and not src.startswith(("$", "http", "/")):
            raise PydanticCustomError(
                "invalid_string_value",
                "when 'string' must be a 'parameter' (start with '$'), a path string (start with '/'), or 'url' (start with 'http')\n",
                dict(wrong_value=src),
            )

        return src

    @field_validator("fallback_text")
    def validate_fallback_text(cls, text: str) -> str:
        return text.upper()


class Badge(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui Badge](https://ui.shadcn.com/docs/components/badge) component.

    Parameters:
    - `text` (`string`) - the descriptive text to put into the badge. Can include parameter variables (indicated by starting the variable name with a `$`)
    - `variant` (`string, optional`) - the style of the badge. Valid options: `['default', 'secondary', 'destructive', 'outline']`. `default` by default
    """

    text: str = Field(min_length=1)
    variant: BadgeVariant = "default"


class Card(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui Card](https://ui.shadcn.com/docs/components/card) component.

    Parameters:
    - `name` (`str`) - the name of the component
    """

    title: str = None
    description: str = None
    content: list[Component] = None
    footer: list[Component] = None


class Carousel(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui Carousel](https://ui.shadcn.com/docs/components/carousel) component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class DataTable(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui DataTable](https://ui.shadcn.com/docs/components/data-table) component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class HoverCard(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui HoverCard](https://ui.shadcn.com/docs/components/hover-card) component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class Progress(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui Progress](https://ui.shadcn.com/docs/components/progress) component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class Resizeable(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui Resizeable](https://ui.shadcn.com/docs/components/resizeable) component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class Separator(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui Separator](https://ui.shadcn.com/docs/components/separator) component.

    Parameters:
    - `styles` (`string, optional`) - an optional set of CSS classes. `None` by default
    - `orientation` (`string, optional`) - the axis orientation of the separator. Valid options: `['horizontal', 'vertical']`. `vertical` by default
    """

    styles: str = None
    orientation: Orientation = "vertical"


class Skeleton(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui Skeleton](https://ui.shadcn.com/docs/components/skeleton) component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class Table(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui Table](https://ui.shadcn.com/docs/components/table) component.

    Parameters:
    - `name` (`str`) - the name of the component
    """
