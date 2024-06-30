from pydantic import ValidationError
import pytest

from tests.mappings.html import HTML_VALID_VALS_MAP
from tests.templates.helper import SimpleCompBuilder
from zentra_models.core.enums.html import HTMLContentTagType
from zentra_models.core.html import Div, FigCaption, Figure, HTMLContent
from zentra_models.core.js import Map
from zentra_models.nextjs import Image, StaticImage
from zentra_models.ui.control import Label


class TestHTMLContent:
    def tag_with_params_and_styles(self, tag: str) -> HTMLContent:
        return HTMLContent(
            tag=tag, styles="font-semibold text-foreground", text="$.artwork.artist"
        )

    @pytest.fixture
    def tag_text_param_standard(self) -> HTMLContent:
        return HTMLContent(
            tag="span",
            styles="font-semibold text-foreground",
            text="This is a long string and I'm $.testing it",
        )

    @pytest.fixture
    def tag_no_styles(self) -> HTMLContent:
        return HTMLContent(
            tag="h1",
            text="This is a long string for $.testing",
        )

    def test_content_tags_with_params_and_styles(self):
        tags = [tag.value for tag in HTMLContentTagType]
        for tag in tags:
            model = self.tag_with_params_and_styles(tag)

            builder = SimpleCompBuilder(model)
            builder.run("content", HTML_VALID_VALS_MAP["html_content"]["content"][tag])

    @staticmethod
    def test_content_text_param_standard(tag_text_param_standard: HTMLContent):
        builder = SimpleCompBuilder(tag_text_param_standard)
        builder.run(
            "content", HTML_VALID_VALS_MAP["html_content"]["content"]["text_standard"]
        )

    @staticmethod
    def test_content_no_styles(tag_no_styles: HTMLContent):
        builder = SimpleCompBuilder(tag_no_styles)
        builder.run(
            "content", HTML_VALID_VALS_MAP["html_content"]["content"]["no_styles"]
        )


class TestDiv:
    @pytest.fixture
    def div_with_label(self) -> Div:
        return Div(
            content=Label(name="example", text="A test $.label"),
        )

    @pytest.fixture
    def div_with_multi_items(self) -> Div:
        return Div(
            content=[
                "This is a",
                HTMLContent(tag="span", styles="red-500", text="complete $.test"),
                Label(name="name", text="First name"),
                Map(
                    obj_name="tags",
                    param_name="tag",
                    content=HTMLContent(tag="h4", text="An epic $.tag heading"),
                ),
                Label(name="email", text="Email address"),
            ],
        )

    @staticmethod
    def test_content_str_simple():
        builder = SimpleCompBuilder(
            Div(content="This is a long test string I'm testing"),
        )
        builder.run("content", HTML_VALID_VALS_MAP["div"]["content"]["simple"])

    @staticmethod
    def test_content_str_params_with_styles():
        builder = SimpleCompBuilder(
            Div(content="This is a $.test string", styles="w-80"),
        )
        builder.run("content", HTML_VALID_VALS_MAP["div"]["content"]["with_styles"])

    @staticmethod
    def test_content_str_with_shell():
        builder = SimpleCompBuilder(
            Div(
                content="This is a shell test",
                fragment=True,
            ),
        )
        builder.run("content", HTML_VALID_VALS_MAP["div"]["content"]["shell"])

    @staticmethod
    def test_content_str_with_map():
        builder = SimpleCompBuilder(
            Div(
                key="$.tag",
                content=Map(
                    obj_name="tags",
                    param_name="tag",
                    content=HTMLContent(tag="h4", text="An epic $.tag heading"),
                ),
            ),
        )
        builder.run("content", HTML_VALID_VALS_MAP["div"]["content"]["map"])

    @staticmethod
    def test_content_str_with_label(div_with_label: Div):
        builder = SimpleCompBuilder(div_with_label)
        builder.run("content", HTML_VALID_VALS_MAP["div"]["content"]["label"])

    @staticmethod
    def test_content_str_with_multi_items(div_with_multi_items: Div):
        builder = SimpleCompBuilder(div_with_multi_items)
        builder.run("content", HTML_VALID_VALS_MAP["div"]["content"]["multi_items"])

    @staticmethod
    def test_content_str_with_multi_items_html():
        builder = SimpleCompBuilder(
            Div(
                styles="w-8 h-12",
                content=[
                    HTMLContent(tag="h1", text="Test h1 $.tag"),
                    Figure(
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
                    ),
                    HTMLContent(tag="h2", text="Test h2 tag"),
                ],
            )
        )
        builder.run("content", HTML_VALID_VALS_MAP["div"]["content"]["multi_html"])

    @staticmethod
    def test_imports_with_label(div_with_label: Div):
        builder = SimpleCompBuilder(div_with_label)
        builder.run("imports", HTML_VALID_VALS_MAP["div"]["imports"]["label"])

    @staticmethod
    def test_imports_with_multi_items(div_with_multi_items: Div):
        builder = SimpleCompBuilder(div_with_multi_items)
        builder.run("imports", HTML_VALID_VALS_MAP["div"]["imports"]["multi_items"])

    @staticmethod
    def test_key_param_invalid():
        with pytest.raises(ValidationError):
            Div(content="key error here", key="keyError")


