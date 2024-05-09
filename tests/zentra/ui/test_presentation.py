import pytest

from cli.templates.details import COMPONENT_DETAILS_DICT

from tests.mappings.ui_imports import VALID_IMPORTS
from tests.mappings.ui_vals import VALID_VALS_MAP
from tests.templates.helper import SimpleCompBuilder

from zentra.nextjs import StaticImage
from zentra.ui.presentation import Avatar, Badge, Separator


class TestSeparator:
    @pytest.fixture
    def separator(self) -> Separator:
        return Separator()

    @pytest.fixture
    def separator_full(self) -> Separator:
        return Separator(styles="mx-4", orientation="horizontal")

    @pytest.fixture
    def wrapper(self, separator: Separator) -> SimpleCompBuilder:
        return SimpleCompBuilder(separator, COMPONENT_DETAILS_DICT["Separator"])

    @pytest.fixture
    def wrapper_full(self, separator_full: Separator) -> SimpleCompBuilder:
        return SimpleCompBuilder(separator_full, COMPONENT_DETAILS_DICT["Separator"])

    @staticmethod
    def test_content_str(wrapper: SimpleCompBuilder):
        wrapper.run("content", VALID_VALS_MAP["separator"]["content"]["simple"])

    @staticmethod
    def test_content_str_full(wrapper_full: SimpleCompBuilder):
        wrapper_full.run("content", VALID_VALS_MAP["separator"]["content"]["full"])

    @staticmethod
    def test_import_str(wrapper: SimpleCompBuilder):
        wrapper.run("imports", VALID_IMPORTS["separator"])


class TestAvatar:
    @pytest.fixture
    def avatar_url(self) -> Avatar:
        return Avatar(
            src="https://github.com/shadcn.png",
            alt="@shadcn",
            fallback_text="CN",
        )

    @pytest.fixture
    def avatar_path(self) -> Avatar:
        return Avatar(
            src="/profile.png",
            alt="Awesome photo of $me",
            fallback_text="AA",
        )

    @pytest.fixture
    def avatar_static(self) -> Avatar:
        return Avatar(
            src=StaticImage(name="profilePic", path="./me.png"),
            alt="Awesome photo of $me",
            fallback_text="AA",
        )

    @pytest.fixture
    def wrapper_url(self, avatar_url: Avatar) -> SimpleCompBuilder:
        return SimpleCompBuilder(avatar_url, COMPONENT_DETAILS_DICT["Avatar"])

    @pytest.fixture
    def wrapper_path(self, avatar_path: Avatar) -> SimpleCompBuilder:
        return SimpleCompBuilder(avatar_path, COMPONENT_DETAILS_DICT["Avatar"])

    @pytest.fixture
    def wrapper_static(self, avatar_static: Avatar) -> SimpleCompBuilder:
        return SimpleCompBuilder(avatar_static, COMPONENT_DETAILS_DICT["Avatar"])

    @staticmethod
    def test_content_str_url(wrapper_url: SimpleCompBuilder):
        wrapper_url.run("content", VALID_VALS_MAP["avatar"]["content"]["url"])

    @staticmethod
    def test_content_str_path(wrapper_path: SimpleCompBuilder):
        wrapper_path.run("content", VALID_VALS_MAP["avatar"]["content"]["path"])

    @staticmethod
    def test_content_str_static(wrapper_static: SimpleCompBuilder):
        wrapper_static.run("content", VALID_VALS_MAP["avatar"]["content"]["static_img"])

    @staticmethod
    def test_import_str_url(wrapper_url: SimpleCompBuilder):
        wrapper_url.run("imports", VALID_IMPORTS["avatar"]["path_n_url"])

    @staticmethod
    def test_import_str_path(wrapper_path: SimpleCompBuilder):
        wrapper_path.run("imports", VALID_IMPORTS["avatar"]["path_n_url"])

    @staticmethod
    def test_import_str_static(wrapper_static: SimpleCompBuilder):
        wrapper_static.run(
            "imports", VALID_IMPORTS["avatar"]["static_img"], list_output=True
        )


class TestBadge:
    @pytest.fixture
    def badge(self) -> Badge:
        return Badge(text="Badge")

    @pytest.fixture
    def badge_outline(self) -> Badge:
        return Badge(text="Badge", variant="outline")

    @pytest.fixture
    def wrapper(self, badge: Badge) -> SimpleCompBuilder:
        return SimpleCompBuilder(badge, COMPONENT_DETAILS_DICT["Badge"])

    @pytest.fixture
    def wrapper_outline(self, badge_outline: Badge) -> SimpleCompBuilder:
        return SimpleCompBuilder(badge_outline, COMPONENT_DETAILS_DICT["Badge"])

    @staticmethod
    def test_content_str(wrapper: SimpleCompBuilder):
        wrapper.run("content", VALID_VALS_MAP["badge"]["content"]["simple"])

    @staticmethod
    def test_content_str_outline(wrapper_outline: SimpleCompBuilder):
        wrapper_outline.run("content", VALID_VALS_MAP["badge"]["content"]["variant"])

    @staticmethod
    def test_import_str(wrapper: SimpleCompBuilder):
        wrapper.run("imports", VALID_IMPORTS["badge"])
