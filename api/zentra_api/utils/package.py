import importlib.util
import importlib.resources as pkg_resources

from pathlib import Path
from types import ModuleType


def package_path(package: str, resources: list[str]) -> Path:
    """Checks if a package exists on the machine and then returns it if True."""
    try:
        path = pkg_resources.files(package).joinpath(*resources)
        list(path.iterdir())  # Check if exists
        return Path(path)

    except FileNotFoundError:
        raise FileNotFoundError(f"'{package}.{".".join(resources)}' does not exist!")


def load_module(root: str, module_path: str) -> ModuleType:
    """Returns a module given a `root` and `module_path`, where the strings are similar to import statements separated by dots.

    Useful for dynamically retrieving constant variables data.

    Example usage:
    ```python
    module = load_module("api.responses", "error.client")
    value = getattr(module, "HTTP_401_ERROR")
    ```
    """
    try:
        module_path = f"{root}.{".".join(module_path.split())}"

        spec = importlib.util.find_spec(module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    except (ModuleNotFoundError, AttributeError):
        raise ValueError(f"Module '{module_path}' does not exist!")
