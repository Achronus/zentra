import pytest

from zentra.ui import FileUpload, Form, FormField
from zentra.ui.control import Input


class TestFormValidator:
    def test_success(self):
        Form(
            name="testForm",
            layout=[1, 2],
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
                FormField(
                    name="companyEmail",
                    label="Agency Email",
                    content=Input(
                        name="email",
                        label="Account Email",
                        placeholder="Email",
                        read_only=True,
                    ),
                ),
            ],
        )

    def test_fail(self):
        with pytest.raises(ValueError):
            Form(
                name="testForm",
                layout=[2],
                fields=[
                    FormField(
                        name="agencyLogo",
                        label="Agency Logo",
                        content=FileUpload(name="agencyLogo"),
                    ),
                ],
            )
