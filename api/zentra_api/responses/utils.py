from pydantic import validate_call
from fastapi import status


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
def merge_dicts_list(dicts: list[dict]) -> dict:
    """Merges multiple dicts into a single one and returns it."""
    return {k: v for d in dicts for k, v in d.items()}
