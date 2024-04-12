from functools import partial, reduce
from itertools import product
from operator import mul
from typing import Any

import pytest
from pydantic import ValidationError

from cli.conf.storage import ComponentDetails
from tests.templates.details import COMPONENT_DETAILS_MAPPING
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
    RADIO_GROUP_VALID_VALS,
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
    RadioButton,
    RadioGroup,
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
        assert result == valid_value, (result.split("\n"), valid_value.split("\n"))


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
            component_details=COMPONENT_DETAILS_MAPPING["button"],
        )

    @pytest.fixture
    def btn_wrapper_url(self, iterables, btn_with_url) -> ComponentFuncWrapper:
        return ComponentFuncWrapper(
            iterable_dict=iterables,
            component_func=btn_with_url,
            component_details=COMPONENT_DETAILS_MAPPING["button"],
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
            component_details=COMPONENT_DETAILS_MAPPING["button"],
        )

    @pytest.fixture
    def btn_wrapper_url(self, iterables, btn_with_url) -> ComponentFuncWrapper:
        return ComponentFuncWrapper(
            iterable_dict=iterables,
            component_func=btn_with_url,
            component_details=COMPONENT_DETAILS_MAPPING["button"],
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
        return SimpleComponentFuncWrapper(
            calendar, COMPONENT_DETAILS_MAPPING["calendar"]
        )

    @pytest.fixture
    def wrapper_long(self, calendar_long_name: Calendar) -> SimpleComponentFuncWrapper:
        return SimpleComponentFuncWrapper(
            calendar_long_name, COMPONENT_DETAILS_MAPPING["calendar"]
        )

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
        wrapper.run("imports", VALID_IMPORTS["calendar"])

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
    def checkbox(self) -> Checkbox:
        return Checkbox(id="terms", label="Accept the terms and conditions.")

    @pytest.fixture
    def checkbox_with_disabled(self) -> Checkbox:
        return Checkbox(
            id="terms",
            label="Accept the terms and conditions.",
            disabled=True,
            more_info="Pretty please!",
        )

    @pytest.fixture
    def wrapper(self, checkbox: Checkbox) -> SimpleComponentFuncWrapper:
        return SimpleComponentFuncWrapper(
            checkbox, COMPONENT_DETAILS_MAPPING["checkbox"]
        )

    @pytest.fixture
    def wrapper_disabled(
        self, checkbox_with_disabled: Checkbox
    ) -> SimpleComponentFuncWrapper:
        return SimpleComponentFuncWrapper(
            checkbox_with_disabled, COMPONENT_DETAILS_MAPPING["checkbox"]
        )

    @staticmethod
    def test_attr_str(wrapper: SimpleComponentFuncWrapper):
        wrapper.run("attributes", CHECKBOX_VALID_VALS["attributes"]["standard"])

    @staticmethod
    def test_attr_str_disabled(wrapper_disabled: SimpleComponentFuncWrapper):
        wrapper_disabled.run(
            "attributes", CHECKBOX_VALID_VALS["attributes"]["with_disabled"]
        )

    @staticmethod
    def test_import_str(wrapper: SimpleComponentFuncWrapper):
        wrapper.run("imports", VALID_IMPORTS["checkbox"])

    @staticmethod
    def test_content_str(wrapper: SimpleComponentFuncWrapper):
        wrapper.run("content", CHECKBOX_VALID_VALS["content"]["standard"])

    @staticmethod
    def test_content_str_disabled(wrapper_disabled: SimpleComponentFuncWrapper):
        wrapper_disabled.run("content", CHECKBOX_VALID_VALS["content"]["with_disabled"])

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
            name="test",
            title="Starred repositories",
            items=["Astrum-AI/Zentra", "Not Zentra"],
        )

    @pytest.fixture
    def wrapper(self, collapsible: Collapsible) -> SimpleComponentFuncWrapper:
        return SimpleComponentFuncWrapper(
            collapsible, COMPONENT_DETAILS_MAPPING["collapsible"]
        )

    @staticmethod
    def test_attr_str(wrapper: SimpleComponentFuncWrapper):
        wrapper.run("attributes", COLLAPSIBLE_VALID_VALS["attributes"])

    @staticmethod
    def test_logic_str(wrapper: SimpleComponentFuncWrapper):
        wrapper.run("logic", COLLAPSIBLE_VALID_VALS["logic"])

    @staticmethod
    def test_import_str(wrapper: SimpleComponentFuncWrapper):
        wrapper.run("imports", VALID_IMPORTS["collapsible"])

    @staticmethod
    def test_content_str(wrapper: SimpleComponentFuncWrapper):
        wrapper.run("content", COLLAPSIBLE_VALID_VALS["content"])

    @staticmethod
    def test_id_validation_whitespace():
        with pytest.raises(ValidationError):
            Collapsible(
                name="invalid id",
                title="Starred repositories",
                items=["Astrum-AI/Zentra", "Not Zentra"],
            )

    @staticmethod
    def test_id_validation_dashes():
        with pytest.raises(ValidationError):
            Collapsible(
                name="invalid-id",
                title="Starred repositories",
                items=["Astrum-AI/Zentra", "Not Zentra"],
            )

    @staticmethod
    def test_id_validation_uppercase():
        with pytest.raises(ValidationError):
            Collapsible(
                name="INVALID",
                title="Starred repositories",
                items=["Astrum-AI/Zentra", "Not Zentra"],
            )

    @staticmethod
    def test_id_validation_capitalise():
        with pytest.raises(ValidationError):
            Collapsible(
                name="Wrong",
                title="Starred repositories",
                items=["Astrum-AI/Zentra", "Not Zentra"],
            )

    @staticmethod
    def test_id_validation_camelcase():
        Collapsible(
            name="testCorrect",
            title="Starred repositories",
            items=["Astrum-AI/Zentra", "Not Zentra"],
        )


