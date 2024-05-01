import pytest

from tests.mappings.ui_imports import VALID_IMPORTS
from tests.mappings.ui_vals import VALID_VALS_MAP
from tests.templates.details import COMPONENT_DETAILS_MAPPING
from tests.templates.helper import SimpleCompBuilder

from zentra.ui.notification import Alert

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
