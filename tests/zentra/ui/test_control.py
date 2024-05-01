import pytest
from pydantic import ValidationError

from cli.conf.storage import ComponentDetails
from tests.templates.details import COMPONENT_DETAILS_MAPPING
from tests.templates.helper import component_builder, parent_component_builder

from tests.mappings.ui_imports import VALID_IMPORTS
from tests.mappings.ui_vals import VALID_VALS_MAP
from zentra.core import Component

from zentra.core.html import Div, FigCaption, Figure, HTMLContent
from zentra.core.js import Map

from zentra.core.react import LucideIcon
from zentra.nextjs import Image
from zentra.ui.control import (
    Calendar,
    Checkbox,
    Collapsible,
    Input,
    InputOTP,
    Label,
    RadioButton,
    RadioGroup,
    ScrollArea,
    Select,
    SelectGroup,
    Slider,
    Switch,
    Textarea,
    Toggle,
)
from zentra.ui.presentation import Separator


class SimpleCompBuilder:
    """A helper class that handles the logic for keeping simple component test implementations unified."""

    def __init__(
        self, component: Component, component_details: ComponentDetails
    ) -> None:
        self.component = component
        self.details = component_details

    def run(self, result_attr: str, valid_value: str):
        builder = component_builder(self.component, details=self.details)
        builder.build()

        result: str = getattr(builder.storage, result_attr)
        assert result == valid_value, (result.split("\n"), valid_value.split("\n"))


class ParentCompBuilder:
    """A helper class that handles the logic for keeping parent component test implementations unified."""

    def __init__(
        self,
        component: Component,
    ) -> None:
        self.component = component

        self.builder = parent_component_builder(component)

    def content(self, valid_value: str):
        result: list[str] = self.builder.build()
        assert "\n".join(result) == valid_value, (result, valid_value.split("\n"))

    def comp_other(self, result_attr: str, valid_value: str):
        _ = self.builder.build()
        result: list[str] = getattr(self.builder.storage, result_attr)
        assert "\n".join(result) == valid_value, (result, valid_value.split("\n"))


