import pytest

from cli.templates.details import COMPONENT_DETAILS_DICT

from tests.mappings.ui_imports import VALID_IMPORTS
from tests.mappings.ui_vals import VALID_VALS_MAP
from tests.templates.helper import SimpleCompBuilder

from zentra.core.react import LucideIcon
from zentra.ui.control import Button
from zentra.ui.navigation import (
    DDMCheckboxGroup,
    DDMGroup,
    DDMItem,
    DDMRadioGroup,
    DDMSeparator,
    DDMSubGroup,
    DropdownMenu,
)


class TestDropdownMenu:
    @pytest.fixture
    def dropdown_menu_radio_group(self) -> DropdownMenu:
        return DropdownMenu(
            trigger=Button(content="open", variant="outline"),
            items=DDMRadioGroup(
                texts=["Top Position", "Bottom Position", "Right Position"]
            ),
            label="Panel Position",
        )

    @pytest.fixture
    def dropdown_menu_checkbox(self) -> DropdownMenu:
        return DropdownMenu(
            trigger=Button(content="open", variant="outline"),
            items=DDMCheckboxGroup(texts=["Status Bar", "Activity Bar", "Panel"]),
            label="Appearance",
        )

    @pytest.fixture
    def dropdown_menu_str_list(self) -> DropdownMenu:
        return DropdownMenu(
            trigger="open",
            items=DDMGroup(items=["Top", "Bottom", "Right"]),
            label="Panel Position",
        )

    @pytest.fixture
    def dropdown_menu_full(self) -> DropdownMenu:
        return DropdownMenu(
            trigger=Button(content="open", variant="outline"),
            items=[
                DDMGroup(
                    items=[
                        DDMItem(
                            icon=LucideIcon(name="User"),
                            text="Profile",
                            shortcut_key="⇧⌘P",
                        ),
                        DDMItem(
                            icon=LucideIcon(name="CreditCard"),
                            text="Billing",
                            shortcut_key="⌘B",
                        ),
                        DDMItem(
                            icon=LucideIcon(name="Settings"),
                            text="Settings",
                            shortcut_key="⌘S",
                        ),
                        DDMItem(
                            icon=LucideIcon(name="Keyboard"),
                            text="Keyboard Shortcuts",
                            shortcut_key="⌘K",
                        ),
                    ]
                ),
                DDMGroup(
                    items=[
                        DDMItem(icon=LucideIcon(name="Users"), text="Team"),
                        DDMSubGroup(
                            trigger=DDMItem(
                                icon=LucideIcon(name="UserPlus"), text="Invite users"
                            ),
                            items=[
                                DDMItem(icon=LucideIcon(name="Mail"), text="Email"),
                                DDMItem(
                                    icon=LucideIcon(name="MessageSquare"),
                                    text="Message",
                                ),
                                DDMSeparator(),
                                DDMItem(
                                    icon=LucideIcon(name="PlusCircle"), text="More..."
                                ),
                            ],
                        ),
                        DDMItem(
                            icon=LucideIcon(name="Plus"),
                            text="New Team",
                            shortcut_key="⌘+T",
                        ),
                    ]
                ),
                DDMGroup(
                    items=[
                        DDMItem(icon=LucideIcon(name="Github"), text="Github"),
                        DDMItem(icon=LucideIcon(name="LifeBuoy"), text="Support"),
                        DDMItem(
                            icon=LucideIcon(name="Cloud"), text="API", disabled=True
                        ),
                        DDMSeparator(),
                        DDMItem(
                            icon=LucideIcon(name="LogOut"),
                            text="Log out",
                            shortcut_key="⇧⌘Q",
                        ),
                    ]
                ),
            ],
            label="My Account",
        )

    @pytest.fixture
    def wrapper_radio_group(
        self, dropdown_menu_radio_group: DropdownMenu
    ) -> SimpleCompBuilder:
        return SimpleCompBuilder(
            dropdown_menu_radio_group, COMPONENT_DETAILS_DICT["DropdownMenu"]
        )

    @pytest.fixture
    def wrapper_checkbox(
        self, dropdown_menu_checkbox: DropdownMenu
    ) -> SimpleCompBuilder:
        return SimpleCompBuilder(
            dropdown_menu_checkbox, COMPONENT_DETAILS_DICT["DropdownMenu"]
        )

    @pytest.fixture
    def wrapper_str_list(
        self, dropdown_menu_str_list: DropdownMenu
    ) -> SimpleCompBuilder:
        return SimpleCompBuilder(
            dropdown_menu_str_list, COMPONENT_DETAILS_DICT["DropdownMenu"]
        )

    @pytest.fixture
    def wrapper_full(self, dropdown_menu_full: DropdownMenu) -> SimpleCompBuilder:
        return SimpleCompBuilder(
            dropdown_menu_full, COMPONENT_DETAILS_DICT["DropdownMenu"]
        )

    @staticmethod
    def test_content_str_radio_group(wrapper_radio_group: SimpleCompBuilder):
        wrapper_radio_group.run(
            "content", VALID_VALS_MAP["dropdown_menu"]["content"]["radio_group"]
        )

    @staticmethod
    def test_content_str_checkbox(wrapper_checkbox: SimpleCompBuilder):
        wrapper_checkbox.run(
            "content", VALID_VALS_MAP["dropdown_menu"]["content"]["checkbox"]
        )

    @staticmethod
    def test_content_str_str_list(wrapper_str_list: SimpleCompBuilder):
        wrapper_str_list.run(
            "content", VALID_VALS_MAP["dropdown_menu"]["content"]["str_list"]
        )

    @staticmethod
    def test_content_str_full(wrapper_full: SimpleCompBuilder):
        wrapper_full.run("content", VALID_VALS_MAP["dropdown_menu"]["content"]["full"])

    @staticmethod
    def test_logic_str_radio_group(wrapper_radio_group: SimpleCompBuilder):
        wrapper_radio_group.run(
            "logic", VALID_VALS_MAP["dropdown_menu"]["logic"]["radio_group"]
        )

    @staticmethod
    def test_logic_str_checkbox(wrapper_checkbox: SimpleCompBuilder):
        wrapper_checkbox.run(
            "logic", VALID_VALS_MAP["dropdown_menu"]["logic"]["checkbox"]
        )

    @staticmethod
    def test_logic_str_str_list(wrapper_str_list: SimpleCompBuilder):
        wrapper_str_list.run(
            "logic", VALID_VALS_MAP["dropdown_menu"]["logic"]["str_list"]
        )

    @staticmethod
    def test_logic_str_full(wrapper_full: SimpleCompBuilder):
        wrapper_full.run("logic", VALID_VALS_MAP["dropdown_menu"]["logic"]["full"])

    @staticmethod
    def test_import_str_radio_group(wrapper_radio_group: SimpleCompBuilder):
        wrapper_radio_group.run(
            "imports", VALID_IMPORTS["dropdown_menu"]["radio_group"]
        )

    @staticmethod
    def test_import_str_checkbox(wrapper_checkbox: SimpleCompBuilder):
        wrapper_checkbox.run("imports", VALID_IMPORTS["dropdown_menu"]["checkbox"])

    @staticmethod
    def test_import_str_str_list(wrapper_str_list: SimpleCompBuilder):
        wrapper_str_list.run("imports", VALID_IMPORTS["dropdown_menu"]["str_list"])

    @staticmethod
    def test_import_str_full(wrapper_full: SimpleCompBuilder):
        wrapper_full.run("imports", VALID_IMPORTS["dropdown_menu"]["full"])
