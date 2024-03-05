import re
from hypothesis import given
from hypothesis.strategies import text, characters

from cli.conf.format import name_from_camel_case


@given(text(alphabet=characters(whitelist_categories=("Lu", "Ll", "Nd")), min_size=10))
def test_name_from_camel_case_hypothesis(input_string):
    result = name_from_camel_case(input_string)

    expected_result = re.sub("([a-z0-9])([A-Z])", r"\1-\2", input_string).lower()
    assert result == expected_result
