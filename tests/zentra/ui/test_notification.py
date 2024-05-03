import pytest

from tests.mappings.ui_imports import VALID_IMPORTS
from tests.mappings.ui_vals import VALID_VALS_MAP
from tests.templates.details import COMPONENT_DETAILS_MAPPING
from tests.templates.helper import SimpleCompBuilder, ParentCompBuilder

from zentra.nextjs import Image
from zentra.ui.control import Button, Label
from zentra.ui.notification import Alert, TextAlertDialog, Tooltip

from pydantic import ValidationError


class TestAlert:
    @pytest.fixture
    def alert(self) -> Alert:
        return Alert(
            title="Heads up!",
            description="You can add components to your app using the cli.",
        )

    @pytest.fixture
    def alert_icon(self) -> Alert:
        return Alert(
            icon="Terminal",
            title="Heads up!",
            description="You can add components to your app using the cli.",
        )

    @pytest.fixture
    def alert_full(self) -> Alert:
        return Alert(
            icon="AlertCircle",
            title="Error",
            description="Your session has expired. Please log in again.",
            variant="destructive",
        )

    @pytest.fixture
    def wrapper(self, alert: Alert) -> SimpleCompBuilder:
        return SimpleCompBuilder(alert, COMPONENT_DETAILS_MAPPING["Alert"])

    @pytest.fixture
    def wrapper_icon(self, alert_icon: Alert) -> SimpleCompBuilder:
        return SimpleCompBuilder(alert_icon, COMPONENT_DETAILS_MAPPING["Alert"])

    @pytest.fixture
    def wrapper_full(self, alert_full: Alert) -> SimpleCompBuilder:
        return SimpleCompBuilder(alert_full, COMPONENT_DETAILS_MAPPING["Alert"])

    @staticmethod
    def test_content_str(wrapper: SimpleCompBuilder):
        wrapper.run("content", VALID_VALS_MAP["alert"]["content"]["simple"])

    @staticmethod
    def test_content_str_icon(wrapper_icon: SimpleCompBuilder):
        wrapper_icon.run("content", VALID_VALS_MAP["alert"]["content"]["icon"])

    @staticmethod
    def test_content_str_full(wrapper_full: SimpleCompBuilder):
        wrapper_full.run("content", VALID_VALS_MAP["alert"]["content"]["full"])

    @staticmethod
    def test_import_str(wrapper: SimpleCompBuilder):
        wrapper.run("imports", VALID_IMPORTS["alert"]["simple"])

    @staticmethod
    def test_import_str_icon(wrapper_icon: SimpleCompBuilder):
        wrapper_icon.run("imports", VALID_IMPORTS["alert"]["icon"])

    @staticmethod
    def test_icon_validation():
        with pytest.raises(ValidationError):
            Alert(title="test", description="test", icon="invalid icon")


class TestTextAlertDialog:
    @pytest.fixture
    def alert_dialog(self) -> TextAlertDialog:
        return TextAlertDialog(
            title="Are you absolutely sure?",
            description="This action cannot be undone. This will permanently delete your account and remove your data from our servers.",
            trigger_text="Delete Account",
        )

    @pytest.fixture
    def wrapper(self, alert_dialog: TextAlertDialog) -> SimpleCompBuilder:
        return SimpleCompBuilder(alert_dialog, COMPONENT_DETAILS_MAPPING["AlertDialog"])

    @staticmethod
    def test_content_str(wrapper: SimpleCompBuilder):
        wrapper.run("content", VALID_VALS_MAP["alert_dialog"]["content"]["simple"])

    @staticmethod
    def test_import_str(wrapper: SimpleCompBuilder):
        wrapper.run("imports", VALID_IMPORTS["alert_dialog"]["simple"])


class TestTooltip:
    @pytest.fixture
    def tooltip_btn(self) -> Tooltip:
        return Tooltip(
            text="Add to Library",
            trigger=Button(content="Hover", variant="outline"),
        )

    @pytest.fixture
    def tooltip_label(self) -> Tooltip:
        return Tooltip(
            text="A cheeky label",
            trigger=Label(name="library", text="UI Library"),
        )

    @pytest.fixture
    def tooltip_image(self) -> Tooltip:
        return Tooltip(
            text="A cool image",
            trigger=Image(src="/img.jpg", width=200, height=200, alt="A cool image"),
        )

    @pytest.fixture
    def wrapper_btn(self, tooltip_btn: Tooltip) -> ParentCompBuilder:
        return ParentCompBuilder(tooltip_btn)

    @pytest.fixture
    def wrapper_label(self, tooltip_label: Tooltip) -> ParentCompBuilder:
        return ParentCompBuilder(tooltip_label)

    @pytest.fixture
    def wrapper_image(self, tooltip_image: Tooltip) -> ParentCompBuilder:
        return ParentCompBuilder(tooltip_image)

    @staticmethod
    def test_content_str_btn(wrapper_btn: ParentCompBuilder):
        wrapper_btn.content(VALID_VALS_MAP["tooltip"]["content"]["button"])

    @staticmethod
    def test_content_str_label(wrapper_label: ParentCompBuilder):
        wrapper_label.content(VALID_VALS_MAP["tooltip"]["content"]["label"])

    @staticmethod
    def test_content_str_image(wrapper_image: ParentCompBuilder):
        wrapper_image.content(VALID_VALS_MAP["tooltip"]["content"]["image"])

    @staticmethod
    def test_import_str_btn(wrapper_btn: ParentCompBuilder):
        wrapper_btn.comp_other("imports", VALID_IMPORTS["tooltip"]["button"])

    @staticmethod
    def test_import_str_label(wrapper_label: ParentCompBuilder):
        wrapper_label.comp_other("imports", VALID_IMPORTS["tooltip"]["label"])

    @staticmethod
    def test_import_str_image(wrapper_image: ParentCompBuilder):
        wrapper_image.comp_other(
            "imports", VALID_IMPORTS["tooltip"]["image"], list_output=True
        )
