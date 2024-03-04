import os
from enum import Enum


class StatusCode(Enum):
    SUCCESS = 0
    FAIL = 1
    CONFIGURED = 2
    NO_COMPONENTS = 3


# Custom print emoji's
PASS = "[green]\u2713[/green]"
FAIL = "[red]\u274c[/red]"
PARTY = ":party_popper:"


# Core folder names and URLS
FOLDER_NAME = "zentra"
DOCS_URL = "#"


class ZentaFilepaths:
    ROOT = os.path.join(os.getcwd(), FOLDER_NAME)  # (cwd)/zentra
    MODELS = os.path.join(ROOT, "models")  # (cwd)/zentra/models
    GENERATED = os.path.join(ROOT, "generated")  # (cwd)/zentra/generated


class ZentraGeneratedFilepaths:
    # (cwd)/zentra/generated
    ROOT = ZentaFilepaths.GENERATED
    COMPONENTS = os.path.join(ROOT, "components")  # generated/components
    ZENTRA = os.path.join(COMPONENTS, "zentra")  # generated/zentra


class ZentraUIFilepaths:
    # (cwd)/zentra/generated/components/zentra/ui
    ROOT = os.path.join(ZentraGeneratedFilepaths.ZENTRA, "ui")
    BASE = os.path.join(ROOT, "base")  # ui/base

    CONTROL = os.path.join(ROOT, "control")  # ui/control
    MODAL = os.path.join(ROOT, "modal")  # ui/modal
    NAVIGATION = os.path.join(ROOT, "navigation")  # ui/navigation
    NOTIFICATION = os.path.join(ROOT, "notification")  # ui/notification
    PRESENTATION = os.path.join(ROOT, "presentation")  # ui/presentation
