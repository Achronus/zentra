from enum import Enum


class SeparatorVariant(str, Enum):
    BREADCRUMB = "breadcrumb"
    DROPDOWN_MENU = "dropdown_menu"
    MENUBAR = "menubar"
    COMMAND = "command"
    CONTEXT_MENU = "context_menu"


class ValueVariant(str, Enum):
    SELECT = "select"


class TriggerVariant(str, Enum):
    ACCORDION = "accordion"
    ALERT_DIALOG = "alert_dialog"
    COLLAPSIBLE = "collapsible"
    DROPDOWN_MENU = "dropdown_menu"
    POPOVER = "popover"
    SELECT = "select"
    TOOLTIP = "tooltip"


class LabelVariant(str, Enum):
    DROPDOWN_MENU = "dropdown_menu"
    CONTEXT_MENU = "context_menu"
    SELECT = "select"


class ItemVariant(str, Enum):
    SELECT = "select"


class GroupVariant(str, Enum):
    DROPDOWN_MENU = "dropdown_menu"
    SELECT = "select"


class ContentVariant(str, Enum):
    DROPDOWN_MENU = "dropdown_menu"
    COLLAPSIBLE = "collapsible"
    SELECT = "select"


class TitleVariant(str, Enum):
    ALERT = "alert"


class DescriptionVariant(str, Enum):
    ALERT = "alert"
