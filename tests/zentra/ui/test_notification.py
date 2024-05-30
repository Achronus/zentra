import pytest


from tests.mappings.ui_imports import VALID_IMPORTS
from tests.mappings.ui_vals import VALID_VALS_MAP
from tests.templates.helper import SimpleCompBuilder

from zentra.core.react import LucideIcon, LucideIconWithText
from zentra.ui.control import Button
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
            icon="terminal",
            title="Heads up!",
            description="You can add components to your app using the cli.",
        )

    @pytest.fixture
    def alert_full(self) -> Alert:
        return Alert(
            icon="circle-alert",
            title="Error",
            description="Your session has expired. Please log in again.",
            variant="destructive",
        )

    @pytest.fixture
    def wrapper(self, alert: Alert) -> SimpleCompBuilder:
        return SimpleCompBuilder(alert)

    @pytest.fixture
    def wrapper_icon(self, alert_icon: Alert) -> SimpleCompBuilder:
        return SimpleCompBuilder(alert_icon)

    @pytest.fixture
    def wrapper_full(self, alert_full: Alert) -> SimpleCompBuilder:
        return SimpleCompBuilder(alert_full)

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
        return SimpleCompBuilder(alert_dialog)

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
    def tooltip_str(self) -> Tooltip:
        return Tooltip(
            text="A cheeky label",
            trigger="Test tooltip",
        )

    @pytest.fixture
    def tooltip_icon(self) -> Tooltip:
        return Tooltip(
            text="Loading...",
            trigger=LucideIcon(name="loader", size=30),
        )

    @pytest.fixture
    def tooltip_icon_text(self) -> Tooltip:
        return Tooltip(
            text="Load me up!",
            trigger=LucideIconWithText(name="loader", text="Loading"),
        )

    @pytest.fixture
    def wrapper_btn(self, tooltip_btn: Tooltip) -> SimpleCompBuilder:
        return SimpleCompBuilder(tooltip_btn)

    @pytest.fixture
    def wrapper_str(self, tooltip_str: Tooltip) -> SimpleCompBuilder:
        return SimpleCompBuilder(tooltip_str)

    @pytest.fixture
    def wrapper_icon(self, tooltip_icon: Tooltip) -> SimpleCompBuilder:
        return SimpleCompBuilder(tooltip_icon)

    @pytest.fixture
    def wrapper_icon_text(self, tooltip_icon_text: Tooltip) -> SimpleCompBuilder:
        return SimpleCompBuilder(tooltip_icon_text)

    @staticmethod
    def test_content_str_btn(wrapper_btn: SimpleCompBuilder):
        wrapper_btn.run("content", VALID_VALS_MAP["tooltip"]["content"]["button"])

    @staticmethod
    def test_content_str_with_str(wrapper_str: SimpleCompBuilder):
        wrapper_str.run("content", VALID_VALS_MAP["tooltip"]["content"]["string"])

    @staticmethod
    def test_content_str_icon(wrapper_icon: SimpleCompBuilder):
        wrapper_icon.run("content", VALID_VALS_MAP["tooltip"]["content"]["icon"])

    @staticmethod
    def test_content_str_icon_text(wrapper_icon_text: SimpleCompBuilder):
        wrapper_icon_text.run(
            "content", VALID_VALS_MAP["tooltip"]["content"]["icon_text"]
        )

    @staticmethod
    def test_import_str_btn(wrapper_btn: SimpleCompBuilder):
        wrapper_btn.run("imports", VALID_IMPORTS["tooltip"]["button"])

    @staticmethod
    def test_import_str_with_str(wrapper_str: SimpleCompBuilder):
        wrapper_str.run("imports", VALID_IMPORTS["tooltip"]["string"])

    @staticmethod
    def test_import_str_icon(wrapper_icon: SimpleCompBuilder):
        wrapper_icon.run("imports", VALID_IMPORTS["tooltip"]["icon"])

    @staticmethod
    def test_import_str_icon_text(wrapper_icon_text: SimpleCompBuilder):
        wrapper_icon_text.run("imports", VALID_IMPORTS["tooltip"]["icon"])
