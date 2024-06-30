from pydantic import ValidationError
import pytest

from zentra_models.ui import Form, FormField
from zentra_models.ui.control import Input
from zentra_models.uploadthing import FileUpload


class TestForm:
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
                        id="agencyName",
                        type="text",
                        label="Agency Name",
                        placeholder="Your Agency Name",
                    ),
                ),
                FormField(
                    name="companyEmail",
                    label="Agency Email",
                    content=Input(
                        id="email",
                        type="email",
                        label="Account Email",
                        placeholder="Email",
                        read_only=True,
                    ),
                ),
            ],
        )

    def test_invalid_single_row(self):
        with pytest.raises(ValidationError):
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

    def test_invalid_row_size(self):
        with pytest.raises(ValidationError):
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
                        FormField(
                            name="agencyLogo",
                            label="Agency Logo",
                            content=FileUpload(),
                        ),
                        FormField(
                            name="agencyLogo",
                            label="Agency Logo",
                            content=FileUpload(),
                        ),
                        FormField(
                            name="agencyLogo",
                            label="Agency Logo",
                            content=FileUpload(),
                        ),
                    ]
                ],
            )
