import os

from zentra_models.cli.conf.env import (
    find_zentra_root,
    get_zentra_root,
    set_zentra_root,
)


class TestFindZentraRoot:
    @staticmethod
    def test_valid(tmp_path):
        path = os.path.join(tmp_path, "zentra.root")
        open(path, "x").close()

        assert find_zentra_root(tmp_path)

    @staticmethod
    def test_fail_valid(tmp_path):
        assert not find_zentra_root(tmp_path)


class TestDotEnv:
    @staticmethod
    def test_set_zentra_root(monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(os, "environ", {})
            set_zentra_root("/path/to/zentra")
            assert os.environ["ZENTRA_ROOT"] == "/path/to/zentra"

    @staticmethod
    def test_get_zentra_root_valid(monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(os, "environ", {"ZENTRA_ROOT": "/path/to/zentra"})
            result = get_zentra_root()
            assert result == "/path/to/zentra"
