import pytest
from pydantic import ValidationError


from tests.templates.helper import SimpleCompBuilder
from tests.mappings.ui_imports import VALID_IMPORTS
from tests.mappings.ui_vals import VALID_VALS_MAP

from zentra.core import DataArray
from zentra.core.html import Div, FigCaption, Figure, HTMLContent
from zentra.core.js import Map

from zentra.core.react import LucideIconWithText
from zentra.nextjs import Image
from zentra.ui.control import (
    Calendar,
    Checkbox,
    Collapsible,
    Combobox,
    DatePicker,
    Input,
    InputOTP,
    Label,
    Pagination,
    RadioButton,
    RadioGroup,
    ScrollArea,
    Select,
    SelectGroup,
    Slider,
    Switch,
    Textarea,
    Toggle,
    ToggleGroup,
)
from zentra.ui.presentation import Separator


class TestCalendar:
    @pytest.fixture
    def calendar(self) -> Calendar:
        return Calendar(name="monthly")

    @pytest.fixture
    def calendar_long_name(self) -> Calendar:
        return Calendar(name="yearlyCalendar")

    @pytest.fixture
    def calendar_multi_mode(self) -> Calendar:
        return Calendar(
            name="monthly",
            mode="multiple",
            min=1,
            max=10,
        )

    @pytest.fixture
    def calendar_range_mode(self) -> Calendar:
        return Calendar(
            name="monthly",
            mode="range",
        )

    @pytest.fixture
    def wrapper(self, calendar: Calendar) -> SimpleCompBuilder:
        return SimpleCompBuilder(calendar)

    @pytest.fixture
    def wrapper_long(self, calendar_long_name: Calendar) -> SimpleCompBuilder:
        return SimpleCompBuilder(calendar_long_name)

    @pytest.fixture
    def wrapper_multi_mode(self, calendar_multi_mode: Calendar) -> SimpleCompBuilder:
        return SimpleCompBuilder(calendar_multi_mode)

    @pytest.fixture
    def wrapper_range_mode(self, calendar_range_mode: Calendar) -> SimpleCompBuilder:
        return SimpleCompBuilder(calendar_range_mode)

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
    def test_logic_str_multi_mode(wrapper_multi_mode: SimpleCompBuilder):
        wrapper_multi_mode.run("logic", VALID_VALS_MAP["calendar"]["logic"]["multiple"])

    @staticmethod
    def test_logic_str_range_mode(wrapper_range_mode: SimpleCompBuilder):
        wrapper_range_mode.run("logic", VALID_VALS_MAP["calendar"]["logic"]["range"])

    @staticmethod
    def test_import_str(wrapper: SimpleCompBuilder):
        wrapper.run("imports", VALID_IMPORTS["calendar"]["single"])

    @staticmethod
    def test_import_str_multi_mode(wrapper_multi_mode: SimpleCompBuilder):
        wrapper_multi_mode.run("imports", VALID_IMPORTS["calendar"]["multiple"])

    @staticmethod
    def test_import_str_range_mode(wrapper_range_mode: SimpleCompBuilder):
        wrapper_range_mode.run("imports", VALID_IMPORTS["calendar"]["range"])

    @staticmethod
    def test_content_str(wrapper: SimpleCompBuilder):
        wrapper.run("content", VALID_VALS_MAP["calendar"]["content"]["standard"])

    @staticmethod
    def test_content_str_multi_mode(wrapper_multi_mode: SimpleCompBuilder):
        wrapper_multi_mode.run(
            "content", VALID_VALS_MAP["calendar"]["content"]["multiple"]
        )

    @staticmethod
    def test_content_str_range_mode(wrapper_range_mode: SimpleCompBuilder):
        wrapper_range_mode.run(
            "content", VALID_VALS_MAP["calendar"]["content"]["range"]
        )

    @staticmethod
    def test_content_str_long_name(wrapper_long: SimpleCompBuilder):
        wrapper_long.run("content", VALID_VALS_MAP["calendar"]["content"]["long_name"])

    @staticmethod
    def test_content_str_single_all_attrs():
        calendar = Calendar(
            name="monthly",
            mode="single",
            styles=None,
            required=True,
            disable_nav=True,
            num_months=2,
            from_year=2023,
            to_year=2025,
            from_month=(2023, 1),
            to_month=(2025, 12),
            from_date=(2023, 1, 4),
            to_date=(2025, 12, 6),
        )
        builder = SimpleCompBuilder(calendar)
        builder.run(
            "content", VALID_VALS_MAP["calendar"]["content"]["single_all_attrs"]
        )

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

    @staticmethod
    def test_min_validation_error():
        with pytest.raises(ValidationError):
            Calendar(name="monthly", min=50)

    @staticmethod
    def test_max_validation_error():
        with pytest.raises(ValidationError):
            Calendar(name="monthly", max=50)

    @staticmethod
    def test_required_validation_error_mode_multiple():
        with pytest.raises(ValidationError):
            Calendar(name="monthly", mode="multiple", required=True)

    @staticmethod
    def test_required_validation_error_mode_range():
        with pytest.raises(ValidationError):
            Calendar(name="monthly", mode="range", required=True)


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
            text="Pretty please!",
        )

    @pytest.fixture
    def wrapper(self, checkbox: Checkbox) -> SimpleCompBuilder:
        return SimpleCompBuilder(checkbox)

    @pytest.fixture
    def wrapper_disabled(self, checkbox_with_disabled: Checkbox) -> SimpleCompBuilder:
        return SimpleCompBuilder(checkbox_with_disabled)

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
            title="@peduarte starred 3 repositories",
            items=["@radix-ui/primitives", "@radix-ui/colors", "@stitches/react"],
        )

    @pytest.fixture
    def wrapper(self, collapsible: Collapsible) -> SimpleCompBuilder:
        return SimpleCompBuilder(collapsible)

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
        return SimpleCompBuilder(input)

    @pytest.fixture
    def wrapper_disabled(self, input_with_disabled: Input) -> SimpleCompBuilder:
        return SimpleCompBuilder(input_with_disabled)

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
        return SimpleCompBuilder(input)

    @pytest.fixture
    def wrapper_pattern(self, input_pattern: InputOTP) -> SimpleCompBuilder:
        return SimpleCompBuilder(input_pattern)

    @pytest.fixture
    def wrapper_custom_pattern(
        self, input_custom_pattern: InputOTP
    ) -> SimpleCompBuilder:
        return SimpleCompBuilder(input_custom_pattern)

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
        return SimpleCompBuilder(label)

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


