from tests.mappings.helper import builder
from zentra.ui.control import Button


class TestBuilder:
    @staticmethod
    def test_all_params_valid():
        btn = Button(
            text="Click me",
            url="https://example.com/",
            variant="secondary",
            size="sm",
            disabled=True,
        )
        result = builder(btn).component_str
        valid = '<Button disabled href="https://example.com/" variant="secondary" size="sm">Click me</Button>'

        assert result == valid, (result, valid)
