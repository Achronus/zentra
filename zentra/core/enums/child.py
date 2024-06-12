from enum import Enum


class SeparatorVariant(str, Enum):
    BREADCRUMB = "breadcrumb"
    DROPDOWN_MENU = "dropdown_menu"
    MENUBAR = "menubar"
    COMMAND = "command"
    CONTEXT_MENU = "context_menu"
    INPUT_OTP = "input_otp"


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
    PAGINATION = "pagination"


class GroupVariant(str, Enum):
    DROPDOWN_MENU = "dropdown_menu"
    SELECT = "select"
    INPUT_OTP = "input_otp"


class ContentVariant(str, Enum):
    DROPDOWN_MENU = "dropdown_menu"
    COLLAPSIBLE = "collapsible"
    SELECT = "select"
    ALERT_DIALOG = "alert_dialog"
    PAGINATION = "pagination"


class TitleVariant(str, Enum):
    ALERT = "alert"
    ALERT_DIALOG = "alert_dialog"


class DescriptionVariant(str, Enum):
    ALERT = "alert"
    ALERT_DIALOG = "alert_dialog"


class HeaderVariant(str, Enum):
    ALERT_DIALOG = "alert_dialog"


class FooterVariant(str, Enum):
    ALERT_DIALOG = "alert_dialog"


class CancelVariant(str, Enum):
    ALERT_DIALOG = "alert_dialog"


class ActionVariant(str, Enum):
    ALERT_DIALOG = "alert_dialog"
