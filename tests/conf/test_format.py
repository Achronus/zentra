import re
from hypothesis import assume, given
from hypothesis.strategies import text, characters, sampled_from, integers

from cli.conf.format import (
    component_count_str,
    name_from_camel_case,
    plural_name_formatter,
    set_colour,
)


@given(text(alphabet=characters(whitelist_categories=("Lu", "Ll", "Nd")), min_size=10))
def test_name_from_camel_case_hypothesis(input_string):
    result = name_from_camel_case(input_string)

    expected_result = re.sub("([a-z0-9])([A-Z])", r"\1-\2", input_string).lower()
    assert result == expected_result


# Hypothesis strategy for valid text and colour inputs
text_strategy = text(min_size=1, max_size=50)
colour_strategy = sampled_from(["red", "green", "blue", "yellow"])


@given(text=text_strategy, colour=colour_strategy)
def test_set_colour(text, colour):
    result = set_colour(text, colour)
    assert result.startswith(f"[{colour}]")
    assert result.endswith(f"[/{colour}]")
    assert text in result


@given(name=text(min_size=1, max_size=20), count=integers(min_value=0, max_value=100))
def test_plural_name_formatter(name, count):
    result = plural_name_formatter(name, count)
    if count == 1:
        assert result == name
    else:
        assert result == f"{name}s"


@given(
    page_count=integers(min_value=0, max_value=100),
    component_count=integers(min_value=0, max_value=100),
)
def test_component_count_str(page_count, component_count):
    assume(page_count >= 0 and component_count >= 0)

    class MockZentra:
        def __init__(self, pages, component_names):
            self.pages = pages
            self.component_names = component_names

    zentra = MockZentra(
        pages=[None] * page_count, component_names=[None] * component_count
    )
    result = component_count_str(zentra)

    page_name = plural_name_formatter("Page", page_count)
    component_name = plural_name_formatter("Component", component_count)

    assert str(page_count) in result
    assert page_name in result
    assert str(component_count) in result
    assert component_name in result
