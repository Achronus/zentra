import pytest

from cli.templates.builders.structural import JSXPageBuilder
from tests.templates.helper import page_builder
from zentra.core import Page
from zentra.ui.control import (
    Button,
    Calendar,
    Checkbox,
    Collapsible,
    Input,
    InputOTP,
    Label,
)
from zentra.uploadthing import FileUpload


def page() -> Page:
    return Page(
        name="TestPage",
        components=[
            Input(id="state", type="text", placeholder="State", disabled=True),
            Input(id="zipcode", type="text", placeholder="Zipcode"),
            FileUpload(),
            Button(
                content="test",
                url="http://example.com",
                variant="secondary",
                size="sm",
                disabled=True,
            ),
            Button(
                content="test",
            ),
            Calendar(name="testCalendar"),
            Checkbox(
                id="name",
                label="Click for having a name!",
                disabled=True,
                more_info="more info test",
            ),
            Collapsible(
                name="tags1", title="Click me to open me!", items=["I'm awesome"]
            ),
            Collapsible(
                name="tags2",
                title="Click me to open me!",
                items=["I'm awesome", "You are awesome"],
            ),
            InputOTP(num_inputs=6, pattern="digits_only"),
            InputOTP(num_inputs=6, num_groups=2, pattern="afwaifhwa"),
            InputOTP(num_inputs=6, num_groups=3),
            Label(name="name", text="Enter first name"),
        ],
    )


class TestPageBuilder:
    @pytest.fixture
    def builder(self) -> JSXPageBuilder:
        return page_builder(page=page())