class TestInput:
    @pytest.fixture
    def input(self) -> Input:
        return Input(id="name", type="text", placeholder="Name")

    @pytest.fixture
    def input_with_disabled(self) -> Input:
        return Input(id="name", type="text", placeholder="Name", disabled=True)

    @pytest.fixture
    def wrapper(self, input: Input) -> SimpleComponentFuncWrapper:
        return SimpleComponentFuncWrapper(input, COMPONENT_DETAILS_MAPPING["input"])

    @pytest.fixture
    def wrapper_disabled(
        self, input_with_disabled: Input
    ) -> SimpleComponentFuncWrapper:
        return SimpleComponentFuncWrapper(
            input_with_disabled, COMPONENT_DETAILS_MAPPING["input"]
        )

    @staticmethod
    def test_attr_str(wrapper: SimpleComponentFuncWrapper):
        wrapper.run("attributes", INPUT_VALID_VALS["attributes"]["standard"])

    @staticmethod
    def test_attr_str_with_disabled(wrapper_disabled: SimpleComponentFuncWrapper):
        wrapper_disabled.run(
            "attributes", INPUT_VALID_VALS["attributes"]["with_disabled"]
        )

    @staticmethod
    def test_import_str(wrapper: SimpleComponentFuncWrapper):
        wrapper.run("imports", VALID_IMPORTS["input"])

    @staticmethod
    def test_content_str(wrapper: SimpleComponentFuncWrapper):
        wrapper.run("content", INPUT_VALID_VALS["content"]["standard"])

    @staticmethod
    def test_content_str_with_disabled(wrapper_disabled: SimpleComponentFuncWrapper):
        wrapper_disabled.run("content", INPUT_VALID_VALS["content"]["with_disabled"])

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
    def input(self) -> InputOTP:
        return InputOTP(num_inputs=6, num_groups=1)

    @pytest.fixture
    def input_pattern(self) -> InputOTP:
        return InputOTP(num_inputs=6, num_groups=2, pattern="digits_n_chars_only")

    @pytest.fixture
    def input_custom_pattern(self) -> InputOTP:
        return InputOTP(num_inputs=6, num_groups=3, pattern=r"([\^$.|?*+()\[\]{}])")

    @pytest.fixture
    def wrapper(self, input: InputOTP) -> SimpleComponentFuncWrapper:
        return SimpleComponentFuncWrapper(input, COMPONENT_DETAILS_MAPPING["input_otp"])

    @pytest.fixture
    def wrapper_pattern(self, input_pattern: InputOTP) -> SimpleComponentFuncWrapper:
        return SimpleComponentFuncWrapper(
            input_pattern, COMPONENT_DETAILS_MAPPING["input_otp"]
        )

    @pytest.fixture
    def wrapper_custom_pattern(
        self, input_custom_pattern: InputOTP
    ) -> SimpleComponentFuncWrapper:
        return SimpleComponentFuncWrapper(
            input_custom_pattern, COMPONENT_DETAILS_MAPPING["input_otp"]
        )

    @staticmethod
    def test_attr_str(wrapper: SimpleComponentFuncWrapper):
        wrapper.run("attributes", INPUTOTP_VALID_VALS["attributes"]["standard"])

    @staticmethod
    def test_attr_str_pattern(wrapper_pattern: SimpleComponentFuncWrapper):
        wrapper_pattern.run("attributes", INPUTOTP_VALID_VALS["attributes"]["pattern"])

    @staticmethod
    def test_attr_str_custom_pattern(
        wrapper_custom_pattern: SimpleComponentFuncWrapper,
    ):
        wrapper_custom_pattern.run(
            "attributes", INPUTOTP_VALID_VALS["attributes"]["custom_pattern"]
        )

    @staticmethod
    def test_content_str(wrapper: SimpleComponentFuncWrapper):
        wrapper.run("content", INPUTOTP_VALID_VALS["content"]["one_group"])

    @staticmethod
    def test_content_str_pattern(wrapper_pattern: SimpleComponentFuncWrapper):
        wrapper_pattern.run("content", INPUTOTP_VALID_VALS["content"]["two_groups"])

    @staticmethod
    def test_content_str_custom_pattern(
        wrapper_custom_pattern: SimpleComponentFuncWrapper,
    ):
        wrapper_custom_pattern.run(
            "content", INPUTOTP_VALID_VALS["content"]["three_groups"]
        )

    @staticmethod
    def test_imports_str(wrapper: SimpleComponentFuncWrapper):
        wrapper.run("imports", VALID_IMPORTS["input_otp"]["standard"])

    @staticmethod
    def test_imports_str_pattern(wrapper_pattern: SimpleComponentFuncWrapper):
        wrapper_pattern.run("imports", VALID_IMPORTS["input_otp"]["pattern"])

    @staticmethod
    def test_imports_str_custom_pattern(
        wrapper_custom_pattern: SimpleComponentFuncWrapper,
    ):
        wrapper_custom_pattern.run(
            "imports", VALID_IMPORTS["input_otp"]["custom_pattern"]
        )

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
        return Label(name="terms", text="Accept terms and conditions.")

    @pytest.fixture
    def wrapper(self, label: Label) -> SimpleComponentFuncWrapper:
        return SimpleComponentFuncWrapper(label, COMPONENT_DETAILS_MAPPING["label"])

    @staticmethod
    def test_attr_str(wrapper: SimpleComponentFuncWrapper):
        wrapper.run("attributes", LABEL_VALID_VALS["attributes"])

    @staticmethod
    def test_content_str(wrapper: SimpleComponentFuncWrapper):
        wrapper.run("content", LABEL_VALID_VALS["content"])

    @staticmethod
    def test_imports_str(wrapper: SimpleComponentFuncWrapper):
        wrapper.run("imports", VALID_IMPORTS["label"])

    @staticmethod
    def test_name_validation_whitespace():
        with pytest.raises(ValidationError):
            Label(name="terms conditions", text="Accept terms and conditions.")

    @staticmethod
    def test_name_validation_dashes():
        with pytest.raises(ValidationError):
            Label(name="terms-conditions", text="Accept terms and conditions.")

    @staticmethod
    def test_name_validation_uppercase():
        with pytest.raises(ValidationError):
            Label(name="TERMS", text="Accept terms and conditions.")

    @staticmethod
    def test_name_validation_capitalise():
        with pytest.raises(ValidationError):
            Label(name="Terms", text="Accept terms and conditions.")

    @staticmethod
    def test_name_validation_camelcase():
        Label(name="termsConditions", text="Accept terms and conditions.")


