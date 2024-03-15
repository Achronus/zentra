import re
from hypothesis import given
from hypothesis.strategies import text, characters, sampled_from, integers

from cli.conf.format import (
    name_from_camel_case,
    name_to_plural,
    set_colour,
)


@given(text(alphabet=characters(whitelist_categories=("Lu", "Ll", "Nd")), min_size=10))
def test_name_from_camel_case(input_string):
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
def test_name_to_plural(name, count):
    result = name_to_plural(name, count)
    if count == 1:
        assert result == name
    else:
        assert result == f"{name}s"
