import os
import pytest

from cli.conf.create import make_path_dirs


class TestMakePathDirs:
    def test_creation_success(self, zentra_path):
        make_path_dirs(zentra_path)
        assert os.path.exists(zentra_path)

    def test_creation_fail(self, zentra_path):
        os.makedirs(zentra_path)
        make_path_dirs(zentra_path)
        assert os.path.exists(zentra_path)
