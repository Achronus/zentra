import os
import pytest

from cli.conf.move import transfer_folder_file_pairs, copy_file, copy_dir_files


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


class TestTransferFolderFilePairs:
    @staticmethod
    def test_success(setup_test_files):
        src_dir, dest_dir, _ = setup_test_files

        folder_file_pairs = [("ui", "file1.txt"), ("ut", "file2.txt")]
        transfer_folder_file_pairs(folder_file_pairs, src_dir, dest_dir, "base")

        assert os.path.exists(os.path.join(dest_dir, "ui", "file1.txt"))
        assert os.path.exists(os.path.join(dest_dir, "ut", "file2.txt"))


def test_copy_file(setup_test_files):
    _, dest_dir, src_ui_dir = setup_test_files

    src_file = os.path.join(src_ui_dir, "file1.txt")
    dest_file_path = os.path.join(dest_dir, "file1.txt")
    copy_file(src_file, dest_dir)

    assert os.path.exists(dest_file_path)

    with open(dest_file_path) as f:
        assert f.read() == "test"


def test_copy_dir_files(setup_test_files):
    src_dir, dest_dir, _ = setup_test_files

    copy_dir_files(src_dir, dest_dir)
    new_dirs = os.listdir(dest_dir)
    valid_dirs = os.listdir(src_dir)

    assert len(new_dirs) == len(valid_dirs)
