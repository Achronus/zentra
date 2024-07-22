import importlib.util
from types import ModuleType

from pydantic import validate_call
from fastapi import status


@validate_call
def build_response(code: int, no_strip: bool = False) -> str:
    """A utility function for building a string representation of a response code."""
    for item in status.__all__:
        if str(code) in item:
            if no_strip:
                return item

            return item.lstrip("HTTP_")

    raise ValueError(
        f"'{code}' isn't a valid HTTP response code! Try 'fastapi.status' for a list of valid response codes"
    )


@validate_call
def get_code_status(code: int) -> str:
    """A utility function for retrieving the code status based on the code."""
    # Validate code exists
    _ = build_response(code)

    code_type_map = {
        "info": range(100, 200),
        "success": range(200, 300),
        "redirect": range(300, 400),
        "error": range(400, 600),
    }

    for key, code_range in code_type_map.items():
        if code in code_range:
            return key


@validate_call
def load_module(root: str, module_path: str) -> ModuleType:
    """Returns a module given a `root` and `module_path`, where the strings are similar to import statements separated by dots.

    Useful for dynamically retrieving constant variables data.

    Example usage:
    ```python
    module = load_module("api.responses", "error.client")
    value = getattr(module, "HTTP_401_ERROR")
    ```
    """
    spec = importlib.util.find_spec(f"{root}.{module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@validate_call
def response_models(codes: int | list[int]) -> dict:
    """A utility function for getting response model schemas."""

    ROOT_PATH = "app.api.responses"

    if isinstance(codes, int):
        codes = [codes]

    models = []
    for code in codes:
        response = build_response(code, no_strip=True).split("_")[:2]
        code_type = get_code_status(code)
        const_name = f"{response[0]}_{code_type}_{str(code)}".upper()

        module = load_module(ROOT_PATH, "models")
        models.append(getattr(module, const_name))

    print(models)
    exit()
    models_dict = {key: value for d in models for key, value in d.items()}
    return models_dict
