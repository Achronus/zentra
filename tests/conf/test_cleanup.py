import os
import pytest

from cli.conf.cleanup import remove_files


class TestRemoveFiles:
    @staticmethod
    def test_success(tmp_path):
        dest_dir = os.path.join(tmp_path, "test_dest")
        file1 = os.path.join(dest_dir, "ui", "file1.txt")

        os.makedirs(os.path.join(dest_dir, "ui"))
        with open(file1, "w") as f:
            f.write("test")

        folder_file_pairs = [("ui", "file1.txt")]
        remove_files(folder_file_pairs, dest_dir)

        checks = [
            not os.path.exists(file1),
            not os.path.exists(os.path.join(dest_dir, "ui")),
        ]
        assert all(checks)
