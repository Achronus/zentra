import re
from typing import Any, Optional
from pydantic_core import PydanticCustomError

from zentra.core.enums.ui import InputOTPPatterns


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
            if type(d[key]) != type(value):
                raise PydanticCustomError(
                    "invalid_value_type",
                    f"position: 2.{idx} -> '{type(d[key])} ({d[key]}) != {type(value)} ({value})'\n",
                    dict(wrong_value=d, full_data=data),
                )

        return data


def calendar_validation(
    val: bool | int, mode: str, condition: bool, err_msg_word: str
) -> bool | int:
    """A helper validation function for the `Calendar` component `required`, `min` and `max` attributes."""
    if condition:
        raise PydanticCustomError(
            "incorrect_mode",
            f"cannot be used {err_msg_word} `mode='single'`. Change 'mode' or remove attribute",
            dict(wrong_value=mode),
        )

    return val


def input_otp_num_groups_validation(num_groups: int, num_inputs: int) -> int:
    """A helper validation function for validating the `InputOtp.num_groups` attribute."""
    if num_groups > num_inputs:
        raise PydanticCustomError(
            "size_out_of_bounds",
            f"cannot have more groups ({num_groups}) than input slots ({num_inputs})\n",
            dict(wrong_value=num_groups, input_size=num_inputs),
        )

    return num_groups


def input_otp_pattern_validation(pattern: str) -> str:
    """A helper validation function for validating the `InputOtp.pattern` attribute."""
    if pattern not in InputOTPPatterns:
        try:
            re.compile(pattern)
        except re.error:
            official_patterns = [pattern.value for pattern in InputOTPPatterns]
            raise PydanticCustomError(
                "invalid_regex_pattern",
                f"must be an official pattern option ({official_patterns}) or a valid regex string\n",
                dict(wrong_value=pattern, official_patterns=official_patterns),
            )
    return pattern


def pagination_validation(links: list[str], max_size: int) -> list[str]:
    """A helper validation function for validating the `Pagination.links` attribute."""
    if len(links) > max_size:
        PydanticCustomError(
            "too_many_links",
            f"exceeds maximum link count ({max_size})",
            dict(wrong_value=links, count=len(links)),
        )
    return links


def radio_group_items_validation(items: list) -> list:
    """A helper validation function for validating the `RadioGroup.items` attribute."""
    if not items or len(items) == 0:
        raise PydanticCustomError(
            "missing_radio_button",
            "must have at least one 'RadioButton'",
            dict(wrong_value=items),
        )
    return items


def radio_group_default_value_validation(
    default_value: str, radio_buttons: list
) -> str:
    """A helper validation function for validating the `RadioGroup.default_value` attribute."""
    present = False

    if radio_buttons:
        for rb in radio_buttons:
            if rb.value == default_value:
                present = True
                break

        if not present:
            raise PydanticCustomError(
                "default_value_missing",
                f"""'value="{default_value}"' missing from 'items'. Provided -> \n    '{radio_buttons}'\n""",
                dict(wrong_value=default_value, items=radio_buttons),
            )

    return default_value


def slider_validation(size: int, min: int, max: int) -> int:
    """A helper validation function for validating the `Slider.bar_size` attribute."""
    if not (min <= size <= max):
        raise PydanticCustomError(
            "out_of_range",
            f"must be between '{min}' and '{max}'",
            dict(wrong_value=size, accepted_min=min, accepted_max=max),
        )
    return size


def ddm_radio_group_validation(values: list[str], texts: list[str]) -> list[str]:
    """A helper validation function for validating the `DDMRadioGroup.values` attribute."""
    if values is not None and len(texts) != len(values):
        raise PydanticCustomError(
            "size_mismatch",
            f"'texts' and 'values' must match in size -> 'texts={len(texts)} != values={len(values)}'\n",
            dict(texts_size=len(texts), values_size=len(values)),
        )
    return values


def aspect_ratio_validation(ratio: str | int) -> str | int:
    """A helper validation function for validating the `AspectRatio.ratio` attribute."""
    if isinstance(ratio, str):
        try:
            eval(ratio)
        except NameError as e:
            raise PydanticCustomError(
                "invalid_equation",
                f"ratio must be an 'integer' or a valid 'numeric equation' that results in an 'integer'\n  Equation error -> NameError: {e}\n",
                dict(wrong_value=ratio),
            )

    return ratio


def skeleton_validation(items: Optional[list], preset: str) -> Optional[list]:
    """A helper validation function for validating the `Skeleton.items` attribute."""
    if preset != "custom" and items is not None:
        raise PydanticCustomError(
            "invalid_preset",
            "cannot use 'items' without" + ' preset="custom"',
            dict(wrong_value=preset),
        )

    if preset == "custom" and items is None:
        raise PydanticCustomError(
            "missing_items",
            "missing 'items' with" + ' preset="custom"',
            dict(wrong_value=items),
        )

    return items
