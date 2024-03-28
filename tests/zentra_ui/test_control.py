from functools import reduce
from itertools import product
from operator import mul

import pytest
from pydantic import ValidationError

from tests.mappings.helper import builder
from tests.mappings.ui_attributes import BTN_VALID_ATTRS, ICON_BTN_VALID_ATTRS
from tests.mappings.ui_content import ICON_BTN_VALID_CONTENT
from tests.mappings.ui_simple import (
    CALENDAR_VALID_VALS,
    CHECKBOX_VALID_VALS,
    COLLAPSIBLE_VALID_VALS,
)
from zentra.core import Icon
from zentra.core.enums.ui import (
    ButtonIconPosition,
    ButtonSize,
    ButtonVariant,
    IconButtonSize,
)
from zentra.ui.control import Button, Calendar, Checkbox, Collapsible, IconButton


@pytest.fixture
def example_btn_values() -> dict:
    return {
        "text": "test",
        "url": "https://example.com/",
        "variants": [variant.value for variant in ButtonVariant],
        "sizes": [size.value for size in ButtonSize],
        "disables": [True, False],
    }


def calc_valid_total(*iterables) -> int:
    return reduce(mul, (len(iterable) for iterable in iterables))


class TestButton:
    @staticmethod
    def test_attr_str_valid(example_btn_values):
        variants = example_btn_values["variants"]
        sizes = example_btn_values["sizes"]
        disables = example_btn_values["disables"]

        valid_total = 0
        desired_total = calc_valid_total(variants, sizes, disables)

        for idx, (variant, size, disabled) in enumerate(
            product(variants, sizes, disables)
        ):
            btn = Button(
                text=example_btn_values["text"],
                url=example_btn_values["url"],
                variant=variant,
                size=size,
                disabled=disabled,
            )
            attr_str = btn.attr_str()
            result = builder(btn).attr_str

            if (attr_str == BTN_VALID_ATTRS[idx]) and (attr_str == result.lstrip()):
                valid_total += 1
            else:
                test_fail_example = attr_str
                test_fail_result = result

        assert (
            valid_total == desired_total
        ), f"({valid_total}/{desired_total}) ({test_fail_example}, {test_fail_result})"

    @staticmethod
    def test_content_str_valid():
        btn = Button(text="test")

        content_str = btn.content_str()
        result = builder(btn).content_str

        assert content_str == result, (result, content_str)

    @staticmethod
    def test_text_empty_str():
        with pytest.raises(ValidationError):
            Button(text="")

    @staticmethod
    def test_invalid_variant():
        with pytest.raises(ValidationError):
            Button(text="test", variant="test")

    @staticmethod
    def test_invalid_size():
        with pytest.raises(ValidationError):
            Button(text="test", size="test")

    @staticmethod
    def test_invalid_url():
        with pytest.raises(ValidationError):
            Button(text="test", url="not a url")


class TestIconButton:
    @pytest.fixture
    def example_values(self, example_btn_values) -> dict:
        values = {
            "icon": Icon(name="test"),
            "icon_positions": [pos.value for pos in ButtonIconPosition],
            **example_btn_values,
        }
        values["size"] = [size.value for size in IconButtonSize]
        return values

    @staticmethod
    def test_attr_str_valid(example_values):
        icon_positions = example_values["icon_positions"]
        variants = example_values["variants"]
        sizes = example_values["sizes"]
        disables = example_values["disables"]

        valid_total = 0
        desired_total = calc_valid_total(icon_positions, variants, sizes, disables)

        for idx, (position, variant, size, disabled) in enumerate(
            product(icon_positions, variants, sizes, disables)
        ):
            btn = IconButton(
                icon=example_values["icon"],
                icon_position=position,
                text=example_values["text"],
                url=example_values["url"],
                variant=variant,
                size=size,
                disabled=disabled,
            )
            attr_str = btn.attr_str()
            result = builder(btn).attr_str

            if (attr_str == ICON_BTN_VALID_ATTRS[idx]) and (
                attr_str == result.lstrip()
            ):
                valid_total += 1

        assert valid_total == desired_total, f"{valid_total}/{desired_total}"

    @staticmethod
    def test_content_str_valid(example_values):
        positions = example_values["icon_positions"]

        valid_total = 0
        desired_total = len(positions)

        for idx, position in enumerate(positions):
            btn = IconButton(
                icon=example_values["icon"],
                icon_position=position,
                text=example_values["text"],
            )
            content_str = btn.content_str()
            result = builder(btn).content_str

            if (content_str == ICON_BTN_VALID_CONTENT[idx]) and (content_str == result):
                valid_total += 1

        assert valid_total == desired_total, f"{valid_total}/{desired_total}"

    @staticmethod
    def test_icon_empty():
        with pytest.raises(ValidationError):
            IconButton(icon="")

    @staticmethod
    def test_invalid_variant():
        with pytest.raises(ValidationError):
            IconButton(icon=Icon(name="test"), variant="test")

    @staticmethod
    def test_invalid_size():
        with pytest.raises(ValidationError):
            IconButton(icon=Icon(name="test"), size="test")

    @staticmethod
    def test_invalid_url():
        with pytest.raises(ValidationError):
            IconButton(icon=Icon(name="test"), url="not a url")


