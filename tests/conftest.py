import os
import pytest


DIR_NAME = "zentra"


@pytest.fixture
def dir_name() -> str:
    return DIR_NAME


@pytest.fixture
def zentra_path(tmp_path, dir_name) -> str:
    return os.path.join(tmp_path, dir_name)
