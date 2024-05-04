import pytest

from tests.mappings.ui_imports import VALID_IMPORTS
from tests.mappings.ui_vals import VALID_VALS_MAP
from tests.templates.details import COMPONENT_DETAILS_MAPPING
from tests.templates.helper import SimpleCompBuilder, ParentCompBuilder

from zentra.nextjs import StaticImage
from zentra.ui.presentation import Avatar, AvatarImage, Separator


class TestSeparator:
    @pytest.fixture
    def separator(self) -> Separator:
        return Separator()

    @pytest.fixture
    def separator_full(self) -> Separator:
        return Separator(styles="mx-4", orientation="horizontal")

    @pytest.fixture
    def wrapper(self, separator: Separator) -> SimpleCompBuilder:
        return SimpleCompBuilder(separator, COMPONENT_DETAILS_MAPPING["Separator"])

    @pytest.fixture
    def wrapper_full(self, separator_full: Separator) -> SimpleCompBuilder:
        return SimpleCompBuilder(separator_full, COMPONENT_DETAILS_MAPPING["Separator"])

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
            img=AvatarImage(src="https://github.com/shadcn.png", alt="@shadcn"),
            fallback_text="CN",
        )

    @pytest.fixture
    def avatar_path(self) -> Avatar:
        return Avatar(
            img=AvatarImage(src="/profile.png", alt="Awesome photo of $me"),
            fallback_text="AA",
        )

    @pytest.fixture
    def avatar_static(self) -> Avatar:
        return Avatar(
            img=AvatarImage(
                src=StaticImage(name="profilePic", path="./me.png"),
                alt="Awesome photo of $me",
            ),
            fallback_text="AA",
        )

    @pytest.fixture
    def wrapper_url(self, avatar_url: Avatar) -> ParentCompBuilder:
        return ParentCompBuilder(avatar_url)

    @pytest.fixture
    def wrapper_path(self, avatar_path: Avatar) -> ParentCompBuilder:
        return ParentCompBuilder(avatar_path)

    @pytest.fixture
    def wrapper_static(self, avatar_static: Avatar) -> ParentCompBuilder:
        return ParentCompBuilder(avatar_static)

    @staticmethod
    def test_content_str_url(wrapper_url: ParentCompBuilder):
        wrapper_url.content(VALID_VALS_MAP["avatar"]["content"]["url"])

    @staticmethod
    def test_content_str_path(wrapper_path: ParentCompBuilder):
        wrapper_path.content(VALID_VALS_MAP["avatar"]["content"]["path"])

    @staticmethod
    def test_content_str_static(wrapper_static: ParentCompBuilder):
        wrapper_static.content(VALID_VALS_MAP["avatar"]["content"]["static_img"])

    @staticmethod
    def test_import_str_url(wrapper_url: ParentCompBuilder):
        wrapper_url.comp_other("imports", VALID_IMPORTS["avatar"]["path_n_url"])

    @staticmethod
    def test_import_str_path(wrapper_path: ParentCompBuilder):
        wrapper_path.comp_other("imports", VALID_IMPORTS["avatar"]["path_n_url"])

    @staticmethod
    def test_import_str_static(wrapper_static: ParentCompBuilder):
        wrapper_static.comp_other(
            "imports", VALID_IMPORTS["avatar"]["static_img"], list_output=True
        )
