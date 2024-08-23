import pytest
from unittest.mock import MagicMock

from rich.console import Console
from rich.panel import Panel

from zentra_sdk.cli.constants.message import MSG_MAPPER, MessageHandler
from zentra_sdk.cli.constants import CommonErrorCodes, SetupSuccessCodes


UNKNOWN_ERROR = "We didn't account for this!"


@pytest.fixture
def console() -> Console:
    return Console()


@pytest.fixture
def msg_mapper() -> dict:
    return MSG_MAPPER


class TestMessageHandler:
    @pytest.fixture
    def message_handler(self, console, msg_mapper) -> MessageHandler:
        return MessageHandler(console=console, msg_mapper=msg_mapper)

    @staticmethod
    def test_msg_success(message_handler: MessageHandler, console: Console):
        console.print = MagicMock()
        exit_code = MagicMock(exit_code=SetupSuccessCodes.TEST_SUCCESS)

        message_handler.msg(exit_code)

        console.print.assert_called_once()
        panel = console.print.call_args[0][0]
        assert isinstance(panel, Panel)
        assert "Test" in panel.renderable
        assert panel.border_style == "bright_green"

    @staticmethod
    def test_msg_error(message_handler: MessageHandler, console: Console):
        console.print = MagicMock()
        exit_code = MagicMock(exit_code=CommonErrorCodes.TEST_ERROR)

        message_handler.msg(exit_code)

        console.print.assert_called_once()
        panel = console.print.call_args[0][0]
        assert isinstance(panel, Panel)
        assert "Test" in panel.renderable
        assert panel.border_style == "bright_red"

    @staticmethod
    def test_msg_unknown_error(message_handler: MessageHandler, console: Console):
        console.print = MagicMock()
        exit_code = MagicMock(exit_code=CommonErrorCodes.UNKNOWN_ERROR)
        message_handler.msg(exit_code)

        console.print.assert_called_once()
        panel = console.print.call_args[0][0]
        assert isinstance(panel, Panel)
        assert UNKNOWN_ERROR in panel.renderable
        assert panel.border_style == "bright_red"

    @staticmethod
    def test_msg_empty_message(message_handler: MessageHandler, console: Console):
        console.print = MagicMock()
        exit_code = MagicMock(exit_code=CommonErrorCodes.UNKNOWN_ERROR)
        message_handler.msg(exit_code)

        console.print.assert_called_once()
        panel = console.print.call_args[0][0]
        assert isinstance(panel, Panel)
        assert UNKNOWN_ERROR in panel.renderable
        assert panel.border_style == "bright_red"
