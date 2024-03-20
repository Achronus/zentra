import pytest

from cli.conf.extract import extract_component_names
from zentra.core import Page
from zentra.ui import FileUpload, Form, FormField
from zentra.ui.control import Input
from zentra.ui.notification import AlertDialog
from zentra.ui.presentation import Card


class TestExtractComponentNames:
    @pytest.fixture
    def agency_details(self) -> Page:
        return Page(
            name="AgencyDetails",
            components=[
                AlertDialog(
                    name="agencyAlertDialog",
                    content=[
                        Card(
                            name="agencyInfo",
                            title="Agency Information",
                            description="Let's create an agency for your business. You can edit agency settings later from the agency settings tab.",
                            content=[
                                Form(
                                    name="agencyForm",
                                    fields=[
                                        FormField(
                                            name="agencyLogo",
                                            label="Agency Logo",
                                            content=FileUpload(name="agencyLogo"),
                                        ),
                                        FormField(
                                            name="name",
                                            label="Agency Name",
                                            content=Input(
                                                name="name",
                                                label="Agency Name",
                                                placeholder="Your Agency Name",
                                            ),
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        )

    def test_success(self, agency_details: Page):
        json_data = agency_details.get_schema()

        result = extract_component_names(json_data)
        assert result == [
            "Page",
            "AlertDialog",
            "Card",
            "Form",
            "FormField",
            "FileUpload",
            "FormField",
            "Input",
        ]
