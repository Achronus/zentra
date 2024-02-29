from ...conf.constants import PASS

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


def run_tasks(tasks: list[tuple]) -> None:
    """A task handler for performing each task in the controller."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        for idx, (task, desc) in enumerate(tasks, 1):
            new_desc = f"{idx}. {desc}"
            task_id = progress.add_task(description=new_desc, total=None)
            task().run(progress)
            progress.update(task_id, completed=1, description=f"{new_desc} {PASS}")