class TestCalendar:
    @pytest.fixture
    def calendar(self) -> Calendar:
        return Calendar(id="test")

    @staticmethod
    def test_attr_str_valid(calendar: Calendar):
        result = calendar.attr_str()
        builder_result: str = builder(calendar).attr_str

        valid = CALENDAR_VALID_VALS["attributes"]

        checks = all(
            [
                result == valid,
                builder_result.lstrip() == valid,
            ]
        )
        assert checks, (result, valid)

    @staticmethod
    def test_unique_logic_str_valid(calendar: Calendar):
        result = calendar.unique_logic_str()
        builder_result = builder(calendar).unique_logic_str

        valid = CALENDAR_VALID_VALS["unique_logic"]

        checks = all(
            [
                result == valid,
                builder_result == valid,
            ]
        )
        assert checks, (result, valid)

    @staticmethod
    def test_id_validation_whitespace():
        with pytest.raises(ValidationError):
            Calendar(id="invalid id")

    @staticmethod
    def test_id_validation_dashes():
        with pytest.raises(ValidationError):
            Calendar(id="invalid-id")

    @staticmethod
    def test_id_validation_uppercase():
        with pytest.raises(ValidationError):
            Calendar(id="INVALID")

    @staticmethod
    def test_id_validation_capitalise():
        with pytest.raises(ValidationError):
            Calendar(id="Wrong")

    @staticmethod
    def test_id_validation_camelcase():
        Calendar(id="testCorrect")


class TestCheckbox:
    @pytest.fixture
    def basic_checkbox(self) -> Checkbox:
        return Checkbox(id="terms", label="Accept the terms and conditions.")

    @pytest.fixture
    def checkbox_with_disabled(self) -> Checkbox:
        return Checkbox(
            id="terms",
            label="Accept the terms and conditions.",
            disabled=True,
            more_info="Pretty please!",
        )

    @staticmethod
    def test_attr_str_required(basic_checkbox: Checkbox):
        result = basic_checkbox.attr_str()
        builder_result: str = builder(basic_checkbox).attr_str

        valid = CHECKBOX_VALID_VALS["attributes"]["required"]

        checks = all(
            [
                result == valid,
                builder_result.lstrip() == valid,
            ]
        )
        assert checks, (builder_result, result, valid)

    @staticmethod
    def test_attr_str_with_disabled(checkbox_with_disabled: Checkbox):
        result = checkbox_with_disabled.attr_str()
        builder_result: str = builder(checkbox_with_disabled).attr_str

        valid = CHECKBOX_VALID_VALS["attributes"]["with_disabled"]

        checks = all(
            [
                result == valid,
                builder_result.lstrip() == valid,
            ]
        )
        assert checks, (builder_result, result, valid)

    @staticmethod
    def test_below_content_str_required(basic_checkbox: Checkbox):
        result = basic_checkbox.below_content_str()
        builder_result: str = builder(basic_checkbox).below_content_str

        valid = CHECKBOX_VALID_VALS["below_content"]["required"]

        checks = all(
            [
                result == valid,
                builder_result == valid,
            ]
        )
        assert checks, (builder_result, result, valid)

    @staticmethod
    def test_below_content_str_with_optionals(checkbox_with_disabled: Checkbox):
        result = checkbox_with_disabled.below_content_str()
        builder_result: str = builder(checkbox_with_disabled).below_content_str

        valid = CHECKBOX_VALID_VALS["below_content"]["with_optionals"]

        checks = all(
            [
                result == valid,
                builder_result == valid,
            ]
        )
        assert checks, (builder_result, result, valid)

    @staticmethod
    def test_complete_jsx_valid(checkbox_with_disabled: Checkbox):
        result: str = builder(checkbox_with_disabled).component_str
        valid = CHECKBOX_VALID_VALS["full_jsx"]

        assert result == valid, (result, valid)

    @staticmethod
    def test_id_validation_whitespace():
        with pytest.raises(ValidationError):
            Checkbox(id="invalid id", label="test")

    @staticmethod
    def test_id_validation_dashes():
        with pytest.raises(ValidationError):
            Checkbox(id="invalid-id", label="test")

    @staticmethod
    def test_id_validation_uppercase():
        with pytest.raises(ValidationError):
            Checkbox(id="INVALID", label="test")

    @staticmethod
    def test_id_validation_capitalise():
        with pytest.raises(ValidationError):
            Checkbox(id="Wrong", label="test")

    @staticmethod
    def test_id_validation_camelcase():
        Checkbox(id="testCorrect", label="test")


