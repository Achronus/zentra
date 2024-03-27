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

    @staticmethod
    def test_repr_valid():
        btn = Button(
            text="Click me",
            url="https://example.com/",
            variant="secondary",
            size="sm",
            disabled=True,
        )
        result = builder(btn).__repr__()
        valid = """Button(component=Button(text='Click me', url=Url('https://example.com/'), variant='secondary', size='sm', disabled=True), attr_str=' disabled href="https://example.com/" variant="secondary" size="sm"', content_str='Click me', import_statement='import { Button } from "../ui/button"', component_str='<Button disabled href="https://example.com/" variant="secondary" size="sm">Click me</Button>', unique_logic_str='', classname='Button', no_content=False, no_unique_logic=True)"""

        assert result == valid, result
