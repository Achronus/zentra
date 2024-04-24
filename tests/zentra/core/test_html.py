from pydantic import ValidationError
import pytest

from cli.conf.storage import ComponentDetails
from tests.mappings.html import HTML_VALID_VALS_MAP
from tests.templates.details import COMPONENT_DETAILS_MAPPING
from tests.templates.helper import html_content_builder
from zentra.core.base import HTMLTag
from zentra.core.enums.html import HTMLContentTagType
from zentra.core.html import Div, FigCaption, Figure, HTMLContent
from zentra.core.js import Map
from zentra.nextjs import Image, StaticImage
from zentra.ui.control import Label


class Builder:
    """A helper class that handles the logic for keeping HTMLTag model test implementations unified."""

    def __init__(self, model: HTMLTag) -> None:
        self.model = model

        self.builder = html_content_builder(model=model)

    def content(self, valid_value: str):
        result: str = "\n".join(self.builder.build())
        assert result == valid_value, (result.split("\n"), valid_value.split("\n"))

    def comp_content(self, valid_value: str, details: ComponentDetails = None):
        result: str = "\n".join(self.builder.build(details=details))
        assert result == valid_value, (result.split("\n"), valid_value.split("\n"))

    def comp_other(self, result_attr: str, valid_value: str):
        _ = self.builder.build()
        result: str = getattr(self.builder.comp_storage, result_attr)
        assert result == valid_value, (result.split("\n"), valid_value.split("\n"))

    def comp_multi_other(
        self, result_attr: str, valid_value: str, details: ComponentDetails = None
    ):
        _ = self.builder.build(details=details)
        result: list[str] = getattr(self.builder.multi_comp_storage, result_attr)
        assert result == valid_value, (result, valid_value)


class TestHTMLContent:
    @staticmethod
    def test_tags_with_params_and_styles():
        tags = [tag.value for tag in HTMLContentTagType]
        for tag in tags:
            builder = Builder(
                model=HTMLContent(
                    tag=tag,
                    styles="font-semibold text-foreground",
                    text="$artwork.artist",
                )
            )
            builder.content(HTML_VALID_VALS_MAP["html_content"]["content"][tag])

    @staticmethod
    def test_content_text_param_standard():
        builder = Builder(
            model=HTMLContent(
                tag="span",
                styles="font-semibold text-foreground",
                text="This is a long string and I'm $testing it",
            )
        )
        builder.content(HTML_VALID_VALS_MAP["html_content"]["content"]["text_standard"])

    @staticmethod
    def test_content_no_styles():
        builder = Builder(
            model=HTMLContent(
                tag="h1",
                text="This is a long string for $testing",
            )
        )
        builder.content(HTML_VALID_VALS_MAP["html_content"]["content"]["no_styles"])


class TestDiv:
    @pytest.fixture
    def div_with_label(self) -> Div:
        return Div(
            items=Label(name="example", text="A test $label"),
        )

    @pytest.fixture
    def div_with_multi_items(self) -> Div:
        return Div(
            items=[
                "This is a",
                HTMLContent(tag="span", styles="red-500", text="complete $test"),
                Label(name="name", text="First name"),
                Map(
                    obj_name="tags",
                    param_name="tag",
                    content=HTMLContent(tag="h4", text="An epic $tag heading"),
                ),
                Label(name="email", text="Email address"),
            ],
        )

    @staticmethod
    def test_content_str_simple():
        builder = Builder(
            model=Div(items="This is a long test string I'm testing"),
        )
        builder.content(HTML_VALID_VALS_MAP["div"]["content"]["simple"])

    @staticmethod
    def test_content_str_params_with_styles():
        builder = Builder(
            model=Div(items="This is a $test string", styles="w-80"),
        )
        builder.content(HTML_VALID_VALS_MAP["div"]["content"]["with_styles"])

    @staticmethod
    def test_content_str_with_shell():
        builder = Builder(
            model=Div(
                items="This is a shell test",
                shell=True,
            ),
        )
        builder.content(HTML_VALID_VALS_MAP["div"]["content"]["shell"])

    @staticmethod
    def test_content_str_with_map():
        builder = Builder(
            model=Div(
                key="$tag",
                items=Map(
                    obj_name="tags",
                    param_name="tag",
                    content=HTMLContent(tag="h4", text="An epic $tag heading"),
                ),
            ),
        )
        builder.content(HTML_VALID_VALS_MAP["div"]["content"]["map"])

    @staticmethod
    def test_content_str_with_label(div_with_label: Div):
        builder = Builder(model=div_with_label)
        builder.comp_content(
            HTML_VALID_VALS_MAP["div"]["content"]["label"],
            COMPONENT_DETAILS_MAPPING["Label"],
        )

    @staticmethod
    def test_content_str_with_multi_items(div_with_multi_items: Div):
        builder = Builder(model=div_with_multi_items)
        builder.comp_content(
            HTML_VALID_VALS_MAP["div"]["content"]["multi_items"],
            COMPONENT_DETAILS_MAPPING["Label"],
        )

    @staticmethod
    def test_imports_with_label(div_with_label: Div):
        builder = Builder(model=div_with_label)
        builder.comp_multi_other(
            "imports",
            HTML_VALID_VALS_MAP["div"]["imports"]["label"],
            COMPONENT_DETAILS_MAPPING["Label"],
        )

    @staticmethod
    def test_imports_with_multi_items(div_with_multi_items: Div):
        builder = Builder(model=div_with_multi_items)
        builder.comp_multi_other(
            "imports",
            HTML_VALID_VALS_MAP["div"]["imports"]["multi_items"],
            COMPONENT_DETAILS_MAPPING["Label"],
        )

    @staticmethod
    def test_key_param_invalid():
        with pytest.raises(ValidationError):
            Div(items="key error here", key="keyError")


