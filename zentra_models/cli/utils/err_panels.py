from zentra_models.cli.conf.constants import FAIL, CommonErrorCodes
from zentra_models.cli.conf.message import BUG_MSG

from rich.panel import Panel


def request_failed_panel(status_code: int, url: str) -> Panel:
    """"""
    return Panel(
        f"\n{FAIL} [red]Failed to fetch file contents[/red] {FAIL}\n\nStatus code: [red]{status_code}[/red]\nFile URL: [magenta]{url}[/magenta].\n{BUG_MSG}\n[cyan]Error code[/cyan]: {CommonErrorCodes.REQUEST_FAILED.value}",
        expand=False,
        border_style="bright_red",
    )
