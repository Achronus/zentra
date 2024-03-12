import os
import pytest

from cli.conf.extract import extract_component_names, get_filenames_in_subdir
from zentra.core import Page
from zentra.ui import FileUpload, Form, FormField
from zentra.ui.control import Input
from zentra.ui.notification import AlertDialog
from zentra.ui.presentation import Card


class TestGetFilenamesInSubdir:
    def test_success(self, zentra_path):
        subdir_name = "test_success"
        dummy_files = [
            os.path.join(zentra_path, subdir_name, "file1.py"),
            os.path.join(zentra_path, subdir_name, "file2.py"),
        ]

        os.makedirs(os.path.join(zentra_path, subdir_name), exist_ok=True)
        for filename in dummy_files:
            with open(filename, "w") as f:
                f.write("")

        result_filenames = get_filenames_in_subdir(
            os.path.join(zentra_path, subdir_name)
        )

        dummy_files = [os.path.basename(file) for file in dummy_files]
        assert result_filenames == dummy_files, "Error retrieving files."

    def test_fail(self, zentra_path):
        subdir_name = "test_fail"
        os.makedirs(os.path.join(zentra_path, subdir_name), exist_ok=True)

        result_filenames = get_filenames_in_subdir(
            os.path.join(zentra_path, subdir_name)
        )
        assert result_filenames == [], "Error: files exist when they shouldn't!"


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
