import pytest

from tests.mappings.ui_imports import VALID_IMPORTS
from tests.mappings.ui_vals import VALID_VALS_MAP
from tests.templates.helper import SimpleCompBuilder

from zentra.core.html import Div, HTMLContent
from zentra.ui.control import Button, Input, Label
from zentra.ui.modal import Popover


class TestPopover:
    @pytest.fixture
    def popover_advanced(self) -> Popover:
        return Popover(
            trigger=Button(content="Open popover", variant="outline"),
            content=Div(
                styles="grid gap-4",
                content=[
                    Div(
                        styles="space-y-2",
                        content=[
                            HTMLContent(
                                styles="font-medium leading-none",
                                tag="h4",
                                text="Dimensions",
                            ),
                            HTMLContent(
                                styles="text-sm text-muted-foreground",
                                tag="p",
                                text="Set the dimensions for the layer.",
                            ),
                        ],
                    ),
                    Div(
                        styles="grid gap-2",
                        content=[
                            Div(
                                styles="grid grid-cols-3 items-center gap-4",
                                content=[
                                    Label(name="width", text="Width"),
                                    Input(
                                        id="width",
                                        default_value="100%",
                                        styles="col-span-2 h-8",
                                    ),
                                ],
                            ),
                            Div(
                                styles="grid grid-cols-3 items-center gap-4",
                                content=[
                                    Label(name="maxWidth", text="Max. width"),
                                    Input(
                                        id="maxWidth",
                                        default_value="300px",
                                        styles="col-span-2 h-8",
                                    ),
                                ],
                            ),
                            Div(
                                styles="grid grid-cols-3 items-center gap-4",
                                content=[
                                    Label(name="height", text="Height"),
                                    Input(
                                        id="height",
                                        default_value="25px",
                                        styles="col-span-2 h-8",
                                    ),
                                ],
                            ),
                            Div(
                                styles="grid grid-cols-3 items-center gap-4",
                                content=[
                                    Label(name="maxHeight", text="Max. height"),
                                    Input(
                                        id="maxHeight",
                                        default_value="none",
                                        styles="col-span-2 h-8",
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            styles="w-80",
        )

    @pytest.fixture
    def wrapper_advanced(self, popover_advanced: Popover) -> SimpleCompBuilder:
        return SimpleCompBuilder(popover_advanced)

    @staticmethod
    def test_content_str_advanced(wrapper_advanced: SimpleCompBuilder):
        wrapper_advanced.run(
            "content", VALID_VALS_MAP["popover"]["content"]["advanced"]
        )

    @staticmethod
    def test_import_str_advanced(wrapper_advanced: SimpleCompBuilder):
        wrapper_advanced.run("imports", VALID_IMPORTS["popover"]["advanced"])
