from zentra_api.cli.constants import FAIL, MAGIC, PASS
from zentra_api.cli.constants.message import (
    creation_msg,
    error_msg_with_checks,
    success_msg_with_checks,
)


def test_creation_msg():
    result = creation_msg("test_project", "api/test_project")

    target = f"\n{MAGIC} Creating new [green]FastAPI[/green] project called: [magenta]test_project[/magenta] -> [yellow]api/test_project[/yellow] {MAGIC}\n"
    assert result == target


def test_error_msg_with_checks():
    result = error_msg_with_checks("test", "nice long checks")

    target = f"\n{FAIL} test {FAIL}\nnice long checks"
    assert result == target


def test_success_msg_with_checks():
    result = success_msg_with_checks("test", "nice long checks", icon=PASS)

    target = f"\n{PASS} test {PASS}\nnice long checks"
    assert result == target
