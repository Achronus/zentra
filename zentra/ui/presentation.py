from typing import Optional

from pydantic import Field, ValidationInfo, field_validator
from pydantic_core import PydanticCustomError

from zentra.core import LOWER_CAMELCASE_SINGLE_WORD, Component, has_valid_pattern
from zentra.core.enums.ui import BadgeVariant, Orientation, SkeletonPreset, ToggleType
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
        5. Or a parameter, signified by a `$.` at the start of the parameter name. Parameters are useful when using the `Image` inside an `iterable` function like `zentra.js.Map`
    - `alt` (`string`) - an `alt` tag used to describe the image for screen readers and search engines. Also, acts as fallback text if the image is disabled, errors, or fails to load. Can also include parameters, signified by a `$.` at the start of the parameter name
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
    - `text` (`string`) - the descriptive text to put into the badge. Can include parameter variables (indicated by starting the variable name with a `$.`)
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


class SkeletonShell(Component, ShadcnUi):
    """
    A helper Zentra model for the [Shadcn/ui Skeleton](https://ui.shadcn.com/docs/components/skeleton) component. Acts as an individual `Skeleton` component.

    Cannot be used on its own, must be used inside a `zentra.ui.presentation.Skeleton` or `zentra.ui.presentation.SkeletonGroup` model.

    Parameters:
    - `styles` (`string`) - a set of custom CSS classes to apply to the skeleton shell. Automatically adds them to `className`. `None` by default
    """

    styles: str


class SkeletonGroup(Component, ShadcnUi):
    """
    A helper Zentra model for the [Shadcn/ui Skeleton](https://ui.shadcn.com/docs/components/skeleton) component. Acts as a single group of `Skeleton` items.

    Cannot be used on its own, must be used inside a `zentra.ui.presentation.Skeleton` model.

    Parameters:
    - `styles` (`string`) - a set of custom CSS classes to apply to the skeleton group container. Automatically adds them to `className`. `None` by default
    - `items` (`list[zentra.ui.presentation.SkeletonShell]`) - a list of `SkeletonShell` models to use in the group
    """

    styles: str
    items: list[SkeletonShell]


