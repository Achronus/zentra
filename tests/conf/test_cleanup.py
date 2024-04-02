import os
import pytest

from cli.conf.cleanup import remove_files


@pytest.fixture
def setup_test_files(tmp_path) -> tuple[str, str]:
    src_dir = os.path.join(tmp_path, "test_src")
    dest_dir = os.path.join(tmp_path, "test_dest")

    src_ui_dir = os.path.join(src_dir, "ui", "base")
    src_ut_dir = os.path.join(src_dir, "ut", "base")

    dest_ui_dir = os.path.join(dest_dir, "ui")
    dest_ut_dir = os.path.join(dest_dir, "ut")

    os.mkdir(dest_dir)
    os.makedirs(src_ui_dir)
    os.makedirs(src_ut_dir)
    os.makedirs(dest_ui_dir)
    os.makedirs(dest_ut_dir)

    src_file1 = os.path.join(src_ui_dir, "file1.txt")
    with open(src_file1, "w") as f:
        f.write("test")

    src_file2 = os.path.join(src_ut_dir, "file2.txt")
    with open(src_file2, "w") as f:
        f.write("test")

    return src_dir, dest_dir, src_ui_dir


class TestRemoveFiles:
    @staticmethod
    def test_success(setup_test_files):
        src_dir, dest_dir, _ = setup_test_files

        folder_file_pairs = [("ui", "file1.txt")]
        remove_files(folder_file_pairs, dest_dir)

        assert not os.path.exists(os.path.join(dest_dir, "ui"))
