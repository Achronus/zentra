from functools import partial, reduce
from itertools import product
from operator import mul
from typing import Any

import pytest
from pydantic import ValidationError

from cli.conf.storage import ComponentDetails
from tests.templates.details import button_details, calendar_details
from tests.templates.dummy import DummyIconButton
from tests.templates.helper import component_builder
from tests.mappings.ui_attributes import BTN_VALID_ATTRS, ICON_BTN_VALID_ATTRS
from tests.mappings.ui_content import (
    BTN_VALID_CONTENT_WITH_LINK,
    BTN_VALID_CONTENT_WITHOUT_LINK,
    ICON_BTN_VALID_CONTENT_WITH_LINK,
    ICON_BTN_VALID_CONTENT_WITHOUT_LINK,
)
from tests.mappings.ui_imports import VALID_IMPORTS
from tests.mappings.ui_simple import (
    CALENDAR_VALID_VALS,
    CHECKBOX_VALID_VALS,
    COLLAPSIBLE_VALID_VALS,
    INPUT_VALID_VALS,
    INPUTOTP_VALID_VALS,
    LABEL_VALID_VALS,
)
from zentra.core import Component
from zentra.core.enums.ui import (
    ButtonIconPosition,
    ButtonSize,
    ButtonVariant,
    IconButtonSize,
)
from zentra.ui.control import (
    Button,
    Calendar,
    Checkbox,
    Collapsible,
    IconButton,
    Input,
    InputOTP,
    Label,
)


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


class ComponentFuncWrapper:
    """A helper class that handles the logic for keeping complicated component test implementations unified."""

    def __init__(
        self,
        iterable_dict: dict[list],
        component_func: callable,
        component_details: ComponentDetails,
    ) -> None:
        self.iterable_dict = iterable_dict
        self.details = component_details
        self.comp_func = component_func

    def dict_product(self, d: dict):
        keys = d.keys()
        values = d.values()
        return [dict(zip(keys, items)) for items in product(*values)]

    def run(self, result_attr: str, mapping: list[str] | dict[str, Any]):
        valid_total = 0
        items_list = self.dict_product(self.iterable_dict)
        desired_total = calc_valid_total(items_list)

        for idx, items in enumerate(items_list):
            component = self.comp_func(**items)
            builder = component_builder(component, self.details)
            builder.build()

            result = getattr(builder.storage, result_attr)

            map_value = mapping[idx] if isinstance(mapping, list) else mapping
            if result == map_value:
                valid_total += 1
            else:
                test_fail_result = result

        assert (
            valid_total == desired_total
        ), f"({valid_total}/{desired_total}) {test_fail_result} != {map_value}"


class SimpleComponentFuncWrapper:
    """A helper class that handles the logic for keeping simple component test implementations unified."""

    def __init__(
        self, component: Component, component_details: ComponentDetails
    ) -> None:
        self.component = component
        self.details = component_details

    def run(self, result_attr: str, valid_value: str):
        builder = component_builder(self.component, details=self.details)
        builder.build()

        result = getattr(builder.storage, result_attr)
        assert result == valid_value, (result, valid_value)


