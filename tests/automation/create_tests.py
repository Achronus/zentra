import os
import textwrap
from pydantic import BaseModel


INPUT_DICT = {
    "name": "DropdownMenu",
    "valid_map_name": "dropdown_menu",
    "items": {
        "radio_group": 'DropdownMenu(trigger=Button(content="open", variant="outline"), items=DDMRadioGroup(texts=["Top Position", "Bottom Position", "Right Position"]), label="Panel Position")',
        "checkbox": 'DropdownMenu(trigger=Button(content="open", variant="outline"), items=DDMCheckboxGroup(texts=["Status Bar", "Activity Bar", "Panel"]), label="Appearance")',
        "str_list": 'DropdownMenu(trigger="open", items=DDMGroup(items=["Top", "Bottom", "Right"]), label="Panel Position")',
        "full": 'DropdownMenu(trigger=Button(content="open", variant="outline"), items=[DDMGroup(items=[DDMItem(icon=LucideIcon(name="User"), text="Profile", shortcut_key="⇧⌘P"), DDMItem(icon=LucideIcon(name="CreditCard"), text="Billing", shortcut_key="⌘B"), DDMItem(icon=LucideIcon(name="Settings"), text="Settings", shortcut_key="⌘S"), DDMItem(icon=LucideIcon(name="Keyboard"), text="Keyboard Shortcuts", shortcut_key="⌘K")]), DDMGroup(items=[DDMItem(icon=LucideIcon(name="Users"), text="Team"), DDMSubGroup(trigger=DDMItem(icon=LucideIcon(name="UserPlus"), text="Invite users"), items=[DDMItem(icon=LucideIcon(name="Mail"), text="Email"), DDMItem(icon=LucideIcon(name="MessageSquare"), text="Message"), DDMSeparator(), DDMItem(icon=LucideIcon(name="PlusCircle"), text="More...")]), DDMItem(icon=LucideIcon(name="Plus"), text="New Team", shortcut_key="⌘+T")]), DDMGroup(items=[DDMItem(icon=LucideIcon(name="Github"), text="Github"), DDMItem(icon=LucideIcon(name="LifeBuoy"), text="Support"), DDMItem(icon=LucideIcon(name="Cloud"), text="API", disabled=True), DDMSeparator(), DDMItem(icon=LucideIcon(name="LogOut"), text="Log out", shortcut_key="⇧⌘Q")])], label="My Account")',
    },
    "num_logic": 4,
    "num_import": 4,
}


class Input(BaseModel):
    name: str
    valid_map_name: str
    items: dict[str, str]
    num_logic: int
    num_import: int


def build_tests(input_model: Input) -> None:
    """Automatically creates a set of tests based on a given input dictionary.

    Must contain the following keys:
    - `name` - the name of the component
    - `valid_map_name` - the lowercased variant of the component. Normally, used with an underscore when using more than two words. E.g., `DropdownMenu` -> `dropdown_menu`
    - `items` - a dictionary of component model examples -> `{name: model_example}`
    - `num_logic` - number of logic tests
    - `num_import` - number of import tests
    """
    func_name_pair = (input_model.valid_map_name, input_model.name)
    import_list, logic_list = [], []

    def fixture(model_name: tuple[str, str], item_type: str, item_value: str) -> str:
        func_name = f"{model_name[0]}_{item_type}"
        return textwrap.indent(
            textwrap.dedent(f"""
        @pytest.fixture
        def {func_name}(self) -> {model_name[1]}:
            return {item_value}
        """),
            "    ",
        )

    def wrapper(item_type: str, model_name: tuple[str, str]) -> str:
        func_name = f"{model_name[0]}_{item_type}"
        return textwrap.indent(
            textwrap.dedent(f"""
        @pytest.fixture
        def wrapper_{item_type}(self, {func_name}: {model_name[1]}) -> SimpleCompBuilder:
            return SimpleCompBuilder({func_name}, COMPONENT_DETAILS_DICT["{model_name[1]}"])
        """),
            "    ",
        )

    def test_func(
        func_type: str,
        items: dict[str, str],
        model_name: str,
        count: int = 1,
    ) -> list[str]:
        func_list = []

        for key in items.keys():
            if func_type == "import":
                if count == 1:
                    map_type = f'VALID_IMPORTS["{model_name}"]'
                else:
                    map_type = f'VALID_IMPORTS["{model_name}"]["{key}"]'
            else:
                map_type = f'VALID_VALS_MAP["{model_name}"]["{func_type}"]["{key}"]'

            run_type = f"{func_type}s" if func_type == "import" else func_type
            func_list.append(
                textwrap.indent(
                    textwrap.dedent(f"""
                @staticmethod
                def test_{func_type}_str_{key}(wrapper_{key}: SimpleCompBuilder):
                    wrapper_{key}.run("{run_type}", {map_type})
                """),
                    "    ",
                )
            )

        return func_list

    fixtures_list = [
        fixture(func_name_pair, key, value) for key, value in input_model.items.items()
    ]
    wrapper_list = [wrapper(key, func_name_pair) for key in input_model.items.keys()]
    content_list = test_func("content", input_model.items, input_model.valid_map_name)

    if input_model.num_logic > 0:
        logic_list = test_func("logic", input_model.items, input_model.valid_map_name)
        logic_list = logic_list[: input_model.num_logic]

    if input_model.num_import > 0:
        import_list = test_func(
            "import",
            input_model.items,
            input_model.valid_map_name,
            input_model.num_import,
        )
        import_list = import_list[: input_model.num_import]

    TEMPLATE = [
        f"class Test{input_model.name}:",
        *fixtures_list,
        *wrapper_list,
        *content_list,
        *logic_list,
        *import_list,
    ]

    filepath = os.path.join(os.getcwd(), "tests", "automation", "output.py")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("".join(TEMPLATE))


if __name__ == "__main__":
    INPUT = Input(**INPUT_DICT)
    build_tests(INPUT)
