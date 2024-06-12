from pydantic import Field, ValidationInfo, field_validator
from zentra.base.library import ShadcnUi
from zentra.core import Component
from zentra.core.constants import PARAMETER_PREFIX
from zentra.core.utils import compress


class PaginationNext(Component, ShadcnUi):
    """
    A helper Zentra model for the [Shadcn/ui Pagination](https://ui.shadcn.com/docs/components/pagination) component. Handles the functionality for the `Next` button.
    """

    start_name: str
    set_start_name: str
    end_name: str
    set_end_name: str

    styles: str = Field(default="", validate_default=True)
    on_click: str = Field(default="", validate_default=True)

    @field_validator("styles")
    def validate_styles(cls, _: str, info: ValidationInfo) -> str:
        end_name = info.data.get("end_name")
        return f'{PARAMETER_PREFIX}{end_name} === maxItems ? "pointer-events-none opacity-50" : undefined'

    @field_validator("on_click")
    def validate_on_click(cls, _: str, info: ValidationInfo) -> str:
        start_name = info.data.get("start_name")
        set_start_name = info.data.get("set_start_name")
        end_name = info.data.get("end_name")
        set_end_name = info.data.get("set_end_name")

        return compress(
            [
                "() => {",
                f"{set_start_name}({start_name} + itemsPerPage);",
                f"{set_end_name}({end_name} + itemsPerPage);",
                "}",
            ]
        )


class PaginationPrevious(Component, ShadcnUi):
    """
    A helper Zentra model for the [Shadcn/ui Pagination](https://ui.shadcn.com/docs/components/pagination) component. Handles the functionality for the `Previous` button.
    """

    start_name: str
    set_start_name: str
    end_name: str
    set_end_name: str

    styles: str = Field(default="", validate_default=True)
    on_click: str = Field(default="", validate_default=True)

    @field_validator("styles")
    def validate_styles(cls, _: str, info: ValidationInfo) -> str:
        start_name = info.data.get("start_name")
        return f'{PARAMETER_PREFIX}{start_name} === 0 ? "pointer-events-none opacity-50" : undefined'

    @field_validator("on_click")
    def validate_on_click(cls, _: str, info: ValidationInfo) -> str:
        start_name = info.data.get("start_name")
        set_start_name = info.data.get("set_start_name")
        end_name = info.data.get("end_name")
        set_end_name = info.data.get("set_end_name")

        return compress(
            [
                "() => {",
                f"{set_start_name}({start_name} - itemsPerPage);",
                f"{set_end_name}({end_name} - itemsPerPage);",
                "}",
            ]
        )


class PaginationEllipsis(Component, ShadcnUi):
    """
    A helper Zentra model for the [Shadcn/ui Pagination](https://ui.shadcn.com/docs/components/pagination) component. Handles the functionality for the `Ellipsis`.
    """


class PaginationLink(Component, ShadcnUi):
    """
    A helper Zentra model for the [Shadcn/ui Pagination](https://ui.shadcn.com/docs/components/pagination) component. Handles the functionality for the `Link`.
    """

    href: str
    is_active: bool = False
    content: str