class TestButton:
    @staticmethod
    def button(**btn_kwargs) -> Button:
        return Button(**btn_kwargs)

    @pytest.fixture
    def iterables(self, example_btn_values) -> dict:
        return {
            "variant": example_btn_values["variants"],
            "size": example_btn_values["sizes"],
            "disabled": example_btn_values["disables"],
        }

    @pytest.fixture
    def btn(self, example_btn_values) -> partial:
        return partial(
            self.button,
            text=example_btn_values["text"],
        )

    @pytest.fixture
    def btn_with_url(self, example_btn_values) -> partial:
        return partial(
            self.button,
            text=example_btn_values["text"],
            url=example_btn_values["url"],
        )

    @pytest.fixture
    def btn_wrapper(self, iterables, btn) -> ComponentFuncWrapper:
        return ComponentFuncWrapper(
            iterable_dict=iterables,
            component_func=btn,
            component_details=button_details(),
        )

    @pytest.fixture
    def btn_wrapper_url(self, iterables, btn_with_url) -> ComponentFuncWrapper:
        return ComponentFuncWrapper(
            iterable_dict=iterables,
            component_func=btn_with_url,
            component_details=button_details(),
        )

    @staticmethod
    def test_attr_str(btn_wrapper_url: ComponentFuncWrapper):
        btn_wrapper_url.run(result_attr="attributes", mapping=BTN_VALID_ATTRS)

    @staticmethod
    def test_content_str(btn_wrapper: ComponentFuncWrapper):
        btn_wrapper.run(result_attr="content", mapping=BTN_VALID_CONTENT_WITHOUT_LINK)

    @staticmethod
    def test_content_str_with_url(btn_wrapper_url: ComponentFuncWrapper):
        btn_wrapper_url.run(result_attr="content", mapping=BTN_VALID_CONTENT_WITH_LINK)

    @staticmethod
    def test_import_str(btn_wrapper: ComponentFuncWrapper):
        btn_wrapper.run(result_attr="imports", mapping=VALID_IMPORTS["button"])

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
    @staticmethod
    def button(**btn_kwargs) -> DummyIconButton:
        return DummyIconButton(**btn_kwargs)

    @pytest.fixture
    def example_values(self, example_btn_values) -> dict:
        values = {
            "icon": "Loader",
            "icon_positions": [pos.value for pos in ButtonIconPosition],
            **example_btn_values,
        }
        values["size"] = [size.value for size in IconButtonSize]
        return values

    @pytest.fixture
    def iterables(self, example_values) -> dict:
        return {
            "icon_position": example_values["icon_positions"],
            "variant": example_values["variants"],
            "size": example_values["sizes"],
            "disabled": example_values["disables"],
        }

    @pytest.fixture
    def btn(self, example_values) -> partial:
        return partial(
            self.button,
            icon=example_values["icon"],
            text=example_values["text"],
        )

    @pytest.fixture
    def btn_with_url(self, example_values) -> partial:
        return partial(
            self.button,
            icon=example_values["icon"],
            text=example_values["text"],
            url=example_values["url"],
        )

    @pytest.fixture
    def btn_wrapper(self, iterables, btn) -> ComponentFuncWrapper:
        return ComponentFuncWrapper(
            iterable_dict=iterables,
            component_func=btn,
            component_details=button_details(),
        )

    @pytest.fixture
    def btn_wrapper_url(self, iterables, btn_with_url) -> ComponentFuncWrapper:
        return ComponentFuncWrapper(
            iterable_dict=iterables,
            component_func=btn_with_url,
            component_details=button_details(),
        )

    @staticmethod
    def test_attr_str(btn_wrapper_url: ComponentFuncWrapper):
        btn_wrapper_url.run(result_attr="attributes", mapping=ICON_BTN_VALID_ATTRS)

    @staticmethod
    def test_content_str(btn_wrapper: ComponentFuncWrapper):
        btn_wrapper.run(
            result_attr="content", mapping=ICON_BTN_VALID_CONTENT_WITHOUT_LINK
        )

    @staticmethod
    def test_content_str_with_url(btn_wrapper_url: ComponentFuncWrapper):
        btn_wrapper_url.run(
            result_attr="content", mapping=ICON_BTN_VALID_CONTENT_WITH_LINK
        )

    @staticmethod
    def test_import_str(btn_wrapper: ComponentFuncWrapper):
        btn_wrapper.run(
            result_attr="imports", mapping=VALID_IMPORTS["icon_button"]["standard"]
        )

    @staticmethod
    def test_import_str_with_url(btn_wrapper_url: ComponentFuncWrapper):
        btn_wrapper_url.run(
            result_attr="imports", mapping=VALID_IMPORTS["icon_button"]["with_url"]
        )

    @staticmethod
    def test_icon_empty():
        with pytest.raises(ValidationError):
            IconButton(icon="")

    @staticmethod
    def test_icon_str_invalid():
        with pytest.raises(ValidationError):
            IconButton(icon="loader is here")

    @staticmethod
    def test_invalid_variant():
        with pytest.raises(ValidationError):
            IconButton(icon="Loader", variant="test")

    @staticmethod
    def test_invalid_size():
        with pytest.raises(ValidationError):
            IconButton(icon="Loader", size="test")

    @staticmethod
    def test_invalid_url():
        with pytest.raises(ValidationError):
            IconButton(icon="Loader", url="not a url")


