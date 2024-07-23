from typing import Any

from pydantic_core import PydanticCustomError


def data_array_validation(data: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """A helper validation function that verifies that a `DataArray.data` attribute is correct."""
    if len(data) == 0 or len(data[0]) == 0:
        raise PydanticCustomError(
            "missing_data",
            "No data exists in the list",
            dict(wrong_value=data),
        )

    reference_dict = data[0]
    for idx, d in enumerate(data[1:], start=1):
        if set(d.keys()) != set(reference_dict.keys()):
            raise PydanticCustomError(
                "invalid_dictionary_keys",
                f"position: 2.{idx} -> '{d.keys()} != {reference_dict.keys()}'\n",
                dict(wrong_value=d, full_data=data),
            )

        for key, value in reference_dict.items():
            if type(d[key]) is not type(value):
                raise PydanticCustomError(
                    "invalid_value_type",
                    f"position: 2.{idx} -> '{type(d[key])} ({d[key]}) != {type(value)} ({value})'\n",
                    dict(wrong_value=d, full_data=data),
                )

        return data