class TestCollapsible:
    @pytest.fixture
    def collapsible(self) -> Collapsible:
        return Collapsible(
            id="test",
            title="Starred repositories",
            items=["Astrum-AI/Zentra", "Not Zentra"],
        )

    @staticmethod
    def test_logic_str(collapsible: Collapsible):
        result = collapsible.unique_logic_str()
        builder_result: str = builder(collapsible).unique_logic_str
        valid = COLLAPSIBLE_VALID_VALS["unique_logic"]

        checks = all(
            [
                result == valid,
                builder_result == valid,
            ]
        )
        assert checks, (builder_result, result, valid)

    @staticmethod
    def test_attr_str(collapsible: Collapsible):
        result = collapsible.attr_str()
        builder_result: str = builder(collapsible).attr_str
        valid = COLLAPSIBLE_VALID_VALS["attributes"]

        checks = all(
            [
                result == valid,
                builder_result.lstrip() == valid,
            ]
        )
        assert checks, (builder_result, result, valid)

    @staticmethod
    def test_content_str(collapsible: Collapsible):
        result = collapsible.content_str()
        builder_result: str = builder(collapsible).content_str
        valid = COLLAPSIBLE_VALID_VALS["content"]

        checks = all(
            [
                result == valid,
                builder_result == valid,
            ]
        )
        assert checks, (builder_result, result, valid)

    @staticmethod
    def test_complete_jsx_valid(collapsible: Collapsible):
        result: str = builder(collapsible).component_str
        valid = COLLAPSIBLE_VALID_VALS["full_jsx"]

        assert result == valid, (result, valid)

    @staticmethod
    def test_id_validation_whitespace():
        with pytest.raises(ValidationError):
            Collapsible(
                id="invalid id",
                title="Starred repositories",
                items=["Astrum-AI/Zentra", "Not Zentra"],
            )

    @staticmethod
    def test_id_validation_dashes():
        with pytest.raises(ValidationError):
            Collapsible(
                id="invalid-id",
                title="Starred repositories",
                items=["Astrum-AI/Zentra", "Not Zentra"],
            )

    @staticmethod
    def test_id_validation_uppercase():
        with pytest.raises(ValidationError):
            Collapsible(
                id="INVALID",
                title="Starred repositories",
                items=["Astrum-AI/Zentra", "Not Zentra"],
            )

    @staticmethod
    def test_id_validation_capitalise():
        with pytest.raises(ValidationError):
            Collapsible(
                id="Wrong",
                title="Starred repositories",
                items=["Astrum-AI/Zentra", "Not Zentra"],
            )

    @staticmethod
    def test_id_validation_camelcase():
        Collapsible(
            id="testCorrect",
            title="Starred repositories",
            items=["Astrum-AI/Zentra", "Not Zentra"],
        )