class TestFigCaption:
    @staticmethod
    def test_content_multi_text():
        builder = Builder(
            model=FigCaption(
                styles="pt-2 text-xs text-muted-foreground",
                text=[
                    "Photo by ",
                    HTMLContent(
                        tag="span",
                        styles="font-semibold text-foreground",
                        text="$artwork.artist",
                    ),
                ],
            )
        )
        builder.content(HTML_VALID_VALS_MAP["figcaption"]["content"]["multi_text"])

    @staticmethod
    def test_content_text_html_content():
        builder = Builder(
            model=FigCaption(
                styles="pt-2 text-xs text-muted-foreground",
                text=HTMLContent(text="test $here", tag="h1"),
            )
        )
        builder.content(
            HTML_VALID_VALS_MAP["figcaption"]["content"]["text_html_content"]
        )

    @staticmethod
    def test_content_text_str_standard():
        builder = Builder(
            model=FigCaption(
                styles="pt-2 text-xs text-muted-foreground",
                text="Photo by author",
            )
        )
        builder.content(HTML_VALID_VALS_MAP["figcaption"]["content"]["standard"])

    @staticmethod
    def test_content_text_str_params():
        builder = Builder(
            model=FigCaption(
                styles="pt-2 text-xs text-muted-foreground",
                text="Photo by $author",
            )
        )
        builder.content(
            HTML_VALID_VALS_MAP["figcaption"]["content"]["standard_with_params"]
        )

    @staticmethod
    def test_content_text_str_standard_no_styles():
        builder = Builder(
            model=FigCaption(
                text="Photo by author",
            )
        )
        builder.content(HTML_VALID_VALS_MAP["figcaption"]["content"]["no_styles"])


class TestFigure:
    @pytest.fixture
    def figure_full(self) -> Figure:
        return Figure(
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
                    "Photo by ",
                    HTMLContent(
                        tag="span",
                        styles="font-semibold text-foreground",
                        text="$artwork.artist",
                    ),
                ],
            ),
        )

    @pytest.fixture
    def figure_static_img(self) -> Figure:
        return Figure(
            img=Image(
                src=StaticImage(name="profilePic", path="./me.png"),
                alt="Photo by me",
                width=300,
                height=400,
            ),
            caption=FigCaption(
                text=[
                    "Photo by ",
                    HTMLContent(
                        tag="span",
                        text="An awesome person",
                    ),
                ],
            ),
        )

    @staticmethod
    def test_content_full(figure_full: Figure):
        builder = Builder(model=figure_full)
        builder.content(HTML_VALID_VALS_MAP["figure"]["content"]["complete"])

    @staticmethod
    def test_content_no_key():
        builder = Builder(
            model=Figure(
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
                        "Photo by ",
                        HTMLContent(
                            tag="span",
                            styles="font-semibold text-foreground",
                            text="$artwork.artist",
                        ),
                    ],
                ),
            )
        )
        builder.content(HTML_VALID_VALS_MAP["figure"]["content"]["no_key"])

    @staticmethod
    def test_content_no_styles():
        builder = Builder(
            model=Figure(
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
                    text=HTMLContent(
                        tag="h1",
                        styles="font-semibold text-foreground",
                        text="Photo by me",
                    ),
                ),
            )
        )
        builder.content(HTML_VALID_VALS_MAP["figure"]["content"]["no_styles"])

    @staticmethod
    def test_content_simple_basic_url():
        builder = Builder(
            model=Figure(
                img=Image(
                    src="$artwork.art",
                    alt="Photo by me",
                    width=300,
                    height=400,
                ),
                caption=FigCaption(
                    text="Photo by author",
                ),
            )
        )
        builder.content(HTML_VALID_VALS_MAP["figure"]["content"]["simple_basic_url"])

    @staticmethod
    def test_content_simple_static_img(figure_static_img: Figure):
        builder = Builder(model=figure_static_img)
        builder.content(HTML_VALID_VALS_MAP["figure"]["content"]["simple_static_img"])

    @staticmethod
    def test_basic_import(figure_full: Figure):
        builder = Builder(model=figure_full)
        builder.comp_other("imports", HTML_VALID_VALS_MAP["figure"]["imports"]["basic"])

    @staticmethod
    def test_simple_static_img_import(figure_static_img: Figure):
        builder = Builder(model=figure_static_img)
        builder.comp_other(
            "imports", HTML_VALID_VALS_MAP["figure"]["imports"]["static_img"]
        )

    @staticmethod
    def test_key_param_invalid():
        with pytest.raises(ValidationError):
            Figure(
                key="testFail",
                img=Image(
                    src="$artwork.art",
                    alt="Photo by me",
                    width=300,
                    height=400,
                ),
                caption=FigCaption(
                    text="Photo by author",
                ),
            )