class TestCalendar:
    @pytest.fixture
    def calendar(self) -> Calendar:
        return Calendar(name="monthly")

    @pytest.fixture
    def calendar_long_name(self) -> Calendar:
        return Calendar(name="yearlyCalendar")

    @pytest.fixture
    def wrapper(self, calendar: Calendar) -> SimpleCompBuilder:
        return SimpleCompBuilder(calendar, COMPONENT_DETAILS_MAPPING["Calendar"])

    @pytest.fixture
    def wrapper_long(self, calendar_long_name: Calendar) -> SimpleCompBuilder:
        return SimpleCompBuilder(
            calendar_long_name, COMPONENT_DETAILS_MAPPING["Calendar"]
        )

    @staticmethod
    def test_attr_str(wrapper: SimpleCompBuilder):
        wrapper.run("attributes", VALID_VALS_MAP["calendar"]["attributes"]["standard"])

    @staticmethod
    def test_attr_str_long_name(wrapper_long: SimpleCompBuilder):
        wrapper_long.run(
            "attributes", VALID_VALS_MAP["calendar"]["attributes"]["long_name"]
        )

    @staticmethod
    def test_logic_str(wrapper: SimpleCompBuilder):
        wrapper.run("logic", VALID_VALS_MAP["calendar"]["logic"]["standard"])

    @staticmethod
    def test_logic_str_long_name(wrapper_long: SimpleCompBuilder):
        wrapper_long.run("logic", VALID_VALS_MAP["calendar"]["logic"]["long_name"])

    @staticmethod
    def test_import_str(wrapper: SimpleCompBuilder):
        wrapper.run("imports", VALID_IMPORTS["calendar"])

    @staticmethod
    def test_content_str(wrapper: SimpleCompBuilder):
        wrapper.run("content", VALID_VALS_MAP["calendar"]["content"]["standard"])

    @staticmethod
    def test_content_str_long_name(wrapper_long: SimpleCompBuilder):
        wrapper_long.run("content", VALID_VALS_MAP["calendar"]["content"]["long_name"])

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
    def wrapper(self, checkbox: Checkbox) -> SimpleCompBuilder:
        return SimpleCompBuilder(checkbox, COMPONENT_DETAILS_MAPPING["Checkbox"])

    @pytest.fixture
    def wrapper_disabled(self, checkbox_with_disabled: Checkbox) -> SimpleCompBuilder:
        return SimpleCompBuilder(
            checkbox_with_disabled, COMPONENT_DETAILS_MAPPING["Checkbox"]
        )

    @staticmethod
    def test_attr_str(wrapper: SimpleCompBuilder):
        wrapper.run("attributes", VALID_VALS_MAP["checkbox"]["attributes"]["standard"])

    @staticmethod
    def test_attr_str_disabled(wrapper_disabled: SimpleCompBuilder):
        wrapper_disabled.run(
            "attributes", VALID_VALS_MAP["checkbox"]["attributes"]["with_disabled"]
        )

    @staticmethod
    def test_import_str(wrapper: SimpleCompBuilder):
        wrapper.run("imports", VALID_IMPORTS["checkbox"])

    @staticmethod
    def test_content_str(wrapper: SimpleCompBuilder):
        wrapper.run("content", VALID_VALS_MAP["checkbox"]["content"]["standard"])

    @staticmethod
    def test_content_str_disabled(wrapper_disabled: SimpleCompBuilder):
        wrapper_disabled.run(
            "content", VALID_VALS_MAP["checkbox"]["content"]["with_disabled"]
        )

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
    def wrapper(self, collapsible: Collapsible) -> SimpleCompBuilder:
        return SimpleCompBuilder(collapsible, COMPONENT_DETAILS_MAPPING["Collapsible"])

    @staticmethod
    def test_attr_str(wrapper: SimpleCompBuilder):
        wrapper.run("attributes", VALID_VALS_MAP["collapsible"]["attributes"])

    @staticmethod
    def test_logic_str(wrapper: SimpleCompBuilder):
        wrapper.run("logic", VALID_VALS_MAP["collapsible"]["logic"])

    @staticmethod
    def test_import_str(wrapper: SimpleCompBuilder):
        wrapper.run("imports", VALID_IMPORTS["collapsible"])

    @staticmethod
    def test_content_str(wrapper: SimpleCompBuilder):
        wrapper.run("content", VALID_VALS_MAP["collapsible"]["content"])

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
    def wrapper(self, input: Input) -> SimpleCompBuilder:
        return SimpleCompBuilder(input, COMPONENT_DETAILS_MAPPING["Input"])

    @pytest.fixture
    def wrapper_disabled(self, input_with_disabled: Input) -> SimpleCompBuilder:
        return SimpleCompBuilder(
            input_with_disabled, COMPONENT_DETAILS_MAPPING["Input"]
        )

    @staticmethod
    def test_attr_str(wrapper: SimpleCompBuilder):
        wrapper.run("attributes", VALID_VALS_MAP["input"]["attributes"]["standard"])

    @staticmethod
    def test_attr_str_with_disabled(wrapper_disabled: SimpleCompBuilder):
        wrapper_disabled.run(
            "attributes", VALID_VALS_MAP["input"]["attributes"]["with_disabled"]
        )

    @staticmethod
    def test_import_str(wrapper: SimpleCompBuilder):
        wrapper.run("imports", VALID_IMPORTS["input"])

    @staticmethod
    def test_content_str(wrapper: SimpleCompBuilder):
        wrapper.run("content", VALID_VALS_MAP["input"]["content"]["standard"])

    @staticmethod
    def test_content_str_with_disabled(wrapper_disabled: SimpleCompBuilder):
        wrapper_disabled.run(
            "content", VALID_VALS_MAP["input"]["content"]["with_disabled"]
        )

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
    def wrapper(self, input: InputOTP) -> SimpleCompBuilder:
        return SimpleCompBuilder(input, COMPONENT_DETAILS_MAPPING["InputOtp"])

    @pytest.fixture
    def wrapper_pattern(self, input_pattern: InputOTP) -> SimpleCompBuilder:
        return SimpleCompBuilder(input_pattern, COMPONENT_DETAILS_MAPPING["InputOtp"])

    @pytest.fixture
    def wrapper_custom_pattern(
        self, input_custom_pattern: InputOTP
    ) -> SimpleCompBuilder:
        return SimpleCompBuilder(
            input_custom_pattern, COMPONENT_DETAILS_MAPPING["InputOtp"]
        )

    @staticmethod
    def test_attr_str(wrapper: SimpleCompBuilder):
        wrapper.run("attributes", VALID_VALS_MAP["input_otp"]["attributes"]["standard"])

    @staticmethod
    def test_attr_str_pattern(wrapper_pattern: SimpleCompBuilder):
        wrapper_pattern.run(
            "attributes", VALID_VALS_MAP["input_otp"]["attributes"]["pattern"]
        )

    @staticmethod
    def test_attr_str_custom_pattern(
        wrapper_custom_pattern: SimpleCompBuilder,
    ):
        wrapper_custom_pattern.run(
            "attributes", VALID_VALS_MAP["input_otp"]["attributes"]["custom_pattern"]
        )

    @staticmethod
    def test_content_str(wrapper: SimpleCompBuilder):
        wrapper.run("content", VALID_VALS_MAP["input_otp"]["content"]["one_group"])

    @staticmethod
    def test_content_str_pattern(wrapper_pattern: SimpleCompBuilder):
        wrapper_pattern.run(
            "content", VALID_VALS_MAP["input_otp"]["content"]["two_groups"]
        )

    @staticmethod
    def test_content_str_custom_pattern(
        wrapper_custom_pattern: SimpleCompBuilder,
    ):
        wrapper_custom_pattern.run(
            "content", VALID_VALS_MAP["input_otp"]["content"]["three_groups"]
        )

    @staticmethod
    def test_imports_str(wrapper: SimpleCompBuilder):
        wrapper.run("imports", VALID_IMPORTS["input_otp"]["standard"])

    @staticmethod
    def test_imports_str_pattern(wrapper_pattern: SimpleCompBuilder):
        wrapper_pattern.run("imports", VALID_IMPORTS["input_otp"]["pattern"])

    @staticmethod
    def test_imports_str_custom_pattern(
        wrapper_custom_pattern: SimpleCompBuilder,
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
    def wrapper(self, label: Label) -> SimpleCompBuilder:
        return SimpleCompBuilder(label, COMPONENT_DETAILS_MAPPING["Label"])

    @staticmethod
    def test_attr_str(wrapper: SimpleCompBuilder):
        wrapper.run("attributes", VALID_VALS_MAP["label"]["attributes"])

    @staticmethod
    def test_content_str(wrapper: SimpleCompBuilder):
        wrapper.run("content", VALID_VALS_MAP["label"]["content"])

    @staticmethod
    def test_imports_str(wrapper: SimpleCompBuilder):
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
    def wrapper(self, radio_group: RadioGroup) -> SimpleCompBuilder:
        return SimpleCompBuilder(radio_group, COMPONENT_DETAILS_MAPPING["RadioGroup"])

    @staticmethod
    def test_attr_str(wrapper: SimpleCompBuilder):
        wrapper.run("attributes", VALID_VALS_MAP["radio_group"]["attributes"])

    @staticmethod
    def test_content_str(wrapper: SimpleCompBuilder):
        wrapper.run("content", VALID_VALS_MAP["radio_group"]["content"])

    @staticmethod
    def test_imports_str(wrapper: SimpleCompBuilder):
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


class TestScrollArea:
    @pytest.fixture
    def scroll_area(self) -> ScrollArea:
        return ScrollArea(content="This is some text that is extremely simple.")

    @pytest.fixture
    def scroll_area_vertical(self) -> ScrollArea:
        return ScrollArea(
            styles="h-72 w-48 rounded-md border",
            content=Div(
                styles="p-4",
                items=[
                    HTMLContent(
                        tag="h4",
                        styles="mb-4 text-sm font-medium leading-none",
                        text="Tags",
                    ),
                    Map(
                        obj_name="tags",
                        param_name="tag",
                        content=Div(
                            shell=True,
                            items=[
                                Div(key="$tag", styles="text-sm", items="$tag"),
                                Separator(styles="my-2"),
                            ],
                        ),
                    ),
                ],
            ),
        )

    @pytest.fixture
    def scroll_area_horizontal(self) -> ScrollArea:
        return ScrollArea(
            styles="w-96 whitespace-nowrap rounded-md border",
            content=Div(
                styles="flex w-max space-x-4 p-4",
                items=Map(
                    obj_name="works",
                    param_name="artwork",
                    content=Figure(
                        key="$artwork.artist",
                        styles="shrink-0",
                        img_container_styles="overflow-hidden rounded-md",
                        img=Image(
                            src="$artwork.art",
                            alt="Photo by $artwork.artist",
                            styles="aspect-[3/4] h-fit w-fit object-cover",
                            width=300,
                            height=400,
                        ),
                        caption=FigCaption(
                            styles="pt-2 text-xs text-muted-foreground",
                            text=[
                                "Photo by ",
                                HTMLContent(
                                    tag="span",
                                    styles="font-semibold text-foreground",
                                    text="$artwork.artist",
                                ),
                            ],
                        ),
                    ),
                ),
            ),
            orientation="horizontal",
        )

    @pytest.fixture
    def wrapper(self, scroll_area: ScrollArea) -> ParentCompBuilder:
        return ParentCompBuilder(scroll_area)

    @pytest.fixture
    def wrapper_vertical(self, scroll_area_vertical: ScrollArea) -> ParentCompBuilder:
        return ParentCompBuilder(scroll_area_vertical)

    @pytest.fixture
    def wrapper_horizontal(
        self, scroll_area_horizontal: ScrollArea
    ) -> ParentCompBuilder:
        return ParentCompBuilder(scroll_area_horizontal)

    @staticmethod
    def test_content_str(wrapper: ParentCompBuilder):
        wrapper.content(VALID_VALS_MAP["scroll_area"]["content"]["simple"])

    @staticmethod
    def test_content_str_vertical(wrapper_vertical: ParentCompBuilder):
        wrapper_vertical.content(VALID_VALS_MAP["scroll_area"]["content"]["vertical"])

    @staticmethod
    def test_content_str_horizontal(wrapper_horizontal: ParentCompBuilder):
        wrapper_horizontal.content(
            VALID_VALS_MAP["scroll_area"]["content"]["horizontal"]
        )

    @staticmethod
    def test_imports_str(wrapper: ParentCompBuilder):
        wrapper.comp_other("imports", VALID_IMPORTS["scroll_area"]["simple"])

    @staticmethod
    def test_imports_str_vertical(wrapper_vertical: ParentCompBuilder):
        wrapper_vertical.comp_other("imports", VALID_IMPORTS["scroll_area"]["vertical"])

    @staticmethod
    def test_imports_str_horizontal(wrapper_horizontal: ParentCompBuilder):
        wrapper_horizontal.comp_other(
            "imports", VALID_IMPORTS["scroll_area"]["horizontal"]
        )


class TestSelect:
    @pytest.fixture
    def simple_select(self) -> Select:
        return Select(
            display_text="Select a fruit",
            groups=SelectGroup(
                label="Fruits",
                items=[
                    ("apple", "Apple"),
                    ("banana", "Banana"),
                ],
            ),
        )

    def wrapper(self, select: Select) -> SimpleCompBuilder:
        return SimpleCompBuilder(select, COMPONENT_DETAILS_MAPPING["Select"])

    def test_content_str_single_group(self, simple_select: Select):
        self.wrapper(simple_select).run(
            "content", VALID_VALS_MAP["select"]["content"]["single_group"]
        )

    def test_content_str_single_group_no_label(self):
        comp = Select(
            display_text="Select a fruit",
            groups=SelectGroup(
                label="Fruits",
                items=[
                    ("apple", "Apple"),
                    ("banana", "Banana"),
                ],
            ),
            show_label=False,
        )
        self.wrapper(comp).run(
            "content", VALID_VALS_MAP["select"]["content"]["single_group_no_label"]
        )

    def test_content_str_multi_groups(self):
        comp = Select(
            display_text="Select a fruit",
            groups=[
                SelectGroup(
                    label="Traditional",
                    items=[
                        ("apple", "Apple"),
                        ("banana", "Banana"),
                    ],
                ),
                SelectGroup(
                    label="Fancy",
                    items=[
                        ("blueberry", "Blueberry"),
                        ("pineapple", "Pineapple"),
                    ],
                ),
            ],
        )
        self.wrapper(comp).run(
            "content", VALID_VALS_MAP["select"]["content"]["multi_groups"]
        )

    def test_content_str_multi_groups_no_label(self):
        comp = Select(
            display_text="Select a fruit",
            groups=[
                SelectGroup(
                    label="Traditional",
                    items=[
                        ("apple", "Apple"),
                        ("banana", "Banana"),
                    ],
                ),
                SelectGroup(
                    label="Fancy",
                    items=[
                        ("blueberry", "Blueberry"),
                        ("pineapple", "Pineapple"),
                    ],
                ),
            ],
            show_label=False,
        )
        self.wrapper(comp).run(
            "content", VALID_VALS_MAP["select"]["content"]["multi_groups"]
        )

    def test_import_str(self, simple_select: Select):
        self.wrapper(simple_select).run("imports", VALID_IMPORTS["select"])


class TestSlider:
    @pytest.fixture
    def slider(self) -> Slider:
        return Slider(value=10)

    @pytest.fixture
    def slider_full(self) -> Slider:
        return Slider(
            value=10,
            min=1,
            max=50,
            bar_size=40,
            name="counts",
            disabled=True,
            orientation="vertical",
        )

    @pytest.fixture
    def wrapper(self, slider: Slider) -> SimpleCompBuilder:
        return SimpleCompBuilder(slider, COMPONENT_DETAILS_MAPPING["Slider"])

    @pytest.fixture
    def wrapper_full(self, slider_full: Slider) -> SimpleCompBuilder:
        return SimpleCompBuilder(slider_full, COMPONENT_DETAILS_MAPPING["Slider"])

    @staticmethod
    def test_content_str_simple(wrapper: SimpleCompBuilder):
        wrapper.run("content", VALID_VALS_MAP["slider"]["content"]["standard"])

    @staticmethod
    def test_content_str_full(wrapper_full: SimpleCompBuilder):
        wrapper_full.run("content", VALID_VALS_MAP["slider"]["content"]["all_params"])

    @staticmethod
    def test_import_str(wrapper: SimpleCompBuilder):
        wrapper.run("imports", VALID_IMPORTS["slider"])

    @staticmethod
    def test_name_validation_whitespace():
        with pytest.raises(ValidationError):
            Slider(value=10, name="terms conditions")

    @staticmethod
    def test_name_validation_dashes():
        with pytest.raises(ValidationError):
            Slider(value=10, name="terms-conditions")

    @staticmethod
    def test_name_validation_uppercase():
        with pytest.raises(ValidationError):
            Slider(value=10, name="TERMS")

    @staticmethod
    def test_name_validation_capitalise():
        with pytest.raises(ValidationError):
            Slider(value=10, name="Terms")

    @staticmethod
    def test_name_validation_camelcase():
        Slider(value=10, name="termsConditions")

    @staticmethod
    def test_bar_size_validation_under_zero():
        with pytest.raises(ValidationError):
            Slider(value=10, bar_size=-20)

    @staticmethod
    def test_bar_size_validation_over_100():
        with pytest.raises(ValidationError):
            Slider(value=10, bar_size=120)

    @staticmethod
    def test_bar_size_validation_valid_max():
        Slider(value=10, bar_size=100)

    @staticmethod
    def test_bar_size_validation_valid_min():
        Slider(value=10, bar_size=0)


class TestSwitch:
    @pytest.fixture
    def switch(self) -> Switch:
        return Switch(id="airplaneMode")

    @pytest.fixture
    def wrapper(self, switch: Switch) -> SimpleCompBuilder:
        return SimpleCompBuilder(switch, COMPONENT_DETAILS_MAPPING["Switch"])

    @staticmethod
    def test_content_str_simple(wrapper: SimpleCompBuilder):
        wrapper.run("content", VALID_VALS_MAP["switch"]["content"]["standard"])

    @staticmethod
    def test_content_str_checked():
        wrapper = SimpleCompBuilder(
            Switch(id="airplaneMode", checked=True),
            COMPONENT_DETAILS_MAPPING["Switch"],
        )
        wrapper.run("content", VALID_VALS_MAP["switch"]["content"]["checked"])

    @staticmethod
    def test_content_str_disabled():
        wrapper = SimpleCompBuilder(
            Switch(id="airplaneMode", disabled=True),
            COMPONENT_DETAILS_MAPPING["Switch"],
        )
        wrapper.run("content", VALID_VALS_MAP["switch"]["content"]["disabled"])

    @staticmethod
    def test_import_str(wrapper: SimpleCompBuilder):
        wrapper.run("imports", VALID_IMPORTS["switch"])

    @staticmethod
    def test_id_validation_whitespace():
        with pytest.raises(ValidationError):
            Switch(id="terms conditions")

    @staticmethod
    def test_id_validation_dashes():
        with pytest.raises(ValidationError):
            Switch(id="terms-conditions")

    @staticmethod
    def test_id_validation_uppercase():
        with pytest.raises(ValidationError):
            Switch(id="TERMS")

    @staticmethod
    def test_id_validation_capitalise():
        with pytest.raises(ValidationError):
            Switch(id="Terms")

    @staticmethod
    def test_id_validation_camelcase():
        Switch(id="termsConditions")


class TestTextarea:
    @pytest.fixture
    def textarea(self) -> Textarea:
        return Textarea(id="message", placeholder="Type your message here.")

    @pytest.fixture
    def wrapper(self, textarea: Textarea) -> SimpleCompBuilder:
        return SimpleCompBuilder(textarea, COMPONENT_DETAILS_MAPPING["Textarea"])

    @staticmethod
    def test_content_str(wrapper: SimpleCompBuilder):
        wrapper.run("content", VALID_VALS_MAP["textarea"]["content"])

    @staticmethod
    def test_import_str(wrapper: SimpleCompBuilder):
        wrapper.run("imports", VALID_IMPORTS["textarea"])


class TestToggle:
    @pytest.fixture
    def toggle(self) -> Toggle:
        return Toggle(content="test $text")

    @pytest.fixture
    def toggle_icon(self) -> Toggle:
        return Toggle(content=LucideIcon(name="Italic", text="icon $text"))

    @pytest.fixture
    def wrapper(self, toggle: Toggle) -> ParentCompBuilder:
        return ParentCompBuilder(toggle)

    @pytest.fixture
    def wrapper_icon(self, toggle_icon: Toggle) -> ParentCompBuilder:
        return ParentCompBuilder(toggle_icon)

    @pytest.fixture
    def wrapper_full(self) -> ParentCompBuilder:
        return ParentCompBuilder(
            Toggle(
                content="test $text",
                style="outline",
                size="sm",
                pressed=True,
                disabled=True,
            )
        )

    @pytest.fixture
    def wrapper_icon_full(self) -> ParentCompBuilder:
        return ParentCompBuilder(
            Toggle(
                content=LucideIcon(name="Italic", text="icon $text", position="end"),
                style="bold",
                size="icon",
                disabled=True,
                pressed=True,
            )
        )

    @staticmethod
    def test_content_str(wrapper: ParentCompBuilder):
        wrapper.content(VALID_VALS_MAP["toggle"]["content"]["simple"])

    @staticmethod
    def test_content_str_icon(wrapper_icon: ParentCompBuilder):
        wrapper_icon.content(VALID_VALS_MAP["toggle"]["content"]["icon"])

    @staticmethod
    def test_content_str_full(wrapper_full: ParentCompBuilder):
        wrapper_full.content(VALID_VALS_MAP["toggle"]["content"]["simple_full"])

    @staticmethod
    def test_content_str_icon_full(wrapper_icon_full: ParentCompBuilder):
        wrapper_icon_full.content(VALID_VALS_MAP["toggle"]["content"]["icon_full"])

    @staticmethod
    def test_import_str(wrapper: ParentCompBuilder):
        wrapper.comp_other("imports", VALID_IMPORTS["toggle"]["simple"])

    @staticmethod
    def test_import_str_icon(wrapper_icon: ParentCompBuilder):
        wrapper_icon.comp_other("imports", VALID_IMPORTS["toggle"]["icon"])
