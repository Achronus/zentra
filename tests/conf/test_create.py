import os

from zentra_models.cli.conf.create import make_directories


class TestMakePathDirs:
    def test_creation_success(self, zentra_path):
        make_directories(zentra_path)
        assert os.path.exists(zentra_path)

    def test_creation_fail(self, zentra_path):
        os.makedirs(zentra_path)
        make_directories(zentra_path)
        assert os.path.exists(zentra_path)
