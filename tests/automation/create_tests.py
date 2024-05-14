import os
import textwrap
from pydantic import BaseModel


INPUT_DICT = {
    "name": "Pagination",
    "items": {
        "simple": 'Pagination(items_per_page=10, links=["#", "#", "#"])',
        "full": 'Pagination(items_per_page=10, total_items=20, links=["#", "#", "#"], ellipsis=True)',
    },
    "num_logic": 2,
    "num_import": 1,
}


class Input(BaseModel):
    name: str
    items: dict[str, str]
    num_logic: int
    num_import: int


def build_tests(input_model: Input) -> None:
    """Automatically creates a set of tests based on a given input dictionary.

    Must contain the following keys:
    - `name` - the name of the component
    - `items` - a dictionary of component model examples -> `{name: model_example}`
    - `num_logic` - number of logic tests
    - `num_import` - number of import tests
    """
    name_upper = input_model.name.capitalize()
    name_lower = input_model.name.lower()
    import_list, logic_list = [], []

    def fixture(model_name: str, item_type: str, item_value: str) -> str:
        func_name = f"{model_name.lower()}_{item_type}"
        return textwrap.indent(
            textwrap.dedent(f"""
        @pytest.fixture
        def {func_name}(self) -> {model_name}:
            return {item_value}
        """),
            "    ",
        )

    def wrapper(item_type: str, model_name: str) -> str:
        func_name = f"{model_name.lower()}_{item_type}"
        return textwrap.indent(
            textwrap.dedent(f"""
        @pytest.fixture
        def wrapper_{item_type}(self, {func_name}: {model_name}) -> SimpleCompBuilder:
            return SimpleCompBuilder({func_name}, COMPONENT_DETAILS_DICT["{model_name}"])
        """),
            "    ",
        )

    def test_func(
        func_type: str, items: dict[str, str], model_name: str, count: int = 1
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
        fixture(name_upper, key, value) for key, value in input_model.items.items()
    ]
    wrapper_list = [wrapper(key, name_upper) for key in input_model.items.keys()]
    content_list = test_func("content", input_model.items, name_lower)

    if input_model.num_logic > 0:
        logic_list = test_func("logic", input_model.items, name_lower)
        logic_list = logic_list[: input_model.num_logic]

    if input_model.num_import > 0:
        import_list = test_func(
            "import", input_model.items, name_lower, input_model.num_import
        )
        import_list = import_list[: input_model.num_import]

    TEMPLATE = [
        f"class Test{name_upper}:",
        *fixtures_list,
        *wrapper_list,
        *content_list,
        *logic_list,
        *import_list,
    ]

    filepath = os.path.join(os.getcwd(), "tests", "automation", "output.py")
    with open(filepath, "w") as f:
        f.write("".join(TEMPLATE))


if __name__ == "__main__":
    INPUT = Input(**INPUT_DICT)
    build_tests(INPUT)
