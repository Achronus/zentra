import os
import pytest

from cli.conf.extract import extract_component_names, get_filenames_in_subdir
from cli.zentra_config._demo.agency_details import agency_details


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
    def test_success(self):
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
