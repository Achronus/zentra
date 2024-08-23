import logging
from pathlib import Path

from zentra_sdk.cli.constants import LOG_FOLDER


class BaseLogger:
    """A base logger class that all loggers inherit from."""

    def __init__(
        self,
        logger_name: str,
        level: int = logging.DEBUG,
    ) -> None:
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(level=level)

    def console_handler(
        self,
        level: int = logging.INFO,
        format: str = "%(name)s: %(levelname)s | %(message)s",
    ) -> None:
        """Configuration for console handlers."""
        handler = logging.StreamHandler()
        handler.setLevel(level=level)

        formatter = logging.Formatter(format)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def file_handler(
        self,
        log_filepath: str,
        level: int = logging.DEBUG,
        format: str = "%(asctime)s (%(name)s): %(levelname)s | %(message)s",
        datefmt: str = "%Y-%m-%d %H:%M:%S",
    ) -> None:
        """Configuration for file handlers."""
        handler = logging.FileHandler(log_filepath)
        handler.setLevel(level=level)

        formatter = logging.Formatter(format, datefmt=datefmt)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def debug(self, msg: str) -> None:
        """Sends a debug message to the logger."""
        self.logger.debug(msg)

    def info(self, msg: str) -> None:
        """Sends a info message to the logger."""
        self.logger.info(msg)

    def warning(self, msg: str) -> None:
        """Sends a warning message to the logger."""
        self.logger.warning(msg)

    def error(self, msg: str) -> None:
        """Sends an error message to the logger."""
        self.logger.error(msg)

    def critical(self, msg: str) -> None:
        """Sends a critical message to the logger."""
        self.logger.critical(msg)


class DebugLogger(BaseLogger):
    """A logger specific for debugging purposes."""

    def __init__(
        self,
        logger_name: str,
        log_filename: str = "debug.log",
        log_folder: str = LOG_FOLDER,
        active: bool = False,
    ):
        super().__init__(logger_name, level=logging.DEBUG)

        log_filepath = Path(log_folder, log_filename)

        if not log_filepath.exists():
            Path(log_folder).mkdir(exist_ok=True)
            log_filepath.touch(exist_ok=True)

        if active:  # pragma: no cover
            self.file_handler(log_filepath)


task_output_logger = DebugLogger(
    "TaskOutputLogger",
    "task_output.log",
    active=True,
)
task_error_logger = DebugLogger(
    "TaskErrorLogger",
    "task_error.log",
    active=True,
)
task_test_logger = DebugLogger(
    "TaskTestLogger",
    "testing.log",
    active=True,
)


class ErrorLoggers:
    """A storage container for error loggers."""

    def __init__(self, stdout: DebugLogger, stderr: DebugLogger) -> None:
        self.stdout = stdout
        self.stderr = stderr


def set_loggers(testing: bool = False) -> ErrorLoggers:
    """Returns a logger object containing debug loggers."""
    if testing:
        return ErrorLoggers(stdout=task_test_logger, stderr=task_test_logger)

    return ErrorLoggers(stdout=task_output_logger, stderr=task_error_logger)
