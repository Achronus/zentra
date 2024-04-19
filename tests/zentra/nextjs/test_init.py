import pytest

from tests.mappings.ui_imports import NEXTJS_VALID_IMPORTS
from tests.mappings.ui_simple import NEXTJS_VALID_VALS_MAP
from tests.templates.helper import nextjs_component_builder

from zentra.core import Component
from zentra.nextjs import Image, StaticImage

from pydantic import ValidationError


class Builder:
    """A helper class that handles the logic for keeping NextJS Component test implementations unified."""

    def __init__(self, component: Component) -> None:
        self.component = component

    def run(self, result_attr: str, valid_value: str):
        builder = nextjs_component_builder(self.component)
        builder.build()

        result: str = getattr(builder.storage, result_attr)
        assert result == valid_value, (result.split("\n"), valid_value.split("\n"))


class TestImage:
    @pytest.fixture
    def image(self) -> Image:
        return Image(
            src="$artwork.art",
            alt="Photo by $artwork.artist",
            styles="aspect-[3/4] h-fit w-fit object-cover",
            width=300,
            height=400,
        )

    @pytest.fixture
    def image_static_src(self) -> Image:
        return Image(
            src=StaticImage(name="profilePic", path="./me.png"),
            alt="Photo by $artwork.artist",
            width=300,
            height=400,
        )

    @staticmethod
    def test_imports_standard(image: Image):
        builder = Builder(image)
        builder.run("imports", NEXTJS_VALID_IMPORTS["image"]["standard"])

    @staticmethod
    def test_imports_with_extra(image_static_src: Image):
        builder = Builder(image_static_src)
        builder.run("imports", NEXTJS_VALID_IMPORTS["image"]["static_src"])

    @staticmethod
    def test_attributes_standard(image: Image):
        builder = Builder(image)
        builder.run("attributes", NEXTJS_VALID_VALS_MAP["image"]["attributes"])

    @staticmethod
    def test_content_standard(image: Image):
        builder = Builder(image)
        builder.run("content", NEXTJS_VALID_VALS_MAP["image"]["content"]["standard"])

    @staticmethod
    def test_content_no_styles():
        img = Image(
            src="$artwork.art",
            alt="Photo by $artwork.artist",
            width=300,
            height=400,
        )
        builder = Builder(img)
        builder.run("content", NEXTJS_VALID_VALS_MAP["image"]["content"]["no_styles"])

    @staticmethod
    def test_content_with_url():
        img = Image(
            src="http://example.com",
            alt="Photo by $artwork.artist",
            width=300,
            height=400,
        )
        builder = Builder(img)
        builder.run("content", NEXTJS_VALID_VALS_MAP["image"]["content"]["with_url"])

    @staticmethod
    def test_content_static_alt_text():
        img = Image(
            src="http://example.com",
            alt="Photo by author",
            width=300,
            height=400,
        )
        builder = Builder(img)
        builder.run("content", NEXTJS_VALID_VALS_MAP["image"]["content"]["basic_alt"])

    @staticmethod
    def test_content_static_img_src(image_static_src: Image):
        builder = Builder(image_static_src)
        builder.run(
            "content", NEXTJS_VALID_VALS_MAP["image"]["content"]["static_img_src"]
        )

    @staticmethod
    def test_content_src_error():
        with pytest.raises(ValidationError):
            Image(
                src="artwork",
                alt="Photo by $artwork.artist",
                width=300,
                height=400,
            )