class TestCalendar:
    @pytest.fixture
    def calendar(self) -> Calendar:
        return Calendar(name="monthly")

    @pytest.fixture
    def calendar_long_name(self) -> Calendar:
        return Calendar(name="yearlyCalendar")

    @pytest.fixture
    def wrapper(self, calendar: Calendar) -> SimpleComponentFuncWrapper:
        return SimpleComponentFuncWrapper(calendar, calendar_details())

    @pytest.fixture
    def wrapper_long(self, calendar_long_name: Calendar) -> SimpleComponentFuncWrapper:
        return SimpleComponentFuncWrapper(calendar_long_name, calendar_details())

    @staticmethod
    def test_attr_str(wrapper: SimpleComponentFuncWrapper):
        wrapper.run("attributes", CALENDAR_VALID_VALS["attributes"]["standard"])

    @staticmethod
    def test_attr_str_long_name(wrapper_long: SimpleComponentFuncWrapper):
        wrapper_long.run("attributes", CALENDAR_VALID_VALS["attributes"]["long_name"])

    @staticmethod
    def test_logic_str(wrapper: SimpleComponentFuncWrapper):
        wrapper.run("logic", CALENDAR_VALID_VALS["logic"]["standard"])

    @staticmethod
    def test_logic_str_long_name(wrapper_long: SimpleComponentFuncWrapper):
        wrapper_long.run("logic", CALENDAR_VALID_VALS["logic"]["long_name"])

    @staticmethod
    def test_import_str(wrapper: SimpleComponentFuncWrapper):
        wrapper.run("imports", CALENDAR_VALID_VALS["imports"])

    @staticmethod
    def test_import_str_long_name(wrapper_long: SimpleComponentFuncWrapper):
        wrapper_long.run("imports", CALENDAR_VALID_VALS["imports"])

    @staticmethod
    def test_content_str(wrapper: SimpleComponentFuncWrapper):
        wrapper.run("content", CALENDAR_VALID_VALS["content"]["standard"])

    @staticmethod
    def test_content_str_long_name(wrapper_long: SimpleComponentFuncWrapper):
        wrapper_long.run("content", CALENDAR_VALID_VALS["content"]["long_name"])

    @staticmethod
    def test_id_validation_whitespace():
        with pytest.raises(ValidationError):
            Calendar(name="invalid id")

    @staticmethod
    def test_id_validation_dashes():
        with pytest.raises(ValidationError):
            Calendar(name="invalid-id")

    @staticmethod
    def test_id_validation_uppercase():
        with pytest.raises(ValidationError):
            Calendar(name="INVALID")

    @staticmethod
    def test_id_validation_capitalise():
        with pytest.raises(ValidationError):
            Calendar(name="Wrong")

    @staticmethod
    def test_id_validation_camelcase():
        Calendar(name="testCorrect")


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
    def test_import_str_valid(basic_checkbox: Checkbox):
        result = builder(basic_checkbox).import_statements
        valid = VALID_IMPORTS["checkbox"]
        assert result == valid, (valid, result)

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
    def test_import_str_valid(collapsible: Collapsible):
        result = builder(collapsible).import_statements
        valid = VALID_IMPORTS["collapsible"]
        assert result == valid, (valid, result)

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


