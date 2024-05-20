from typing import Optional

from pydantic import Field, field_validator
from pydantic_core import PydanticCustomError

from zentra.core import Component
from zentra.core.enums.ui import BadgeVariant, Orientation, ToggleType
from zentra.custom import CustomUrl
from zentra.nextjs import Image, StaticImage
from zentra.ui import ShadcnUi


class AccordionItem(Component, ShadcnUi):
    """
    A helper Zentra model for the [Shadcn/ui Accordion](https://ui.shadcn.com/docs/components/accordion) component. Represents a single accordion item.

    Cannot be used on its own, must be used inside a `zentra.ui.presentation.Accordion` model.

    Parameters:
    - `title` (`string`) - the title of the accordion item. Added to `AccordionTrigger`
    - `content` (`string`) - the text content of the accordion item. Added to `AccordionContent`
    - `disabled` (`boolean, optional`) - adds the disabled property, preventing the item from being clicked. `False` by default
    """

    title: str
    content: str
    disabled: bool = False


class Accordion(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui Accordion](https://ui.shadcn.com/docs/components/accordion) component.

    Parameters:
    - `items` (`list[zentra.ui.presentation.AccordionItems]`) - a list of `AccordionItem` models
    - `type` (`string, optional`) - determines how many items can be opened at the same time. Valid options: `['single', 'multiple']`. `single` by default
    - `orientation` (`string, optional`) - the axis orientation of the accordion. Valid options: `['vertical', 'horizontal']`. `vertical` by default
    - `disabled` (`boolean, optional`) - adds the disabled property, preventing the accordion from being clicked. `False` by default
    - `styles` (`string, optional`) - a set of custom CSS classes to apply to the accordion. Automatically adds them to `className`. `w-full` by default
    """

    items: list[AccordionItem]
    type: ToggleType = "single"
    orientation: Orientation = "vertical"
    disabled: bool = False
    styles: Optional[str] = "w-full"

    @property
    def custom_common_attributes(self) -> list[str]:
        return ["orientation"]


class AspectRatio(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui AspectRatio](https://ui.shadcn.com/docs/components/aspect-ratio) component.

    Parameters:
    - `img` (`zentra.nextjs.Image`) - the `Image` model to use inside the aspect ratio
    - `ratio` (`string | integer`) - the ratio to apply to the aspect ratio. Can be a string for defining an equation (e.g., `16 / 9`) that results in an integer or a standard integer (e.g., `1`)
    - `styles` (`string, optional`) - a set of custom CSS classes to apply to the aspect ratio. Automatically adds them to `className`. `None` by default
    """

    img: Image
    ratio: str | int
    styles: Optional[str] = None

    @field_validator("ratio")
    def validate_ratio(cls, ratio: str | int) -> str | int:
        if isinstance(ratio, str):
            try:
                eval(ratio)
            except NameError as e:
                raise PydanticCustomError(
                    "invalid_equation",
                    f"ratio must be an 'integer' or a valid 'numeric equation' that results in an 'integer'\n  Equation error -> NameError: {e}\n",
                    dict(wrong_value=ratio),
                )

        return ratio


class Avatar(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui Avatar](https://ui.shadcn.com/docs/components/avatar) component.

    Parameters:
    - `src` (`string | zentra.nextjs.StaticImage`) - can be either:
        1. A local path string starting with `/`, `./`, or `../`
        2. A statically imported image file represented by a `StaticImage` model
        3. An absolute external URL starting with `http://`, `https://`, `ftp://`, or `file://`
        4. An informative path string starting with `mailto:`, or `tel:`
        5. Or a parameter, signified by a `$` at the start of the parameter name. Parameters are useful when using the `Image` inside an `iterable` function like `zentra.js.Map`
    - `alt` (`string`) - an `alt` tag used to describe the image for screen readers and search engines. Also, acts as fallback text if the image is disabled, errors, or fails to load. Can also include parameters, signified by a `$` at the start of the parameter name
    - `fallback_text` (`string`) - the fallback text if the avatar image doesn't load. Up to a maximum of `2` characters
    """

    src: str | StaticImage
    alt: str
    fallback_text: str = Field(min_length=1, max_length=2)

    @property
    def inner_attributes(self) -> list[str]:
        return ["src", "alt"]

    @field_validator("src")
    def validate_src(cls, src: str | StaticImage) -> str | StaticImage:
        if isinstance(src, str):
            CustomUrl(url=src, plus_param=True).validate_url()

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
    - `value` (`integer, optional`) - the initial value of the progress bar. Assigned to the `setProgress` function in the `useEffect`. `10` by default
    - `min` (`integer, optional`) - the minimum size of the progress bar. Assigned as the initial value of the `useState` hook. `0` by default
    - `max` (`integer, optional`) - the maximum size of the progress bar. Assigned as the maximum value of the `setTimeout` function in the `useEffect` hook. `100` by default
    - `styles` (`string, optional`) - a set of custom CSS classes to apply to the progress bar. Automatically adds them to `className`. `w-[60%]` by default
    """

    value: int = 10
    min: int = 0
    max: int = 100
    styles: Optional[str] = "w-[60%]"

    @property
    def custom_common_attributes(self) -> list[str]:
        return ["min", "max"]

    @property
    def use_state_names(self) -> tuple[str, str]:
        """Defines the `useState` hook `get` and `set` names."""
        return ["progress", "setProgress"]


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
    - `styles` (`string, optional`) - a set of custom CSS classes to apply to the separator. Automatically adds them to `className`. `None` by default
    - `orientation` (`string, optional`) - the axis orientation of the separator. Valid options: `['horizontal', 'vertical']`. `vertical` by default
    """

    styles: Optional[str] = None
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
