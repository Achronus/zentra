import pytest

from tests.mappings.ui_imports import NEXTJS_VALID_IMPORTS
from tests.mappings.ui_vals import NEXTJS_VALID_VALS_MAP
from tests.templates.helper import nextjs_component_builder

from zentra.core import Component
from zentra.nextjs import Image, Link, StaticImage, Url

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
    def test_content_static_basic_path():
        img = Image(
            src="/profile.png",
            alt="Photo by author",
            width=300,
            height=400,
        )
        builder = Builder(img)
        builder.run("content", NEXTJS_VALID_VALS_MAP["image"]["content"]["basic_path"])

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


class TestStaticImage:
    @pytest.fixture
    def image(self) -> StaticImage:
        return StaticImage(name="profilePic", path="./me.png")

    @staticmethod
    def test_name_uppercase_error():
        with pytest.raises(ValidationError):
            StaticImage(name="PROFILE", path="./me.png")

    @staticmethod
    def test_name_multi_word_error():
        with pytest.raises(ValidationError):
            StaticImage(name="profile pic", path="./me.png")

    @staticmethod
    def test_name_pascalcase_error():
        with pytest.raises(ValidationError):
            StaticImage(name="ProfilePic", path="./me.png")


class TestLink:
    @pytest.fixture
    def link(self) -> Link:
        return Link(href="/dashboard")

    @staticmethod
    def test_imports_valid(link: Link):
        builder = Builder(link)
        builder.run("imports", NEXTJS_VALID_IMPORTS["link"])

    @staticmethod
    def test_content_required(link: Link):
        builder = Builder(link)
        builder.run("content", NEXTJS_VALID_VALS_MAP["link"]["content"]["standard"])

    @staticmethod
    def test_content_with_text():
        link = Link(href="/dashboard", text="Dashboard")
        builder = Builder(link)
        builder.run("content", NEXTJS_VALID_VALS_MAP["link"]["content"]["with_text"])

    @staticmethod
    def test_content_full():
        link = Link(
            href=Url(
                pathname="/dashboard",
                query={"name": "test"},
            ),
            text="Dashboard",
            styles="rounded-md border",
            target="_blank",
            replace=True,
            scroll=False,
            prefetch=False,
        )
        builder = Builder(link)
        builder.run("content", NEXTJS_VALID_VALS_MAP["link"]["content"]["full"])

    @staticmethod
    def test_attr_styles():
        link = Link(href="/dashboard", styles="rounded-md border")
        builder = Builder(link)
        builder.run("attributes", NEXTJS_VALID_VALS_MAP["link"]["attributes"]["styles"])

    @staticmethod
    def test_attr_target():
        link = Link(href="/dashboard", target="_blank")
        builder = Builder(link)
        builder.run("attributes", NEXTJS_VALID_VALS_MAP["link"]["attributes"]["target"])

    @staticmethod
    def test_attr_replace():
        link = Link(href="/dashboard", replace=True)
        builder = Builder(link)
        builder.run(
            "attributes", NEXTJS_VALID_VALS_MAP["link"]["attributes"]["replace"]
        )

    @staticmethod
    def test_attr_scroll():
        link = Link(href="/dashboard", scroll=False)
        builder = Builder(link)
        builder.run("attributes", NEXTJS_VALID_VALS_MAP["link"]["attributes"]["scroll"])

    @staticmethod
    def test_attr_prefetch_false():
        link = Link(href="/dashboard", prefetch=False)
        builder = Builder(link)
        builder.run(
            "attributes", NEXTJS_VALID_VALS_MAP["link"]["attributes"]["prefetch_false"]
        )

    @staticmethod
    def test_attr_prefetch_true():
        link = Link(href="/dashboard", prefetch=True)
        builder = Builder(link)
        builder.run(
            "attributes", NEXTJS_VALID_VALS_MAP["link"]["attributes"]["prefetch_true"]
        )

    @staticmethod
    def test_attr_href_url():
        link = Link(
            href=Url(
                pathname="/dashboard",
                query={"name": "test"},
            ),
        )
        builder = Builder(link)
        builder.run(
            "attributes", NEXTJS_VALID_VALS_MAP["link"]["attributes"]["href_url"]
        )

    @staticmethod
    def test_attr_href_url_multi_query():
        link = Link(
            href=Url(
                pathname="/dashboard",
                query={"name": "test", "second": "test2"},
            ),
        )
        builder = Builder(link)
        builder.run(
            "attributes",
            NEXTJS_VALID_VALS_MAP["link"]["attributes"]["href_url_multi_query"],
        )


class TestUrl:
    @staticmethod
    def test_pathname_invalid():
        with pytest.raises(ValidationError):
            Url(
                pathname="dashboard",
                query={"name": "test"},
            )
