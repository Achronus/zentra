import os
from enum import Enum


class CommonErrorCodes(Enum):
    CONFIG_MISSING = 1
    MODELS_DIR_MISSING = 2
    SRC_DIR_MISSING = 3
    DEST_DIR_MISSING = 4


class SetupErrorCodes(Enum):
    INIT_SUCCESS = 0
    CONFIGURED = 1
    ZENTRA_MISSING = 2


class GenerateErrorCodes(Enum):
    NO_COMPONENTS = 1


# Custom print emoji's
PASS = "[green]\u2713[/green]"
FAIL = "[red]\u274c[/red]"
PARTY = ":party_popper:"


# Core folder names and URLS
FOLDER_NAME = "zentra"
DOCS_URL = "#"


class ZentaFilepaths:
    """A storage container for the core filepaths in the `zentra` folder."""

    ROOT = os.path.join(os.getcwd(), FOLDER_NAME)  # (cwd)/zentra
    MODELS = os.path.join(ROOT, "models")  # (cwd)/zentra/models
    GENERATED = os.path.join(ROOT, "generated")  # (cwd)/zentra/generated

    SETUP_FILENAME = "__init__.py"


class LocalCoreComponentFilepaths:
    """A storage container for the local core component filepaths in the `components` folder."""

    # (cwd)/components
    ROOT = os.path.join(os.getcwd(), "components")
    UI = os.path.join(ROOT, "ui")  # components/ui
    UPLOADTHING = os.path.join(ROOT, "uploadthing")  # components/uploadthing


class LocalUIComponentFilepaths:
    """A storage container for the local UI component filepaths in the `components/ui` folder."""

    # (cwd)/components/ui
    ROOT = LocalCoreComponentFilepaths.UI
    BASE = os.path.join(ROOT, "base")  # ui/base
    TEMPLATES = os.path.join(ROOT, "templates")  # ui/templates


class LocalUploadthingFilepaths:
    """A storage container for the local Uploadthing component filepaths in the `components/uploadthing` folder."""

    # (cwd)/components/uploadthing
    ROOT = LocalCoreComponentFilepaths.UPLOADTHING
    BASE = os.path.join(ROOT, "base")  # uploadthing/base
    TEMPLATES = os.path.join(ROOT, "templates")  # uploadthing/templates

    BASE_BASIC = os.path.join(BASE, "basic")  # base/basic
    BASE_NEXTJS = os.path.join(BASE, "nextjs")  # base/nextjs


class ZentraGeneratedFilepaths:
    """A storage container for the core filepaths in the `zentra/generated` folder."""

    # (cwd)/zentra/generated
    ROOT = ZentaFilepaths.GENERATED
    COMPONENTS = os.path.join(ROOT, "components")  # generated/components
    ZENTRA = os.path.join(COMPONENTS, "zentra")  # generated/components/zentra


class ZentraUIFilepaths:
    """A storage container for filepaths in the `generated/components/zentra/ui` folder."""

    # (cwd)/zentra/generated/components/zentra/ui
    ROOT = os.path.join(ZentraGeneratedFilepaths.ZENTRA, "ui")
    BASE = os.path.join(ROOT, "base")  # ui/base

    CONTROL = os.path.join(ROOT, "control")  # ui/control
    MODAL = os.path.join(ROOT, "modal")  # ui/modal
    NAVIGATION = os.path.join(ROOT, "navigation")  # ui/navigation
    NOTIFICATION = os.path.join(ROOT, "notification")  # ui/notification
    PRESENTATION = os.path.join(ROOT, "presentation")  # ui/presentation