class TestInput:
    @pytest.fixture
    def basic_input(self) -> Input:
        return Input(id="name", type="text", placeholder="Name")

    @pytest.fixture
    def input_with_disabled(self) -> Input:
        return Input(id="name", type="text", placeholder="Name", disabled=True)

    @staticmethod
    def test_attr_str_required(basic_input: Input):
        result = basic_input.attr_str()
        builder_result: str = builder(basic_input).attr_str

        valid = INPUT_VALID_VALS["attributes"]["required"]

        checks = all(
            [
                result == valid,
                builder_result.lstrip() == valid,
            ]
        )
        assert checks, (builder_result, result, valid)

    @staticmethod
    def test_attr_str_with_disabled(input_with_disabled: Input):
        result = input_with_disabled.attr_str()
        builder_result: str = builder(input_with_disabled).attr_str

        valid = INPUT_VALID_VALS["attributes"]["with_disabled"]

        checks = all(
            [
                result == valid,
                builder_result.lstrip() == valid,
            ]
        )
        assert checks, (builder_result, result, valid)

    @staticmethod
    def test_complete_jsx_valid(input_with_disabled: Input):
        result: str = builder(input_with_disabled).component_str
        valid = INPUT_VALID_VALS["full_jsx"]

        assert result == valid, (result, valid)

    @staticmethod
    def test_import_str_valid(basic_input: Input):
        result = builder(basic_input).import_statements
        valid = VALID_IMPORTS["input"]
        assert result == valid, (valid, result)

    @staticmethod
    def test_id_validation_whitespace():
        with pytest.raises(ValidationError):
            Input(id="name input", type="text", placeholder="Name", disabled=True)

    @staticmethod
    def test_id_validation_dashes():
        with pytest.raises(ValidationError):
            Input(id="name-input", type="text", placeholder="Name", disabled=True)

    @staticmethod
    def test_id_validation_uppercase():
        with pytest.raises(ValidationError):
            Input(id="NAME", type="text", placeholder="Name", disabled=True)

    @staticmethod
    def test_id_validation_capitalise():
        with pytest.raises(ValidationError):
            Input(id="Name", type="text", placeholder="Name", disabled=True)

    @staticmethod
    def test_id_validation_camelcase():
        Input(id="agencyName", type="text", placeholder="Name", disabled=True)


class TestInputOTP:
    @pytest.fixture
    def basic_input(self) -> InputOTP:
        return InputOTP(num_inputs=6, num_groups=2)

    @pytest.fixture
    def input_with_pattern(self) -> InputOTP:
        return InputOTP(num_inputs=6, num_groups=2, pattern="digits_n_chars_only")

    @staticmethod
    def test_attr_str_required(basic_input: InputOTP):
        result = basic_input.attr_str()
        builder_result: str = builder(basic_input).attr_str

        valid = INPUTOTP_VALID_VALS["attributes"]["required"]

        checks = all(
            [
                result == valid,
                builder_result.lstrip() == valid,
            ]
        )
        assert checks, (builder_result, result, valid)

    @staticmethod
    def test_attr_str_with_official_pattern(input_with_pattern: InputOTP):
        result = input_with_pattern.attr_str()
        builder_result: str = builder(input_with_pattern).attr_str

        valid = INPUTOTP_VALID_VALS["attributes"]["with_official_pattern"]

        checks = all(
            [
                result == valid,
                builder_result.lstrip() == valid,
            ]
        )
        assert checks, (builder_result, result, valid)

    @staticmethod
    def test_attr_str_with_custom_pattern():
        input_with_pattern = InputOTP(
            num_inputs=6, num_groups=2, pattern=r"([\^$.|?*+()\[\]{}])"
        )
        result = input_with_pattern.attr_str()
        builder_result: str = builder(input_with_pattern).attr_str

        valid = INPUTOTP_VALID_VALS["attributes"]["with_custom_pattern"]

        checks = all(
            [
                result == valid,
                builder_result.lstrip() == valid,
            ]
        )
        assert checks, (builder_result, result, valid)

    @staticmethod
    def test_content_str_one_group():
        input = InputOTP(num_inputs=6)
        result = input.content_str()
        builder_result: str = builder(input).content_str
        valid = INPUTOTP_VALID_VALS["content"]["one_group"]

        checks = all(
            [
                result == valid,
                builder_result == valid,
            ]
        )
        assert checks, (builder_result, result, valid)

    @staticmethod
    def test_content_str_two_groups(basic_input: InputOTP):
        result = basic_input.content_str()
        builder_result: str = builder(basic_input).content_str
        valid = INPUTOTP_VALID_VALS["content"]["two_groups"]

        checks = all(
            [
                result == valid,
                builder_result == valid,
            ]
        )
        assert checks, (builder_result, result, valid)

    @staticmethod
    def test_content_str_three_groups():
        input = InputOTP(num_inputs=6, num_groups=3)
        result = input.content_str()
        builder_result: str = builder(input).content_str
        valid = INPUTOTP_VALID_VALS["content"]["three_groups"]

        checks = all(
            [
                result == valid,
                builder_result == valid,
            ]
        )
        assert checks, (builder_result, result, valid)

    @staticmethod
    def test_complete_jsx_valid(input_with_pattern: InputOTP):
        result: str = builder(input_with_pattern).component_str
        valid = INPUTOTP_VALID_VALS["full_jsx"]

        assert result == valid, (result, valid)

    @staticmethod
    def test_import_str_required():
        input = InputOTP(num_inputs=6, num_groups=1)
        result = builder(input).import_statements
        valid = VALID_IMPORTS["input_otp"]["required"]
        assert result == valid, (valid, result)

    @staticmethod
    def test_import_str_with_official_pattern():
        input = InputOTP(num_inputs=6, num_groups=1, pattern="digits_only")
        result = builder(input).import_statements
        valid = VALID_IMPORTS["input_otp"]["with_pattern"]
        assert result == valid, (valid, result)

    @staticmethod
    def test_import_str_with_seperator(basic_input: InputOTP):
        result = builder(basic_input).import_statements
        valid = VALID_IMPORTS["input_otp"]["with_sep"]
        assert result == valid, (valid, result)

    @staticmethod
    def test_import_str_with_all(input_with_pattern: InputOTP):
        result = builder(input_with_pattern).import_statements
        valid = VALID_IMPORTS["input_otp"]["all"]
        assert result == valid, (valid, result)

    @staticmethod
    def test_num_groups_validation_error():
        with pytest.raises(ValidationError):
            InputOTP(num_inputs=3, num_groups=4)

    @staticmethod
    def test_pattern_validation_error():
        with pytest.raises(ValidationError):
            InputOTP(num_inputs=6, num_groups=2, pattern=r"[.*")


