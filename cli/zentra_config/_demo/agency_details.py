from zentra.core import Page
from zentra.ui import Form, FormField
from zentra.ui.control import Input, Switch
from zentra.ui.notification import AlertDialog
from zentra.ui.presentation import Card
from zentra.uploadthing import FileUpload


form_fields = [
    FormField(
        name="agencyLogo",
        label="Agency Logo",
        content=FileUpload(),
    ),
    [
        FormField(
            name="name",
            label="Agency Name",
            content=Input(type="text", placeholder="Your Agency Name"),
        ),
        FormField(
            name="companyEmail",
            label="Agency Email",
            content=Input(type="email", placeholder="Email"),
        ),
    ],
    FormField(
        name="companyPhone",
        label="Agency Phone Number",
        content=Input(type="tel", placeholder="Phone"),
    ),
    FormField(
        name="whiteLabel",
        label="White Label Mode",
        description="Turning on White label mode will show your agency logo to all sub accounts by default. You can override this behaviour through sub account settings.",
        content=Switch(),
        message=False,
    ),
    FormField(
        name="address",
        label="Address",
        content=Input(type="text", placeholder="123 st..."),
    ),
    [
        FormField(
            name="city",
            label="City",
            content=Input(type="text", placeholder="City"),
        ),
        FormField(
            name="state",
            label="State",
            content=Input(type="text", placeholder="State"),
        ),
        FormField(
            name="zipCode",
            label="Zipcode",
            content=Input(type="text", placeholder="Zipcode"),
        ),
    ],
]

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
                            fields=form_fields,
                            btn_text="Save Agency Information",
                        ),
                    ],
                ),
            ],
        ),
    ],
)
