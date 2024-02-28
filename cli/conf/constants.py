import os
from enum import Enum


class StatusCode(Enum):
    SUCCESS = 0
    FAIL = 1
    CONFIGURED = 2


# Custom print emoji's
PASS = "[green]\u2713[/green]"
FAIL = "[red]\u274c[/red]"
PARTY = ":party_popper:"


# Filepaths
FOLDER_NAME = "zentra"
ZENTRA_MODELS_PATH = os.path.join(os.getcwd(), FOLDER_NAME, "models")
