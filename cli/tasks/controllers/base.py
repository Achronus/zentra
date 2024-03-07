from typing import TypeVar
from functools import wraps

from cli.conf.constants import PASS, FAIL
from cli.conf.logger import task_status_logger

from rich.progress import Progress


def status(func):
    """A wrapper around controller functions to define the function completion status."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
            return True
        except Exception as e:
            task_status_logger.error(f"{type(e).__name__}: {e}")
            return False

    return wrapper


ControllerMethod = TypeVar("ControllerMethod", bound="BaseController")


class BaseController:
    """A base controller class for all CLI tasks.

    :param tasks: (list[tuple[ControllerMethod, str]]) - a list of tuples in the format of (task, desc), where `task` is a class method and `desc` is a descriptive string highlighting what the task does. For example:
    ```python
    sub_tasks = [
        (self.create, "Building venv"),
        (self.update_pip, "Updating PIP")
    ]
    ```
    """

    def __init__(self, tasks: list[tuple[ControllerMethod, str]]) -> None:
        self.tasks = tasks
        self.called_tasks = []

    @staticmethod
    def update_desc(desc: str) -> str:
        """Updates task description format."""
        return f"   {desc}..."

    def format_tasks(self) -> None:
        """Formats controller tasks into a standardised format."""
        updated_tasks = []
        for task, desc in self.tasks:
            updated_tasks.append((task, self.update_desc(desc)))

        self.tasks = updated_tasks

    def run(self, progress: Progress) -> None:
        """A subtask handler for performing subtasks in the controller."""
        self.format_tasks()

        for task, desc in self.tasks:
            task_id = progress.add_task(description=desc, total=None)
            is_successful = task()
            self.called_tasks.append((desc, is_successful))
            status = PASS if is_successful else FAIL
            progress.update(task_id, completed=1, description=f"{desc} {status}")
