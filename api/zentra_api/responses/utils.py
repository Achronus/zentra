from pydantic import validate_call
from fastapi import status

from zentra_api.utils.package import load_module


@validate_call
def build_response(code: int, no_strip: bool = False) -> str:
    """A utility function for building a string representation of a response code."""
    valid_codes: dict[int, str] = {}
    for item in status.__all__:
        item_code = int(item.split("_")[1])
        valid_codes[item_code] = item

    try:
        item = valid_codes[code]

        if no_strip:
            return item

        return item.lstrip("HTTP_")

    except KeyError:
        raise ValueError(
            f"'{code}' isn't a valid HTTP response code! Try 'fastapi.status' for a list of valid response codes"
        )


@validate_call
def get_code_status(code: int) -> str:
    """A utility function for retrieving the code status based on the code."""
    _ = build_response(code)  # Validate code exists

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
def response_models(codes: int | list[int]) -> dict:
    """A utility function for getting response model schemas."""

    ROOT_PATH = "zentra_api.responses"

    if isinstance(codes, int):
        codes = [codes]

    models = []
    for code in codes:
        response = build_response(code, no_strip=True).split("_")[:2]
        code_type = get_code_status(code)
        const_name = f"{response[0]}_{code_type}_{str(code)}".upper()

        module = load_module(ROOT_PATH, "models")
        models.append(getattr(module, const_name))

    models_dict = {key: value for d in models for key, value in d.items()}
    return models_dict


@validate_call
def merge_dicts(*dicts: dict) -> dict:
    """Merges multiple dicts into a single one and returns it."""
    return {k: v for d in dicts for k, v in d.items()}
