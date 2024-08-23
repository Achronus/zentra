from pathlib import Path
import pytest
from math import ceil

from zentra_api.utils.package import package_path


@pytest.fixture
def key_length() -> int:
    def _key_length(size: int):
        return ceil((size // 8) * 8 / 6)

    return _key_length


@pytest.fixture(scope="session", autouse=True)
def clear_logs_after_tests(request):
    path = package_path("zentra_sdk", ["logs"])
    filepath = Path(path, "testing.log")

    if filepath.exists():

        def clear_log_file():
            with open(filepath, "w") as file:
                file.truncate(0)

        request.addfinalizer(clear_log_file)
