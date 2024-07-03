from functools import wraps

from zentra_models.cli.conf.logger import task_status_logger


def status(func):
    """A wrapper around controller functions to define the function completion status."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
            return True, None
        except Exception as e:
            task_status_logger.error(f"{type(e).__name__}: {e}")
            return False, e

    return wrapper
