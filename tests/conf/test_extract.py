import os

from cli.conf.extract import get_filenames_in_subdir


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
        assert result_filenames == dummy_files, "Error retrieving files."

    def test_fail(self, zentra_path):
        subdir_name = "test_fail"
        os.makedirs(os.path.join(zentra_path, subdir_name), exist_ok=True)

        result_filenames = get_filenames_in_subdir(
            os.path.join(zentra_path, subdir_name)
        )
        assert result_filenames == [], "Error: files exist when they shouldn't!"
