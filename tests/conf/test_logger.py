import os
import pytest

from cli.conf.logger import BaseLogger


class TestBaseLogger:
    @pytest.fixture
    def log_file(self, tmp_path) -> str:
        return os.path.join(tmp_path, "tests.log")

    @pytest.fixture
    def mock_logger(self, log_file):
        """Fixture to provide a mock logger instance."""
        logger = BaseLogger("TestLogger")

        logger.file_handler(log_file)
        return logger

    def read_log_file(self, log_file: str) -> str:
        with open(log_file, "r") as file:
            return file.read()

    def test_debug(self, mock_logger: BaseLogger, log_file: str):
        message = "Debug message"
        mock_logger.debug(message)
        log_content = self.read_log_file(log_file)
        assert message in log_content

    def test_info(self, mock_logger: BaseLogger, log_file: str):
        message = "Info message"
        mock_logger.info(message)
        log_content = self.read_log_file(log_file)
        assert message in log_content

    def test_warning(self, mock_logger: BaseLogger, log_file: str):
        message = "Warning message"
        mock_logger.warning(message)
        log_content = self.read_log_file(log_file)
        assert message in log_content

    def test_error(self, mock_logger: BaseLogger, log_file: str):
        message = "Error message"
        mock_logger.error(message)
        log_content = self.read_log_file(log_file)
        assert message in log_content

    def test_critical(self, mock_logger: BaseLogger, log_file: str):
        message = "Critical message"
        mock_logger.critical(message)
        log_content = self.read_log_file(log_file)
        assert message in log_content
