import pytest


from tests.mappings.ui_imports import VALID_IMPORTS
from tests.mappings.ui_vals import VALID_VALS_MAP
from tests.templates.helper import SimpleCompBuilder

from zentra_models.ui.control import Button
from zentra_models.ui.notification import Alert, AlertDialog

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


class TestAlertDialog:
    @pytest.fixture
    def alert_dialog_simple(self) -> AlertDialog:
        return AlertDialog(
            trigger=Button(variant="outline", content="Show Dialog"),
            title="Are you absolutely sure?",
            description="This action cannot be undone. This will permanently delete your account and remove your data from our servers.",
            cancel_btn="Cancel",
            action_btn="Continue",
        )

    @pytest.fixture
    def alert_dialog_no_buttons(self) -> AlertDialog:
        return AlertDialog(
            trigger=Button(variant="outline", content="Show Dialog"),
            title="Are you absolutely sure?",
            description="This action cannot be undone. This will permanently delete your account and remove your data from our servers.",
        )

    @pytest.fixture
    def alert_dialog_trigger_text(self) -> AlertDialog:
        return AlertDialog(trigger="Show Dialog", header="Are you absolutely sure?")

    @pytest.fixture
    def alert_dialog_text_content(self) -> AlertDialog:
        return AlertDialog(
            trigger=Button(variant="outline", content="Show Dialog"),
            header="Are you absolutely sure?",
            footer="This is a string footer.",
        )

    @pytest.fixture
    def wrapper_simple(self, alert_dialog_simple: AlertDialog) -> SimpleCompBuilder:
        return SimpleCompBuilder(alert_dialog_simple)

    @pytest.fixture
    def wrapper_no_buttons(
        self, alert_dialog_no_buttons: AlertDialog
    ) -> SimpleCompBuilder:
        return SimpleCompBuilder(alert_dialog_no_buttons)

    @pytest.fixture
    def wrapper_trigger_text(
        self, alert_dialog_trigger_text: AlertDialog
    ) -> SimpleCompBuilder:
        return SimpleCompBuilder(alert_dialog_trigger_text)

    @pytest.fixture
    def wrapper_text_content(
        self, alert_dialog_text_content: AlertDialog
    ) -> SimpleCompBuilder:
        return SimpleCompBuilder(alert_dialog_text_content)

    @staticmethod
    def test_content_str_simple(wrapper_simple: SimpleCompBuilder):
        wrapper_simple.run(
            "content", VALID_VALS_MAP["alert_dialog"]["content"]["simple"]
        )

    @staticmethod
    def test_content_str_no_buttons(wrapper_no_buttons: SimpleCompBuilder):
        wrapper_no_buttons.run(
            "content", VALID_VALS_MAP["alert_dialog"]["content"]["no_buttons"]
        )

    @staticmethod
    def test_content_str_trigger_text(wrapper_trigger_text: SimpleCompBuilder):
        wrapper_trigger_text.run(
            "content", VALID_VALS_MAP["alert_dialog"]["content"]["trigger_text"]
        )

    @staticmethod
    def test_content_str_text_content(wrapper_text_content: SimpleCompBuilder):
        wrapper_text_content.run(
            "content", VALID_VALS_MAP["alert_dialog"]["content"]["text_content"]
        )

    @staticmethod
    def test_logic_str_simple(wrapper_simple: SimpleCompBuilder):
        wrapper_simple.run("logic", VALID_VALS_MAP["alert_dialog"]["logic"]["simple"])

    @staticmethod
    def test_logic_str_no_buttons(wrapper_no_buttons: SimpleCompBuilder):
        wrapper_no_buttons.run(
            "logic", VALID_VALS_MAP["alert_dialog"]["logic"]["no_buttons"]
        )

    @staticmethod
    def test_logic_str_trigger_text(wrapper_trigger_text: SimpleCompBuilder):
        wrapper_trigger_text.run(
            "logic", VALID_VALS_MAP["alert_dialog"]["logic"]["trigger_text"]
        )

    @staticmethod
    def test_logic_str_text_content(wrapper_text_content: SimpleCompBuilder):
        wrapper_text_content.run(
            "logic", VALID_VALS_MAP["alert_dialog"]["logic"]["text_content"]
        )

    @staticmethod
    def test_import_str_simple(wrapper_simple: SimpleCompBuilder):
        wrapper_simple.run("imports", VALID_IMPORTS["alert_dialog"]["simple"])

    @staticmethod
    def test_import_str_no_buttons(wrapper_no_buttons: SimpleCompBuilder):
        wrapper_no_buttons.run("imports", VALID_IMPORTS["alert_dialog"]["no_buttons"])

    @staticmethod
    def test_import_str_trigger_text(wrapper_trigger_text: SimpleCompBuilder):
        wrapper_trigger_text.run(
            "imports", VALID_IMPORTS["alert_dialog"]["trigger_text"]
        )

    @staticmethod
    def test_import_str_text_content(wrapper_text_content: SimpleCompBuilder):
        wrapper_text_content.run(
            "imports", VALID_IMPORTS["alert_dialog"]["text_content"]
        )
