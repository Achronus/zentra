from pathlib import Path
import pytest

from zentra_api.utils.package import package_path


@pytest.fixture(scope="session", autouse=True)
def clear_logs_after_tests(request):
    path = package_path("zentra_api", ["logs"])
    filepath = Path(path, "testing.log")

    if filepath.exists():

        def clear_log_file():
            with open(filepath, "w") as file:
                file.truncate(0)

        request.addfinalizer(clear_log_file)
