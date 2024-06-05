import pytest

from tests.mappings.js import JS_VALID_VALS_MAP

from tests.templates.helper import SimpleCompBuilder
from zentra.core.html import Div, FigCaption, Figure, HTMLContent
from zentra.core.js import Map
from zentra.nextjs import Image
from zentra.ui.control import Label


class TestMap:
    @pytest.fixture
    def js_map_figure(self) -> Map:
        fig = Figure(
            key="$.artwork.artist",
            styles="shrink-0",
            img_container_styles="overflow-hidden rounded-md",
            img=Image(
                src="$.artwork.art",
                alt="Photo by $.artwork.artist",
                styles="aspect-[3/4] h-fit w-fit object-cover",
                width=300,
                height=400,
            ),
            caption=FigCaption(
                styles="pt-2 text-xs text-muted-foreground",
                text=[
                    "Photo by ",
                    HTMLContent(
                        tag="span",
                        styles="font-semibold text-foreground",
                        text="$.artwork.artist",
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
            content=Div(content="Test $.tag"),
        )

    @pytest.fixture
    def js_map_image(self) -> Map:
        return Map(
            obj_name="tags",
            param_name="tag",
            content=Image(
                src="$.test", width=200, height=200, alt="This is a test image"
            ),
        )

    @pytest.fixture
    def js_map_label(self) -> Map:
        return Map(
            obj_name="tags",
            param_name="tag",
            content=Label(name="test", text="Test $.tag"),
        )

    @staticmethod
    def test_content_str_figure(js_map_figure: Map):
        builder = SimpleCompBuilder(js_map_figure)
        builder.run("content", JS_VALID_VALS_MAP["map"]["content"]["figure"])

    @staticmethod
    def test_content_str_div(js_map_div: Map):
        builder = SimpleCompBuilder(js_map_div)
        builder.run("content", JS_VALID_VALS_MAP["map"]["content"]["div"])

    @staticmethod
    def test_content_str_image(js_map_image: Map):
        builder = SimpleCompBuilder(js_map_image)
        builder.run("content", JS_VALID_VALS_MAP["map"]["content"]["image"])

    @staticmethod
    def test_content_str_label(js_map_label: Map):
        builder = SimpleCompBuilder(js_map_label)
        builder.run("content", JS_VALID_VALS_MAP["map"]["content"]["label"])

    @staticmethod
    def test_additional_imports_image(js_map_image: Map):
        builder = SimpleCompBuilder(js_map_image)
        builder.run("imports", JS_VALID_VALS_MAP["map"]["imports"]["image"])
