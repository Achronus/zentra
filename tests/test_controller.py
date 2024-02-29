import pytest


def test_make_path_success(folder_controller):
    assert folder_controller.make_path() is True