class TestRadioGroup:
    @pytest.fixture
    def radio_group(self) -> RadioGroup:
        return RadioGroup(
            default_value="comfortable",
            items=[
                RadioButton(id="r1", value="default", text="Default"),
                RadioButton(id="r2", value="comfortable", text="Comfortable"),
                RadioButton(id="r3", value="compact", text="Compact"),
            ],
        )

    @pytest.fixture
    def wrapper(self, radio_group: RadioGroup) -> SimpleComponentFuncWrapper:
        return SimpleComponentFuncWrapper(
            radio_group, COMPONENT_DETAILS_MAPPING["radio_group"]
        )

    @staticmethod
    def test_attr_str(wrapper: SimpleComponentFuncWrapper):
        wrapper.run("attributes", RADIO_GROUP_VALID_VALS["attributes"])

    @staticmethod
    def test_content_str(wrapper: SimpleComponentFuncWrapper):
        wrapper.run("content", RADIO_GROUP_VALID_VALS["content"])

    @staticmethod
    def test_imports_str(wrapper: SimpleComponentFuncWrapper):
        wrapper.run("imports", VALID_IMPORTS["radio_group"])

    @staticmethod
    def test_items_validation_missing_radio_button():
        with pytest.raises(ValidationError):
            RadioGroup(default_value="comfortable", items=[])

    @staticmethod
    def test_items_validation_missing_parameter():
        with pytest.raises(ValidationError):
            RadioGroup(default_value="comfortable")

    @staticmethod
    def test_default_value_validation_dashed():
        with pytest.raises(ValidationError):
            RadioGroup(
                default_value="default-value",
                items=[RadioButton(id="r1", value="default", text="Default")],
            )

    @staticmethod
    def test_default_value_validation_uppercase():
        with pytest.raises(ValidationError):
            RadioGroup(
                default_value="DEFAULT",
                items=[RadioButton(id="r1", value="default", text="Default")],
            )

    @staticmethod
    def test_default_value_validation_capitalise():
        with pytest.raises(ValidationError):
            RadioGroup(
                default_value="Default",
                items=[RadioButton(id="r1", value="default", text="Default")],
            )

    @staticmethod
    def test_default_value_validation_camelcase():
        with pytest.raises(ValidationError):
            RadioGroup(
                default_value="defaultValue",
                items=[RadioButton(id="r1", value="default", text="Default")],
            )

    @staticmethod
    def test_default_value_validation_two_words():
        with pytest.raises(ValidationError):
            RadioGroup(
                default_value="default value",
                items=[RadioButton(id="r1", value="default", text="Default")],
            )

    @staticmethod
    def test_default_value_validation_missing_from_items():
        with pytest.raises(ValidationError):
            RadioGroup(
                default_value="comfortable",
                items=[RadioButton(id="r1", value="default", text="Default")],
            )
