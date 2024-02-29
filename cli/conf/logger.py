import os
import logging


class BaseLogger:
    """A base logger class that all loggers inherit from."""

    def __init__(
        self,
        logger_name: str,
        log_filename: str = "debug.log",
        level: int = logging.DEBUG,
    ) -> None:
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(level=level)

        self.log_filename = log_filename

    def console_handler(
        self,
        level: int = logging.INFO,
        format: str = "%(name)s: %(levelname)s | %(message)s",
    ) -> logging.StreamHandler:
        """Configuration for console handlers."""
        handler = logging.StreamHandler()
        handler.setLevel(level=level)

        formatter = logging.Formatter(format)
        handler.setFormatter(formatter)

        return handler

    def file_handler(
        self,
        log_filepath: str,
        level: int = logging.DEBUG,
        format: str = "%(asctime)s (%(name)s): %(levelname)s | %(message)s",
        datefmt: str = "%Y-%m-%d %H:%M:%S",
    ) -> logging.FileHandler:
        """Configuration for file handlers."""
        handler = logging.FileHandler(log_filepath)
        handler.setLevel(level=level)

        formatter = logging.Formatter(format, datefmt=datefmt)
        handler.setFormatter(formatter)
        return handler

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


class TaskStatusLogger(BaseLogger):
    """A logger specific to the task status wrapper."""

    def __init__(self, logger_name: str, log_filename: str = "debug.log"):
        super().__init__(logger_name, log_filename)

        log_filepath = os.path.join(os.getcwd(), "cli", "conf", "logs", log_filename)

        self.logger.addHandler(self.console_handler())
        self.logger.addHandler(self.file_handler(log_filepath))


task_status_logger = TaskStatusLogger("TaskStatusLogger")
