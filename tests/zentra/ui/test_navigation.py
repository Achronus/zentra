import pytest

from cli.templates.details import COMPONENT_DETAILS_DICT

from tests.mappings.ui_imports import VALID_IMPORTS
from tests.mappings.ui_vals import VALID_VALS_MAP
from tests.templates.helper import SimpleCompBuilder

from pydantic import ValidationError

from zentra.core.react import LucideIcon
from zentra.nextjs import Link
from zentra.ui.control import Button
from zentra.ui.navigation import (
    BCDropdownMenu,
    BCItem,
    BCTrigger,
    Breadcrumb,
    Command,
    CommandGroup,
    CommandItem,
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
    def dropdown_menu_with_links(self) -> DropdownMenu:
        return DropdownMenu(
            trigger="open",
            items=DDMGroup(
                label="Core Settings",
                items=[
                    DDMItem(text="Profile", icon=LucideIcon(name="User")),
                    DDMItem(
                        text=Link(href="/billing", text="Billing"),
                        icon=LucideIcon(name="CreditCard"),
                        shortcut_key="⌘B",
                        disabled=True,
                    ),
                    DDMItem(
                        text=Link(href="/settings", text="Settings"),
                    ),
                    DDMItem(
                        text=Link(href="/settings", text="Settings"),
                        shortcut_key="⌘B",
                    ),
                ],
            ),
            label="Account Settings",
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
    def wrapper_with_links(
        self, dropdown_menu_with_links: DropdownMenu
    ) -> SimpleCompBuilder:
        return SimpleCompBuilder(
            dropdown_menu_with_links, COMPONENT_DETAILS_DICT["DropdownMenu"]
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
    def test_content_str_no_label():
        comp = DropdownMenu(
            trigger="open",
            items=DDMGroup(items=["Top", "Bottom", "Right"]),
        )
        wrapper = SimpleCompBuilder(comp, COMPONENT_DETAILS_DICT["DropdownMenu"])
        wrapper.run("content", VALID_VALS_MAP["dropdown_menu"]["content"]["no_label"])

    @staticmethod
    def test_content_with_links(wrapper_with_links: SimpleCompBuilder):
        wrapper_with_links.run(
            "content", VALID_VALS_MAP["dropdown_menu"]["content"]["with_links"]
        )

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

    @staticmethod
    def test_import_with_links(wrapper_with_links: SimpleCompBuilder):
        wrapper_with_links.run(
            "imports", VALID_IMPORTS["dropdown_menu"]["with_links"], list_output=True
        )

    @staticmethod
    def test_validate_link_error():
        with pytest.raises(ValidationError):
            DropdownMenu(
                trigger="open",
                items=DDMGroup(items=[DDMItem(text=Link(href="/settings"))]),
            )

    @staticmethod
    def test_item_values_error():
        with pytest.raises(ValidationError):
            DropdownMenu(
                trigger="open",
                items=DDMRadioGroup(texts=["test"], values=["test1", "test2"]),
            )


class TestBreadcrumb:
    @pytest.fixture
    def breadcrumb_ellipsis_trigger(self) -> Breadcrumb:
        return Breadcrumb(
            page_name="Breadcrumb",
            items=[
                BCItem(text="Home", href="/"),
                BCDropdownMenu(
                    trigger=BCTrigger(),
                    items=[
                        BCItem(text="Documentation", href="/docs"),
                        BCItem(text="Themes", href="/themes"),
                        BCItem(text="GitHub", href="/github"),
                    ],
                ),
                BCItem(text="Components", href="/docs/components"),
            ],
        )

    @pytest.fixture
    def breadcrumb_text_trigger(self) -> Breadcrumb:
        return Breadcrumb(
            page_name="Breadcrumb",
            items=[
                BCItem(text="Home", href="/"),
                BCDropdownMenu(
                    trigger=BCTrigger(variant="text", text="Components"),
                    items=[
                        BCItem(text="Documentation", href="/docs"),
                        BCItem(text="Themes", href="/themes"),
                        BCItem(text="GitHub", href="/github"),
                    ],
                ),
                BCItem(text="Components", href="/docs/components"),
            ],
            custom_sep="Slash",
        )

    @pytest.fixture
    def wrapper_ellipsis_trigger(
        self, breadcrumb_ellipsis_trigger: Breadcrumb
    ) -> SimpleCompBuilder:
        return SimpleCompBuilder(
            breadcrumb_ellipsis_trigger, COMPONENT_DETAILS_DICT["Breadcrumb"]
        )

    @pytest.fixture
    def wrapper_text_trigger(
        self, breadcrumb_text_trigger: Breadcrumb
    ) -> SimpleCompBuilder:
        return SimpleCompBuilder(
            breadcrumb_text_trigger, COMPONENT_DETAILS_DICT["Breadcrumb"]
        )

    @staticmethod
    def test_content_str_ellipsis_trigger(wrapper_ellipsis_trigger: SimpleCompBuilder):
        wrapper_ellipsis_trigger.run(
            "content", VALID_VALS_MAP["breadcrumb"]["content"]["ellipsis_trigger"]
        )

    @staticmethod
    def test_content_str_text_trigger(wrapper_text_trigger: SimpleCompBuilder):
        wrapper_text_trigger.run(
            "content", VALID_VALS_MAP["breadcrumb"]["content"]["text_trigger"]
        )

    @staticmethod
    def test_import_str_ellipsis_trigger(wrapper_ellipsis_trigger: SimpleCompBuilder):
        wrapper_ellipsis_trigger.run(
            "imports", VALID_IMPORTS["breadcrumb"]["ellipsis_trigger"], list_output=True
        )

    @staticmethod
    def test_import_str_text_trigger(wrapper_text_trigger: SimpleCompBuilder):
        wrapper_text_trigger.run(
            "imports", VALID_IMPORTS["breadcrumb"]["text_trigger"], list_output=True
        )


class TestCommand:
    @pytest.fixture
    def command_simple(self) -> Command:
        return Command(items=[CommandGroup(items=["Calendar", "Search Emoji"])])

    @pytest.fixture
    def command_simple_links(self) -> Command:
        return Command(
            items=[
                CommandGroup(
                    items=[
                        CommandItem(
                            text=Link(href="/", text="Calendar"),
                            icon=LucideIcon(name="Calendar"),
                        ),
                        CommandItem(
                            text=Link(href="/", text="Search Emoji"),
                            icon=LucideIcon(name="Smile"),
                        ),
                    ],
                    heading="Suggestions",
                )
            ]
        )

    @pytest.fixture
    def command_group_simple(self) -> Command:
        return Command(
            items=[
                CommandGroup(
                    items=[
                        CommandItem(text="Calendar"),
                        CommandItem(text="Search Emoji"),
                    ],
                    heading="Suggestions",
                )
            ]
        )

    @pytest.fixture
    def command_multi_groups(self) -> Command:
        return Command(
            items=[
                CommandGroup(
                    items=[
                        CommandItem(text="Calendar", icon=LucideIcon(name="Calendar")),
                        CommandItem(text="Search Emoji", icon=LucideIcon(name="Smile")),
                        CommandItem(
                            text="Calculator", icon=LucideIcon(name="Calculator")
                        ),
                    ],
                    heading="Suggestions",
                ),
                CommandGroup(
                    items=[
                        CommandItem(
                            text="Profile",
                            icon=LucideIcon(name="User"),
                            shortcut_key="⌘P",
                        ),
                        CommandItem(
                            text="Billing",
                            icon=LucideIcon(name="CreditCard"),
                            shortcut_key="⌘B",
                        ),
                        CommandItem(
                            text="Settings",
                            icon=LucideIcon(name="Settings"),
                            shortcut_key="⌘S",
                        ),
                    ],
                    heading="Settings",
                ),
            ]
        )

    @pytest.fixture
    def wrapper_simple(self, command_simple: Command) -> SimpleCompBuilder:
        return SimpleCompBuilder(command_simple, COMPONENT_DETAILS_DICT["Command"])

    @pytest.fixture
    def wrapper_simple_links(self, command_simple_links: Command) -> SimpleCompBuilder:
        return SimpleCompBuilder(
            command_simple_links, COMPONENT_DETAILS_DICT["Command"]
        )

    @pytest.fixture
    def wrapper_group_simple(self, command_group_simple: Command) -> SimpleCompBuilder:
        return SimpleCompBuilder(
            command_group_simple, COMPONENT_DETAILS_DICT["Command"]
        )

    @pytest.fixture
    def wrapper_multi_groups(self, command_multi_groups: Command) -> SimpleCompBuilder:
        return SimpleCompBuilder(
            command_multi_groups, COMPONENT_DETAILS_DICT["Command"]
        )

    @staticmethod
    def test_content_str_simple(wrapper_simple: SimpleCompBuilder):
        wrapper_simple.run("content", VALID_VALS_MAP["command"]["content"]["simple"])

    @staticmethod
    def test_content_str_simple_links(wrapper_simple_links: SimpleCompBuilder):
        wrapper_simple_links.run(
            "content", VALID_VALS_MAP["command"]["content"]["simple_links"]
        )

    @staticmethod
    def test_content_str_group_simple(wrapper_group_simple: SimpleCompBuilder):
        wrapper_group_simple.run(
            "content", VALID_VALS_MAP["command"]["content"]["group_simple"]
        )

    @staticmethod
    def test_content_str_multi_groups(wrapper_multi_groups: SimpleCompBuilder):
        wrapper_multi_groups.run(
            "content", VALID_VALS_MAP["command"]["content"]["multi_groups"]
        )

    @staticmethod
    def test_import_str_simple(wrapper_simple: SimpleCompBuilder):
        wrapper_simple.run("imports", VALID_IMPORTS["command"]["simple"])

    @staticmethod
    def test_import_str_simple_links(wrapper_simple_links: SimpleCompBuilder):
        wrapper_simple_links.run("imports", VALID_IMPORTS["command"]["simple_links"])

    @staticmethod
    def test_import_str_group_simple(wrapper_group_simple: SimpleCompBuilder):
        wrapper_group_simple.run("imports", VALID_IMPORTS["command"]["group_simple"])

    @staticmethod
    def test_import_str_multi_groups(wrapper_multi_groups: SimpleCompBuilder):
        wrapper_multi_groups.run("imports", VALID_IMPORTS["command"]["multi_groups"])
