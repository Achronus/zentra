import os

from zentra_models.cli.local.files import make_directories, remove_files


class TestMakePathDirs:
    def test_creation_success(self, zentra_path):
        make_directories(zentra_path)
        assert os.path.exists(zentra_path)

    def test_creation_fail(self, zentra_path):
        os.makedirs(zentra_path)
        make_directories(zentra_path)
        assert os.path.exists(zentra_path)


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