class TestLabel:
    @pytest.fixture
    def label(self) -> Label:
        return Label(id="terms", text="Accept terms and conditions.")

    @staticmethod
    def test_attr_str(label: Label):
        result = label.attr_str()
        builder_result: str = builder(label).attr_str

        valid = LABEL_VALID_VALS["attributes"]

        checks = all(
            [
                result == valid,
                builder_result.lstrip() == valid,
            ]
        )
        assert checks, (builder_result, result, valid)

    @staticmethod
    def test_content_str(label: Label):
        result = label.content_str()
        builder_result: str = builder(label).content_str
        valid = LABEL_VALID_VALS["content"]

        checks = all(
            [
                result == valid,
                builder_result == valid,
            ]
        )
        assert checks, (builder_result, result, valid)

    @staticmethod
    def test_complete_jsx_valid(label: Label):
        result: str = builder(label).component_str
        valid = LABEL_VALID_VALS["full_jsx"]

        assert result == valid, (result, valid)

    @staticmethod
    def test_import_str(label: Label):
        result = builder(label).import_statements
        valid = VALID_IMPORTS["label"]
        assert result == valid, (valid, result)

    @staticmethod
    def test_id_validation_whitespace():
        with pytest.raises(ValidationError):
            Label(id="terms conditions", text="Accept terms and conditions.")

    @staticmethod
    def test_id_validation_dashes():
        with pytest.raises(ValidationError):
            Label(id="terms-conditions", text="Accept terms and conditions.")

    @staticmethod
    def test_id_validation_uppercase():
        with pytest.raises(ValidationError):
            Label(id="TERMS", text="Accept terms and conditions.")

    @staticmethod
    def test_id_validation_capitalise():
        with pytest.raises(ValidationError):
            Label(id="Terms", text="Accept terms and conditions.")

    @staticmethod
    def test_id_validation_camelcase():
        Label(id="termsConditions", text="Accept terms and conditions.")
