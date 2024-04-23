import pytest

from cli.conf.storage import ComponentDetails
from tests.mappings.js import JS_VALID_VALS_MAP
from tests.templates.details import COMPONENT_DETAILS_MAPPING
from tests.templates.helper import js_iterable_content_builder

from zentra.core.base import JSIterable
from zentra.core.html import Div, FigCaption, Figure, HTMLContent
from zentra.core.js import Map
from zentra.nextjs import Image
from zentra.ui.control import Label


class Builder:
    """A helper class that handles the logic for keeping NextJS Component test implementations unified."""

    def __init__(self, model: JSIterable) -> None:
        self.model = model

        self.builder = js_iterable_content_builder(model=self.model)

    def content(self, valid_value: str):
        result: str = "\n".join(self.builder.build())
        assert result == valid_value, (result.split("\n"), valid_value.split("\n"))

    def comp_content(self, valid_value: str, details: ComponentDetails):
        result: str = "\n".join(self.builder.build(details=details))
        assert result == valid_value, (result.split("\n"), valid_value.split("\n"))

    def comp_other(self, result_attr: str, valid_value: str, details: ComponentDetails):
        _ = self.builder.build(details=details)
        result: str = getattr(self.builder.comp_storage, result_attr)
        assert result == valid_value, (result.split("\n"), valid_value.split("\n"))


class TestMap:
    @pytest.fixture
    def js_map_figure(self) -> Map:
        fig = Figure(
            key="$artwork.artist",
            styles="shrink-0",
            img_container_styles="overflow-hidden rounded-md",
            img=Image(
                src="$artwork.art",
                alt="Photo by $artwork.artist",
                styles="aspect-[3/4] h-fit w-fit object-cover",
                width=300,
                height=400,
            ),
            caption=FigCaption(
                styles="pt-2 text-xs text-muted-foreground",
                text=[
                    'Photo by{" "}',
                    HTMLContent(
                        tag="span",
                        styles="font-semibold text-foreground",
                        text="$artwork.artist",
                    ),
                ],
            ),
        )

        return Map(
            obj_name="works",
            param_name="artwork",
            content=fig,
        )

    @pytest.fixture
    def js_map_div(self) -> Map:
        return Map(
            obj_name="tags",
            param_name="tag",
            content=Div(items="Test $tag"),
        )

    @pytest.fixture
    def js_map_image(self) -> Map:
        return Map(
            obj_name="tags",
            param_name="tag",
            content=Image(
                src="$test", width=200, height=200, alt="This is a test image"
            ),
        )

    @pytest.fixture
    def js_map_label(self) -> Map:
        return Map(
            obj_name="tags",
            param_name="tag",
            content=Label(name="test", text="Test $tag"),
        )

    @staticmethod
    def test_missing_details(js_map_label):
        with pytest.raises(AttributeError):
            builder = js_iterable_content_builder(model=js_map_label)
            builder.build()

    @staticmethod
    def test_content_str_figure(js_map_figure: JSIterable):
        builder = Builder(model=js_map_figure)
        builder.content(JS_VALID_VALS_MAP["map"]["content"]["figure"])

    @staticmethod
    def test_content_str_div(js_map_div: JSIterable):
        builder = Builder(model=js_map_div)
        builder.content(JS_VALID_VALS_MAP["map"]["content"]["div"])

    @staticmethod
    def test_content_str_image(js_map_image: JSIterable):
        builder = Builder(model=js_map_image)
        builder.content(JS_VALID_VALS_MAP["map"]["content"]["image"])

    @staticmethod
    def test_content_str_label(js_map_label: JSIterable):
        builder = Builder(model=js_map_label)
        builder.comp_content(
            valid_value=JS_VALID_VALS_MAP["map"]["content"]["label"],
            details=COMPONENT_DETAILS_MAPPING["Label"],
        )

    @staticmethod
    def test_additional_imports_image(js_map_image: JSIterable):
        builder = Builder(model=js_map_image)
        builder.comp_other(
            "imports", JS_VALID_VALS_MAP["map"]["imports"]["image"], details=None
        )
