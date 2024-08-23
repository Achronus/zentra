import pytest
import logging
from unittest import mock

from zentra_sdk.cli.conf.logger import (
    BaseLogger,
    DebugLogger,
    set_loggers,
    ErrorLoggers,
)


class TestBaseLogger:
    @pytest.fixture
    def base_logger(self) -> BaseLogger:
        return BaseLogger(logger_name="test_logger")

    @staticmethod
    def test_console_handler(base_logger: BaseLogger):
        base_logger.console_handler(level=logging.DEBUG, format="%(message)s")

        assert len(base_logger.logger.handlers) == 1
        handler = base_logger.logger.handlers[0]
        assert isinstance(handler, logging.StreamHandler)
        assert handler.level == logging.DEBUG
        assert isinstance(handler.formatter, logging.Formatter)
        assert handler.formatter._fmt == "%(message)s"

    @staticmethod
    def test_file_handler(base_logger: BaseLogger, tmp_path):
        log_filepath = tmp_path / "test.log"
        base_logger.file_handler(
            log_filepath=str(log_filepath),
            level=logging.ERROR,
            format="%(asctime)s | %(levelname)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        assert len(base_logger.logger.handlers) == 2
        handler = base_logger.logger.handlers[-1]
        assert isinstance(handler, logging.FileHandler)
        assert handler.level == logging.ERROR
        assert isinstance(handler.formatter, logging.Formatter)
        assert handler.formatter._fmt == "%(asctime)s | %(levelname)s | %(message)s"
        assert handler.formatter.datefmt == "%Y-%m-%d %H:%M:%S"

    @staticmethod
    def test_log_methods(base_logger: BaseLogger):
        with mock.patch("logging.Logger.debug") as mock_debug:
            base_logger.debug("Debug message")
            mock_debug.assert_called_once_with("Debug message")

        with mock.patch("logging.Logger.info") as mock_info:
            base_logger.info("Info message")
            mock_info.assert_called_once_with("Info message")

        with mock.patch("logging.Logger.warning") as mock_warning:
            base_logger.warning("Warning message")
            mock_warning.assert_called_once_with("Warning message")

        with mock.patch("logging.Logger.error") as mock_error:
            base_logger.error("Error message")
            mock_error.assert_called_once_with("Error message")

        with mock.patch("logging.Logger.critical") as mock_critical:
            base_logger.critical("Critical message")
            mock_critical.assert_called_once_with("Critical message")


class TestDebugLogger:
    @pytest.fixture
    def mock_pkg_resources(self):
        with mock.patch("importlib.resources") as mock_files:
            yield mock_files

    @pytest.fixture
    def debug_logger(self, mock_pkg_resources, tmp_path) -> DebugLogger:
        # Mock the files() function and its behavior
        mock_files = mock_pkg_resources.return_value
        mock_files.joinpath.return_value = tmp_path / "logs"

        return DebugLogger(
            logger_name="test_debug_logger",
            log_filename="debug.log",
            log_folder=tmp_path / "logs",
            active=True,
        )

    @staticmethod
    def test_init(debug_logger: DebugLogger, tmp_path):
        log_filepath = tmp_path / "logs" / "debug.log"

        assert debug_logger.logger.name == "test_debug_logger"
        assert debug_logger.logger.level == logging.DEBUG

    @staticmethod
    def test_file_handler(debug_logger: DebugLogger, tmp_path):
        log_filepath = tmp_path / "logs" / "debug.log"

        assert len(debug_logger.logger.handlers) == 2
        handler = debug_logger.logger.handlers[-1]
        assert isinstance(handler, logging.FileHandler)
        assert handler.baseFilename == str(log_filepath)


class TestSetLoggers:
    @pytest.mark.parametrize(
        "testing, expected_stdout_name, expected_stderr_name",
        [
            (True, "TaskTestLogger", "TaskTestLogger"),
            (False, "TaskOutputLogger", "TaskErrorLogger"),
        ],
    )
    def test_set_loggers(self, testing, expected_stdout_name, expected_stderr_name):
        error_loggers = set_loggers(testing)

        assert isinstance(error_loggers, ErrorLoggers)
        assert error_loggers.stdout.logger.name == expected_stdout_name
        assert error_loggers.stderr.logger.name == expected_stderr_name