class TestPagination:
    @pytest.fixture
    def pagination_simple(self) -> Pagination:
        return Pagination(items_per_page=10, links=["#", "#", "#"])

    @pytest.fixture
    def pagination_full(self) -> Pagination:
        return Pagination(
            items_per_page=10, total_items=20, links=["#", "#", "#"], ellipsis=True
        )

    @pytest.fixture
    def wrapper_simple(self, pagination_simple: Pagination) -> SimpleCompBuilder:
        return SimpleCompBuilder(pagination_simple)

    @pytest.fixture
    def wrapper_full(self, pagination_full: Pagination) -> SimpleCompBuilder:
        return SimpleCompBuilder(pagination_full)

    @staticmethod
    def test_content_str_simple(wrapper_simple: SimpleCompBuilder):
        wrapper_simple.run("content", VALID_VALS_MAP["pagination"]["content"]["simple"])

    @staticmethod
    def test_content_str_full(wrapper_full: SimpleCompBuilder):
        wrapper_full.run("content", VALID_VALS_MAP["pagination"]["content"]["full"])

    @staticmethod
    def test_logic_str_simple(wrapper_simple: SimpleCompBuilder):
        wrapper_simple.run("logic", VALID_VALS_MAP["pagination"]["logic"]["simple"])

    @staticmethod
    def test_logic_str_full(wrapper_full: SimpleCompBuilder):
        wrapper_full.run("logic", VALID_VALS_MAP["pagination"]["logic"]["full"])

    @staticmethod
    def test_import_str_simple(wrapper_simple: SimpleCompBuilder):
        wrapper_simple.run("imports", VALID_IMPORTS["pagination"])


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
        return SimpleCompBuilder(radio_group)

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
                content=[
                    HTMLContent(
                        tag="h4",
                        styles="mb-4 text-sm font-medium leading-none",
                        text="Tags",
                    ),
                    Map(
                        obj_name="tags",
                        param_name="tag",
                        content=Div(
                            fragment=True,
                            content=[
                                Div(key="$.tag", styles="text-sm", content="$.tag"),
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
                content=Map(
                    obj_name="works",
                    param_name="artwork",
                    content=Figure(
                        key="$.artwork.artist",
                        styles="shrink-0",
                        img_container_styles="overflow-hidden rounded-md",
                        img=Image(
                            src="$.artwork.art",
                            alt="Photo by $.artwork.artist",
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
                                    text="$.artwork.artist",
                                ),
                            ],
                        ),
                    ),
                ),
            ),
            orientation="horizontal",
        )

    @pytest.fixture
    def wrapper(self, scroll_area: ScrollArea) -> SimpleCompBuilder:
        return SimpleCompBuilder(scroll_area)

    @pytest.fixture
    def wrapper_vertical(self, scroll_area_vertical: ScrollArea) -> SimpleCompBuilder:
        return SimpleCompBuilder(scroll_area_vertical)

    @pytest.fixture
    def wrapper_horizontal(
        self, scroll_area_horizontal: ScrollArea
    ) -> SimpleCompBuilder:
        return SimpleCompBuilder(scroll_area_horizontal)

    @staticmethod
    def test_content_str(wrapper: SimpleCompBuilder):
        wrapper.run("content", VALID_VALS_MAP["scroll_area"]["content"]["simple"])

    @staticmethod
    def test_content_str_vertical(wrapper_vertical: SimpleCompBuilder):
        wrapper_vertical.run(
            "content", VALID_VALS_MAP["scroll_area"]["content"]["vertical"]
        )

    @staticmethod
    def test_content_str_horizontal(wrapper_horizontal: SimpleCompBuilder):
        wrapper_horizontal.run(
            "content", VALID_VALS_MAP["scroll_area"]["content"]["horizontal"]
        )

    @staticmethod
    def test_imports_str(wrapper: SimpleCompBuilder):
        wrapper.run("imports", VALID_IMPORTS["scroll_area"]["simple"])

    @staticmethod
    def test_imports_str_vertical(wrapper_vertical: SimpleCompBuilder):
        wrapper_vertical.run("imports", VALID_IMPORTS["scroll_area"]["vertical"])

    @staticmethod
    def test_imports_str_horizontal(wrapper_horizontal: SimpleCompBuilder):
        wrapper_horizontal.run(
            "imports", VALID_IMPORTS["scroll_area"]["horizontal"], list_output=True
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
        return SimpleCompBuilder(select)

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
        return SimpleCompBuilder(slider)

    @pytest.fixture
    def wrapper_full(self, slider_full: Slider) -> SimpleCompBuilder:
        return SimpleCompBuilder(slider_full)

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
        return SimpleCompBuilder(switch)

    @staticmethod
    def test_content_str_simple(wrapper: SimpleCompBuilder):
        wrapper.run("content", VALID_VALS_MAP["switch"]["content"]["standard"])

    @staticmethod
    def test_content_str_checked():
        wrapper = SimpleCompBuilder(Switch(id="airplaneMode", checked=True))
        wrapper.run("content", VALID_VALS_MAP["switch"]["content"]["checked"])

    @staticmethod
    def test_content_str_disabled():
        wrapper = SimpleCompBuilder(Switch(id="airplaneMode", disabled=True))
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
        return SimpleCompBuilder(textarea)

    @staticmethod
    def test_content_str(wrapper: SimpleCompBuilder):
        wrapper.run("content", VALID_VALS_MAP["textarea"]["content"])

    @staticmethod
    def test_import_str(wrapper: SimpleCompBuilder):
        wrapper.run("imports", VALID_IMPORTS["textarea"])


class TestToggle:
    @pytest.fixture
    def toggle(self) -> Toggle:
        return Toggle(content="test $.text")

    @pytest.fixture
    def toggle_icon(self) -> Toggle:
        return Toggle(content=LucideIconWithText(name="italic", text="icon $.text"))

    @pytest.fixture
    def wrapper(self, toggle: Toggle) -> SimpleCompBuilder:
        return SimpleCompBuilder(toggle)

    @pytest.fixture
    def wrapper_icon(self, toggle_icon: Toggle) -> SimpleCompBuilder:
        return SimpleCompBuilder(toggle_icon)

    @pytest.fixture
    def wrapper_full(self) -> SimpleCompBuilder:
        return SimpleCompBuilder(
            Toggle(
                content="test $.text",
                style="outline",
                size="sm",
                variant="outline",
                pressed=True,
                disabled=True,
            )
        )

    @pytest.fixture
    def wrapper_icon_full(self) -> SimpleCompBuilder:
        return SimpleCompBuilder(
            Toggle(
                content=LucideIconWithText(
                    name="italic", text="icon $.text", position="end"
                ),
                style="bold",
                size="lg",
                disabled=True,
                pressed=True,
            )
        )

    @staticmethod
    def test_content_str(wrapper: SimpleCompBuilder):
        wrapper.run("content", VALID_VALS_MAP["toggle"]["content"]["simple"])

    @staticmethod
    def test_content_str_icon(wrapper_icon: SimpleCompBuilder):
        wrapper_icon.run("content", VALID_VALS_MAP["toggle"]["content"]["icon"])

    @staticmethod
    def test_content_str_full(wrapper_full: SimpleCompBuilder):
        wrapper_full.run("content", VALID_VALS_MAP["toggle"]["content"]["simple_full"])

    @staticmethod
    def test_content_str_icon_full(wrapper_icon_full: SimpleCompBuilder):
        wrapper_icon_full.run(
            "content", VALID_VALS_MAP["toggle"]["content"]["icon_full"]
        )

    @staticmethod
    def test_import_str(wrapper: SimpleCompBuilder):
        wrapper.run("imports", VALID_IMPORTS["toggle"]["simple"])

    @staticmethod
    def test_import_str_icon(wrapper_icon: SimpleCompBuilder):
        wrapper_icon.run("imports", VALID_IMPORTS["toggle"]["icon"])


class TestToggleGroup:
    @pytest.fixture
    def toggle_group(self) -> ToggleGroup:
        return ToggleGroup(
            items=[
                Toggle(
                    content=LucideIconWithText(name="italic"),
                ),
                Toggle(
                    content=LucideIconWithText(name="bold"),
                ),
                Toggle(
                    content=LucideIconWithText(name="underline"),
                ),
            ]
        )

    @pytest.fixture
    def toggle_group_full(self) -> ToggleGroup:
        return ToggleGroup(
            items=[
                Toggle(
                    content=LucideIconWithText(name="italic", text="italic $.text"),
                    pressed=True,
                ),
                Toggle(
                    content=LucideIconWithText(
                        name="bold", text="bold $.text", position="end"
                    ),
                    disabled=True,
                ),
                Toggle(
                    content=LucideIconWithText(
                        name="underline", text="undeline $.text"
                    ),
                ),
            ],
            type="single",
            disabled=True,
            size="lg",
            variant="outline",
            orientation="vertical",
        )

    @pytest.fixture
    def wrapper(self, toggle_group: ToggleGroup) -> SimpleCompBuilder:
        return SimpleCompBuilder(toggle_group)

    @pytest.fixture
    def wrapper_full(self, toggle_group_full: ToggleGroup) -> SimpleCompBuilder:
        return SimpleCompBuilder(toggle_group_full)

    @staticmethod
    def test_content_str(wrapper: SimpleCompBuilder):
        wrapper.run("content", VALID_VALS_MAP["toggle_group"]["content"]["simple"])

    @staticmethod
    def test_content_str_full(wrapper_full: SimpleCompBuilder):
        wrapper_full.run("content", VALID_VALS_MAP["toggle_group"]["content"]["full"])

    @staticmethod
    def test_import_str(wrapper: SimpleCompBuilder):
        wrapper.run("imports", VALID_IMPORTS["toggle_group"])


class TestDatePicker:
    @pytest.fixture
    def date_picker_single(self) -> DatePicker:
        return DatePicker(
            trigger="Pick a date",
            content=Calendar(name="datePicker"),
            styles="w-auto p-0",
        )

    @pytest.fixture
    def date_picker_multiple(self) -> DatePicker:
        return DatePicker(
            trigger="Pick a date",
            content=Calendar(name="datePicker", mode="multiple"),
            styles="w-auto p-0",
        )

    @pytest.fixture
    def date_picker_range(self) -> DatePicker:
        return DatePicker(
            trigger="Pick a date",
            content=Calendar(name="datePicker", mode="range"),
            styles="w-auto p-0",
        )

    @pytest.fixture
    def wrapper_single(self, date_picker_single: DatePicker) -> SimpleCompBuilder:
        return SimpleCompBuilder(date_picker_single)

    @pytest.fixture
    def wrapper_multiple(self, date_picker_multiple: DatePicker) -> SimpleCompBuilder:
        return SimpleCompBuilder(date_picker_multiple)

    @pytest.fixture
    def wrapper_range(self, date_picker_range: DatePicker) -> SimpleCompBuilder:
        return SimpleCompBuilder(date_picker_range)

    @staticmethod
    def test_content_str_single(wrapper_single: SimpleCompBuilder):
        wrapper_single.run(
            "content", VALID_VALS_MAP["date_picker"]["content"]["single"]
        )

    @staticmethod
    def test_content_str_multiple(wrapper_multiple: SimpleCompBuilder):
        wrapper_multiple.run(
            "content", VALID_VALS_MAP["date_picker"]["content"]["multiple"]
        )

    @staticmethod
    def test_content_str_range(wrapper_range: SimpleCompBuilder):
        wrapper_range.run("content", VALID_VALS_MAP["date_picker"]["content"]["range"])

    @staticmethod
    def test_logic_str_single(wrapper_single: SimpleCompBuilder):
        wrapper_single.run("logic", VALID_VALS_MAP["date_picker"]["logic"]["single"])

    @staticmethod
    def test_logic_str_multiple(wrapper_multiple: SimpleCompBuilder):
        wrapper_multiple.run(
            "logic", VALID_VALS_MAP["date_picker"]["logic"]["multiple"]
        )

    @staticmethod
    def test_logic_str_range(wrapper_range: SimpleCompBuilder):
        wrapper_range.run("logic", VALID_VALS_MAP["date_picker"]["logic"]["range"])

    @staticmethod
    def test_import_str_single(wrapper_single: SimpleCompBuilder):
        wrapper_single.run("imports", VALID_IMPORTS["date_picker"]["single"])

    @staticmethod
    def test_import_str_multiple(wrapper_multiple: SimpleCompBuilder):
        wrapper_multiple.run("imports", VALID_IMPORTS["date_picker"]["multiple"])

    @staticmethod
    def test_import_str_range(wrapper_range: SimpleCompBuilder):
        wrapper_range.run("imports", VALID_IMPORTS["date_picker"]["range"])


class TestCombobox:
    @pytest.fixture
    def combobox_simple(self) -> Combobox:
        return Combobox(
            data=DataArray(
                name="frameworks",
                type_name="FrameworkType",
                data=[{"value": "next.js", "label": "Next.js"}],
            ),
            display_text="Select framework...",
            search_text="Search framework...",
        )

    @pytest.fixture
    def combobox_custom(self) -> Combobox:
        return Combobox(
            data=DataArray(
                name="frameworks",
                type_name="FrameworkType",
                data=[
                    {"value": "next.js", "label": "Next.js"},
                    {"value": "sveltekit", "label": "SvelteKit"},
                    {"value": "nuxt.js", "label": "Nuxt.js"},
                    {"value": "remix", "label": "Remix"},
                    {"value": "astro", "label": "Astro"},
                ],
            ),
            display_text="Select framework...",
            search_text="Search framework...",
            hook_name="cb",
        )

    @pytest.fixture
    def wrapper_simple(self, combobox_simple: Combobox) -> SimpleCompBuilder:
        return SimpleCompBuilder(combobox_simple)

    @pytest.fixture
    def wrapper_custom(self, combobox_custom: Combobox) -> SimpleCompBuilder:
        return SimpleCompBuilder(combobox_custom)

    @staticmethod
    def test_content_str_simple(wrapper_simple: SimpleCompBuilder):
        wrapper_simple.run("content", VALID_VALS_MAP["combobox"]["content"]["simple"])

    @staticmethod
    def test_content_str_custom(wrapper_custom: SimpleCompBuilder):
        wrapper_custom.run("content", VALID_VALS_MAP["combobox"]["content"]["custom"])

    @staticmethod
    def test_logic_str_simple(wrapper_simple: SimpleCompBuilder):
        wrapper_simple.run("logic", VALID_VALS_MAP["combobox"]["logic"]["simple"])

    @staticmethod
    def test_logic_str_custom(wrapper_custom: SimpleCompBuilder):
        wrapper_custom.run("logic", VALID_VALS_MAP["combobox"]["logic"]["custom"])

    @staticmethod
    def test_import_str_simple(wrapper_simple: SimpleCompBuilder):
        wrapper_simple.run("imports", VALID_IMPORTS["combobox"])