class Skeleton(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui Skeleton](https://ui.shadcn.com/docs/components/skeleton) component.

    Parameters:
    - `preset` (`string`) - the type of skeleton to create. Either select an available preset or create your own. Valid options: `['custom', 'testimonial', 'card']`
    - `styles` (`string, optional`) - a set of custom CSS classes to apply to the root `div` container of the skeleton items. Automatically adds them to `className`. `None` by default
    - `items` (`zentra.ui.presentation.SkeletonShell | zentra.ui.presentation.SkeletonGroup | list[zentra.ui.presentation.SkeletonShell | zentra.ui.presentation.SkeletonGroup], optional`) - Can only be used when `preset="custom"`. Can be either:
      1. A single `SkeletonShell` models
      2. A single `SkeletonGroup` models for multiple `SkeletonShells` in a single `div` container
      3. A list of `SkeletonShell` and/or `SkeletonGroup` models for multiple `SkeletonShells` in multiple separate `div` containers. Useful for creating complex skeletons
      4. `None` when using a different `preset`. `None` by default

    Examples:
    1. Testimonial preset
    ```python
    from zentra.ui.presentation import Skeleton

    comp = Skeleton(preset="testimonial")
    ```
    JSX equivalent ->
    ```jsx
    import { Skeleton } from "@/components/ui/skeleton"


    <div className="flex items-center space-x-4">
      <Skeleton className="h-12 w-12 rounded-full" />
      <div className="space-y-2">
        <Skeleton className="h-4 w-[250px]" />
        <Skeleton className="h-4 w-[200px]" />
      </div>
    </div>
    ```

    2. Card preset
    ```python
    from zentra.ui.presentation import Skeleton

    comp = Skeleton(preset="card")
    ```
    JSX equivalent ->
    ```jsx
    import { Skeleton } from "@/components/ui/skeleton"


    <div className="flex flex-col space-y-3">
      <Skeleton className="h-[125px] w-[250px] rounded-xl" />
      <div className="space-y-2">
        <Skeleton className="h-4 w-[250px]" />
        <Skeleton className="h-4 w-[200px]" />
      </div>
    </div>
    ```

    3. Custom preset with a single shell
    ```python
    from zentra.ui.presentation import Skeleton, SkeletonShell

    comp = Skeleton(
        preset="custom",
        styles="flex items-center",
        items=SkeletonShell(styles="h-[125px] w-[250px] rounded-xl"),
    )
    ```
    JSX equivalent ->
    ```jsx
    import { Skeleton } from "@/components/ui/skeleton"

    <div className="flex items-center">
      <Skeleton className="h-[125px] w-[250px] rounded-xl" />
    </div>
    ```
    """

    preset: SkeletonPreset
    styles: Optional[str] = Field(default=None, validate_default=True)
    items: Optional[
        SkeletonShell | SkeletonGroup | list[SkeletonShell | SkeletonGroup]
    ] = Field(default=None, validate_default=True)

    @field_validator("items")
    def validate_items(
        cls,
        items: list[SkeletonShell | list[SkeletonGroup]] | None,
        info: ValidationInfo,
    ) -> list[SkeletonShell | list[SkeletonGroup]] | None:
        preset: str = info.data.get("preset")

        if preset != "custom" and items is not None:
            raise PydanticCustomError(
                "invalid_preset",
                "cannot use 'items' without" + ' preset="custom"',
                dict(wrong_value=preset),
            )

        if preset == "custom" and items is None:
            raise PydanticCustomError(
                "missing_items",
                "missing 'items' with" + ' preset="custom"',
                dict(wrong_value=items),
            )

        return items

    @field_validator("styles")
    def validate_styles(cls, styles: str | None, info: ValidationInfo) -> str | None:
        styles_dict = {
            "testimonial": "flex items-center space-x-4",
            "card": "flex flex-col space-y-3",
        }
        preset = info.data.get("preset")

        if styles is None and preset != "custom":
            return styles_dict[preset]

        return styles

    @property
    def container_name(self) -> str:
        return "div"


class TableCell(Component, ShadcnUi):
    """
    A helper Zentra model for the [Shadcn/ui Table](https://ui.shadcn.com/docs/components/table) component. Represents a single table cell.

    Cannot be used on its own, must be used inside a `zentra.ui.presentation.Table` or `zentra.ui.presentation.TableMap` model.

    Parameters:
    - `text` (`string`) - the descriptive text to put into the cell. Can include parameter variables (indicated by starting the variable name with a `$.`)
    - `col_span` (`integer, optional`) - an optional positive integer to indicate how many columns this cell takes up. `None` by default
    - `styles` (`string, optional`) - a set of custom CSS classes to apply to the cell. Automatically adds them to `className`. `None` by default
    """

    text: str
    col_span: Optional[int] = Field(default=None, ge=1)
    styles: Optional[str] = None


class TableRow(Component, ShadcnUi):
    """
    A helper Zentra model for the [Shadcn/ui Table](https://ui.shadcn.com/docs/components/table) component. Represents a single table row.

    Cannot be used on its own, must be used inside a `zentra.ui.presentation.Table` model.

    Parameters:
    - `cells` (`list[string | zentra.ui.presentation.TableCell`]) - A list of strings or `TableCell` models containing the body content. When `string` can include parameter variables (indicated by starting the variable name with a `$.`)
    - `key` (`string | integer, optional`) - an optional unique identifier for each row. Added to the `key` prop. `None` by default
    """

    cells: list[str | TableCell]
    key: Optional[str | int] = None


class TableMapRow(TableRow, ShadcnUi):
    """
    A helper Zentra model for the [Shadcn/ui Table](https://ui.shadcn.com/docs/components/table) component. Represents a single table row for a `TableMap`.

    Cannot be used on its own, must be used inside a `zentra.ui.presentation.TableMap` model.

    Parameters:
    - `cells` (`list[string | zentra.ui.presentation.TableCell`]) - A list of strings or `TableCell` models containing the body content. Cell text is automatically converted to a parameter string and prepended with the `param_name`
    - `key` (`string | integer, optional`) - an optional unique identifier for each row. Added to the `key` prop. `None` by default
    """

    @field_validator("cells")
    def validate_cells(cls, cells: list[str | TableCell]) -> list[str | TableCell]:
        for idx, item in enumerate(cells):
            item_type = "str"

            if isinstance(item, TableCell):
                item = item.text
                item_type = "TableCell.text"

            if " " in item:
                raise PydanticCustomError(
                    "invalid_parameter_string",
                    f"'cells.{idx}' contains whitespace in '{item_type}'. Cannot be converted to a parameter",
                    dict(wrong_value=item, value_idx=idx),
                )
        return cells


class TableMap(Component, ShadcnUi):
    """
    A helper Zentra model for the [Shadcn/ui Table](https://ui.shadcn.com/docs/components/table) component. Wraps a set of table cells in a `JavaScript Map` function.

    Cannot be used on its own, must be used inside a `zentra.ui.presentation.Table` model.

    Parameters:
    - `obj_name` (`string`) - the name of the data object array to iterate over. Must be `lowercase` or `camelCase`, a `single word`, and up to a maximum of `20` characters
    - `param_name` (`string`) - the name of the parameter to iterate over inside the map. Must be `lowercase` or `camelCase`, a `single word`, and up to a maximum of `20` characters
    - `row` (`TableMapRow`) - a `TableMapRow` model containing the body content
    - `map_idx` (`boolean, optional`) - a flag for adding the map index as a parameter and automatically using it as the `TableRow` `key` value. `True` by default
    """

    obj_name: str = Field(min_length=1, max_length=20)
    param_name: str = Field(min_length=1, max_length=20)
    row: TableMapRow
    map_idx: bool = True

    @field_validator("obj_name", "param_name")
    def validate_name(cls, v: str) -> str:
        result = has_valid_pattern(pattern=LOWER_CAMELCASE_SINGLE_WORD, value=v)

        if not result:
            raise PydanticCustomError(
                "string_pattern_mismatch",
                f"'{v}'. Must be 'lowercase' or 'camelCase', a single word and a maximum of '20' characters\n",
                dict(wrong_value=v, pattern=LOWER_CAMELCASE_SINGLE_WORD),
            )

        return v


class Table(Component, ShadcnUi):
    """
    A Zentra model for the [Shadcn/ui Table](https://ui.shadcn.com/docs/components/table) component.

    Parameters:
    - `headings` (`list[string | zentra.ui.presentation.TableCell]`) - a list of strings or `TableCell` models defining the `TableHeads` for the table columns
    - `body` (`list[zentra.ui.presentation.TableRow] | zentra.ui.presentation.TableMap`) - can be either:
      1. A list of `TableRow` models containing text based body content
      2. A `TableMap` model containing the iterable body content. Useful for iterating over `Arrays` of data
    - `footer` (`list[string | zentra.ui.presentation.TableCell], optional`) - a list of strings or `TableCell` models containing the footer content. `None` by default
    - `caption` (`string, optional`) - optional descriptive text for adding a `TableCaption` to the table. `None` by default
    """

    headings: list[str | TableCell]
    body: list[TableRow] | TableMap
    footer: Optional[list[str | TableCell]] = None
    caption: Optional[str] = None
