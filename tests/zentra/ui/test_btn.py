from pydantic import ValidationError
import pytest
from functools import partial, reduce
from itertools import product
from operator import mul
from typing import Any

from cli.conf.logger import test_logger
from cli.conf.storage import ComponentDetails
from cli.templates.details import COMPONENT_DETAILS_DICT

from tests.mappings.btn_content import BTN_VALID_VALS_MAP
from tests.mappings.ui_imports import VALID_IMPORTS
from tests.templates.helper import component_builder

from zentra.ui.control import Button
from zentra.core.react import LucideIconWithText
from zentra.core.enums.ui import ButtonSize, ButtonVariant


def calc_valid_total(*iterables) -> int:
    return reduce(mul, (len(iterable) for iterable in iterables))


class BtnCompBuilder:
    """A helper class that handles the logic for keeping complicated component test implementations unified."""

    def __init__(
        self,
        iterable_dict: dict[list],
        component_func: callable,
        component_details: ComponentDetails,
    ) -> None:
        self.iterable_dict = iterable_dict
        self.details = component_details
        self.comp_func = component_func

    @staticmethod
    def dict_product(d: dict):
        keys = d.keys()
        values = d.values()
        return [dict(zip(keys, items)) for items in product(*values)]

    def content(self, mapping: list[str] | dict[str, Any]):
        valid_total = 0
        items_list = self.dict_product(self.iterable_dict)
        desired_total = calc_valid_total(items_list)

        for idx, items in enumerate(items_list):
            component = self.comp_func(**items)
            builder = component_builder(component, self.details)
            builder.build()
            content = builder.storage.content

            map_value = mapping[idx] if isinstance(mapping, list) else mapping
            if content == map_value:
                valid_total += 1
            else:
                test_fail_result = content

            test_logger.debug(f"{content}")

        assert (
            valid_total == desired_total
        ), f"({valid_total}/{desired_total}) {test_fail_result} != {map_value}"

    def comp_other(
        self,
        component: Button,
        result_attr: str,
        valid_value: str,
        list_output: bool = False,
    ):
        builder = component_builder(component, self.details)
        builder.build()

        result: str = getattr(builder.storage, result_attr)

        if list_output:
            result = result.split("\n")

        test_logger.debug(f"Result: {result}, Valid: {valid_value}")
        assert result == valid_value, (
            result if list_output else result.split("\n"),
            valid_value if list_output else valid_value.split("\n"),
        )


class TestButton:
    @staticmethod
    def button(**btn_kwargs) -> Button:
        return Button(**btn_kwargs)

    @pytest.fixture
    def iterables(self) -> dict:
        return {
            "variant": [variant.value for variant in ButtonVariant],
            "size": [size.value for size in ButtonSize],
            "disabled": [True, False],
        }

    @pytest.fixture
    def btn_text(self) -> partial:
        return partial(self.button, content="test $tag")

    @pytest.fixture
    def btn_icon(self) -> partial:
        return partial(
            self.button,
            content=LucideIconWithText(name="Italic", text="test $tag"),
        )

    @pytest.fixture
    def btn_text_url(self) -> partial:
        return partial(self.button, content="test $tag", url="https://example.com/")

    @pytest.fixture
    def btn_icon_url(self) -> partial:
        return partial(
            self.button,
            content=LucideIconWithText(name="Italic", text="test $tag"),
            url="https://example.com/",
        )

    @pytest.fixture
    def btn_text_wrapper(self, iterables, btn_text) -> BtnCompBuilder:
        return BtnCompBuilder(
            iterable_dict=iterables,
            component_func=btn_text,
            component_details=COMPONENT_DETAILS_DICT["Button"],
        )

    @pytest.fixture
    def btn_icon_wrapper(self, iterables, btn_icon) -> BtnCompBuilder:
        return BtnCompBuilder(
            iterable_dict=iterables,
            component_func=btn_icon,
            component_details=COMPONENT_DETAILS_DICT["Button"],
        )

    @pytest.fixture
    def btn_text_url_wrapper(self, iterables, btn_text_url) -> BtnCompBuilder:
        return BtnCompBuilder(
            iterable_dict=iterables,
            component_func=btn_text_url,
            component_details=COMPONENT_DETAILS_DICT["Button"],
        )

    @pytest.fixture
    def btn_icon_url_wrapper(self, iterables, btn_icon_url) -> BtnCompBuilder:
        return BtnCompBuilder(
            iterable_dict=iterables,
            component_func=btn_icon_url,
            component_details=COMPONENT_DETAILS_DICT["Button"],
        )

    @staticmethod
    def test_content_str_btn_text(btn_text_wrapper: BtnCompBuilder):
        btn_text_wrapper.content(BTN_VALID_VALS_MAP["text"])

    @staticmethod
    def test_content_str_btn_icon(btn_icon_wrapper: BtnCompBuilder):
        btn_icon_wrapper.content(BTN_VALID_VALS_MAP["icon"])

    @staticmethod
    def test_content_str_btn_text_url(btn_text_url_wrapper: BtnCompBuilder):
        btn_text_url_wrapper.content(BTN_VALID_VALS_MAP["text_url"])

    @staticmethod
    def test_content_str_btn_icon_url(btn_icon_url_wrapper: BtnCompBuilder):
        btn_icon_url_wrapper.content(mapping=BTN_VALID_VALS_MAP["icon_url"])

    @staticmethod
    def test_import_str_simple(btn_text_wrapper: BtnCompBuilder):
        btn_text_wrapper.comp_other(
            Button(content="test $tag"),
            "imports",
            VALID_IMPORTS["button"]["simple"],
        )

    @staticmethod
    def test_import_str_icon(btn_text_wrapper: BtnCompBuilder):
        btn_text_wrapper.comp_other(
            Button(content=LucideIconWithText(name="Loader")),
            "imports",
            VALID_IMPORTS["button"]["icon"],
        )

    @staticmethod
    def test_import_str_icon_url(btn_text_wrapper: BtnCompBuilder):
        btn_text_wrapper.comp_other(
            Button(
                content=LucideIconWithText(name="Loader"), url="https://example.com/"
            ),
            "imports",
            VALID_IMPORTS["button"]["icon_url"],
            list_output=True,
        )

    @staticmethod
    def test_invalid_variant():
        with pytest.raises(ValidationError):
            Button(content="test", variant="test")

    @staticmethod
    def test_invalid_size():
        with pytest.raises(ValidationError):
            Button(content="test", size="test")

    @staticmethod
    def test_invalid_url():
        with pytest.raises(ValidationError):
            Button(content="test", url="not a url")
