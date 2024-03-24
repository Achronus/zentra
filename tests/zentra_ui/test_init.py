import pytest

from zentra.ui import Form, FormField
from zentra.ui.control import Input
from zentra.uploadthing import FileUpload


class TestFormValidator:
    def test_success(self):
        Form(
            name="testForm",
            layout=[1, 2],
            fields=[
                FormField(
                    name="agencyLogo",
                    label="Agency Logo",
                    content=FileUpload(),
                ),
                FormField(
                    name="name",
                    label="Agency Name",
                    content=Input(
                        type="text",
                        label="Agency Name",
                        placeholder="Your Agency Name",
                    ),
                ),
                FormField(
                    name="companyEmail",
                    label="Agency Email",
                    content=Input(
                        type="email",
                        label="Account Email",
                        placeholder="Email",
                        read_only=True,
                    ),
                ),
            ],
        )

    def test_invalid_single_row(self):
        with pytest.raises(ValueError):
            Form(
                name="testForm",
                layout=[2],
                fields=[
                    [
                        FormField(
                            name="agencyLogo",
                            label="Agency Logo",
                            content=FileUpload(),
                        ),
                    ]
                ],
            )
