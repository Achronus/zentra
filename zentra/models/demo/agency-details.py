from zentra.core import Page
from zentra.ui import FileUpload, Form, FormField
from zentra.ui.control import Input
from zentra.ui.presentation import Card


class AgencyDetails(Page):
    """Agency details page."""

    ...


AgencyDetails(
    components=[
        Card(
            title="Agency Information",
            description="Let's create an agency for your business. You can edit agency settings later from the agency settings tab.",
            content=[
                Form(
                    fields=[
                        FormField(
                            name="agencyLogo",
                            label="Agency Logo",
                            component=FileUpload(name="agencyLogo"),
                        ),
                        FormField(
                            name="name",
                            label="Agency Name",
                            component=Input(
                                name="name",
                                label="Agency Name",
                                placeholder="Your Agency Name",
                            ),
                        ),
                    ]
                ),
            ],
            footer=None,
        ),
    ],
)
