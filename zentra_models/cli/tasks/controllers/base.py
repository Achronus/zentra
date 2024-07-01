from typing import TypeVar
from functools import wraps

from zentra_models.cli.conf.constants import PASS, FAIL
from zentra_models.cli.conf.logger import task_status_logger

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


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


ControllerMethod = TypeVar("ControllerMethod", bound="BaseController")


class BaseController:
    """A base controller class for all CLI tasks.

    Parameters:
    - `tasks` (`list[tuple[ControllerMethod, str]]`) - a list of tuples in the format of (task, desc), where `task` is a class method and `desc` is a descriptive string highlighting what the task does. For example:
    ```python
    tasks = [
        (self.create, "Creating my awesome components"),
        (self.update, "Updating my components")
    ]
    ```
    """

    def __init__(self, tasks: list[tuple[ControllerMethod, str]]) -> None:
        self.tasks = tasks
        self.called_tasks = []

    def run(self) -> None:
        """A handler for performing tasks in the controller."""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            for idx, (task, desc) in enumerate(self.tasks, 1):
                new_desc = f"{idx}. {desc}..."

                task_id = progress.add_task(description=new_desc, total=None)
                is_successful, error = task()

                self.called_tasks.append((new_desc, is_successful))
                status = PASS if is_successful else FAIL

                progress.update(
                    task_id, completed=1, description=f"{new_desc} {status}"
                )

                if error is not None:
                    raise error