class TestFigCaption:
    @staticmethod
    def test_content_multi_text():
        builder = SimpleCompBuilder(
            FigCaption(
                styles="pt-2 text-xs text-muted-foreground",
                text=[
                    "Photo by ",
                    HTMLContent(
                        tag="span",
                        styles="font-semibold text-foreground",
                        text="$.artwork.artist",
                    ),
                ],
            )
        )
        builder.run(
            "content", HTML_VALID_VALS_MAP["figcaption"]["content"]["multi_text"]
        )

    @staticmethod
    def test_content_text_html_content():
        builder = SimpleCompBuilder(
            FigCaption(
                styles="pt-2 text-xs text-muted-foreground",
                text=HTMLContent(text="test $.here", tag="h1"),
            )
        )
        builder.run(
            "content", HTML_VALID_VALS_MAP["figcaption"]["content"]["text_html_content"]
        )

    @staticmethod
    def test_content_text_str_standard():
        builder = SimpleCompBuilder(
            FigCaption(
                styles="pt-2 text-xs text-muted-foreground",
                text="Photo by author",
            )
        )
        builder.run("content", HTML_VALID_VALS_MAP["figcaption"]["content"]["standard"])

    @staticmethod
    def test_content_text_str_params():
        builder = SimpleCompBuilder(
            FigCaption(
                styles="pt-2 text-xs text-muted-foreground",
                text="Photo by $.author",
            )
        )
        builder.run(
            "content",
            HTML_VALID_VALS_MAP["figcaption"]["content"]["standard_with_params"],
        )

    @staticmethod
    def test_content_text_str_standard_no_styles():
        builder = SimpleCompBuilder(
            FigCaption(
                text="Photo by author",
            )
        )
        builder.run(
            "content", HTML_VALID_VALS_MAP["figcaption"]["content"]["no_styles"]
        )


class TestFigure:
    @pytest.fixture
    def figure_full(self) -> Figure:
        return Figure(
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
        builder = SimpleCompBuilder(figure_full)
        builder.run("content", HTML_VALID_VALS_MAP["figure"]["content"]["complete"])

    @staticmethod
    def test_content_no_key():
        builder = SimpleCompBuilder(
            Figure(
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
        )
        builder.run("content", HTML_VALID_VALS_MAP["figure"]["content"]["no_key"])

    @staticmethod
    def test_content_no_styles():
        builder = SimpleCompBuilder(
            Figure(
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
                    text=HTMLContent(
                        tag="h1",
                        styles="font-semibold text-foreground",
                        text="Photo by me",
                    ),
                ),
            )
        )
        builder.run("content", HTML_VALID_VALS_MAP["figure"]["content"]["no_styles"])

    @staticmethod
    def test_content_simple_basic_url():
        builder = SimpleCompBuilder(
            Figure(
                img=Image(
                    src="$.artwork.art",
                    alt="Photo by me",
                    width=300,
                    height=400,
                ),
                caption=FigCaption(
                    text="Photo by author",
                ),
            )
        )
        builder.run(
            "content", HTML_VALID_VALS_MAP["figure"]["content"]["simple_basic_url"]
        )

    @staticmethod
    def test_content_simple_static_img(figure_static_img: Figure):
        builder = SimpleCompBuilder(figure_static_img)
        builder.run(
            "content", HTML_VALID_VALS_MAP["figure"]["content"]["simple_static_img"]
        )

    @staticmethod
    def test_basic_import(figure_full: Figure):
        builder = SimpleCompBuilder(figure_full)
        builder.run("imports", HTML_VALID_VALS_MAP["figure"]["imports"]["basic"])

    @staticmethod
    def test_simple_static_img_import(figure_static_img: Figure):
        builder = SimpleCompBuilder(figure_static_img)
        builder.run("imports", HTML_VALID_VALS_MAP["figure"]["imports"]["static_img"])

    @staticmethod
    def test_key_param_invalid():
        with pytest.raises(ValidationError):
            Figure(
                key="testFail",
                img=Image(
                    src="$.artwork.art",
                    alt="Photo by me",
                    width=300,
                    height=400,
                ),
                caption=FigCaption(
                    text="Photo by author",
                ),
            )
