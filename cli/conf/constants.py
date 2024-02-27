from enum import Enum


class StatusCode(Enum):
    SUCCESS = 0
    FAIL = 1
    CONFIGURED = 2


# Custom print emoji's
PASS = "[green]\u2713[/green]"
FAIL = "[red]\u274c[/red]"
PARTY = ":party_popper:"
