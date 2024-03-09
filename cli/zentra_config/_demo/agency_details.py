from zentra.core import Page
from zentra.ui import FileUpload, Form, FormField
from zentra.ui.control import Input
from zentra.ui.notification import AlertDialog
from zentra.ui.presentation import Card


agency_details = Page(
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
