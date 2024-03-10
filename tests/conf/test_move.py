import os
import pytest
import typer
from cli.conf.constants import CommonErrorCodes

from cli.conf.move import copy_list_of_files


class TestCopyListOfFiles:
    @pytest.fixture
    def setup_test_folders(self, tmp_path) -> tuple[str, str]:
        src_dir = os.path.join(tmp_path, "test_src")
        dest_dir = os.path.join(tmp_path, "test_dest")
        os.mkdir(src_dir)
        os.mkdir(dest_dir)
        return src_dir, dest_dir

    @staticmethod
    def test_filesnames_as_none(setup_test_folders):
        src, dest = setup_test_folders

        open(os.path.join(src, "file1.txt"), "w").close()
        open(os.path.join(src, "file2.txt"), "w").close()

        copy_list_of_files(
            src, dest, CommonErrorCodes.TEST_ERROR, CommonErrorCodes.TEST_ERROR
        )

        checks = [
            os.path.exists(os.path.join(dest, "file1.txt")),
            os.path.exists(os.path.join(dest, "file2.txt")),
        ]

        assert all(checks)

    @staticmethod
    def test_specified_filenames(setup_test_folders):
        src, dest = setup_test_folders

        open(os.path.join(src, "file1.txt"), "w").close()
        open(os.path.join(src, "file2.txt"), "w").close()
        open(os.path.join(src, "file3.txt"), "w").close()

        copy_list_of_files(
            src,
            dest,
            CommonErrorCodes.TEST_ERROR,
            CommonErrorCodes.TEST_ERROR,
            filenames=["file1.txt", "file3.txt"],
        )

        checks = [
            os.path.exists(os.path.join(dest, "file1.txt")),
            not os.path.exists(os.path.join(dest, "file2.txt")),
            os.path.exists(os.path.join(dest, "file3.txt")),
        ]

        assert all(checks)

    @staticmethod
    def test_src_invalid(setup_test_folders):
        _, dest = setup_test_folders

        with pytest.raises(typer.Exit) as e_info:
            copy_list_of_files(
                "random_src",
                dest,
                CommonErrorCodes.TEST_ERROR,
                CommonErrorCodes.TEST_ERROR,
            )

        assert e_info.value.exit_code == CommonErrorCodes.TEST_ERROR

    @staticmethod
    def test_dest_invalid(setup_test_folders):
        src, _ = setup_test_folders

        with pytest.raises(typer.Exit) as e_info:
            copy_list_of_files(
                src,
                "random_dest",
                CommonErrorCodes.TEST_ERROR,
                CommonErrorCodes.TEST_ERROR,
            )

        assert e_info.value.exit_code == CommonErrorCodes.TEST_ERROR
