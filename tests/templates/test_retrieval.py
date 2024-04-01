import pytest

from cli.conf.constants import GITHUB_COMPONENTS_DIR, GITHUB_INIT_ASSETS_DIR
from cli.templates.retrieval import ComponentRetriever, ZentraSetupRetriever
from tests.mappings.retrieval import COMPONENT_GITHUB_VALID, ZENTRA_INIT_VALID


class TestComponentRetriever:
    @pytest.fixture
    def retriever(self) -> ComponentRetriever:
        return ComponentRetriever(url=GITHUB_COMPONENTS_DIR)

    @staticmethod
    def test_dirnames(retriever: ComponentRetriever):
        result = retriever.set_dirnames(retriever.url)
        assert result == COMPONENT_GITHUB_VALID["root_dirs"]

    @staticmethod
    def test_extract_names(retriever: ComponentRetriever):
        result = retriever.extract_names(retriever.url)
        assert result == COMPONENT_GITHUB_VALID["file_folder_list"]

    @staticmethod
    def test_extract(retriever: ComponentRetriever):
        retriever.extract()

        ui_checks = [
            retriever.ui.base == COMPONENT_GITHUB_VALID["ui_storage"]["base"],
            retriever.ui.templates == COMPONENT_GITHUB_VALID["ui_storage"]["templates"],
            retriever.ui.lib == COMPONENT_GITHUB_VALID["ui_storage"]["lib"],
        ]

        ut_checks = [
            retriever.uploadthing.base == COMPONENT_GITHUB_VALID["ut_storage"]["base"],
            retriever.uploadthing.templates
            == COMPONENT_GITHUB_VALID["ut_storage"]["templates"],
            retriever.uploadthing.lib == COMPONENT_GITHUB_VALID["ut_storage"]["lib"],
        ]
        checks = ui_checks + ut_checks
        assert all(checks)


class TestZentraSetupRetriever:
    @pytest.fixture
    def retriever(self) -> ZentraSetupRetriever:
        return ZentraSetupRetriever(url=GITHUB_INIT_ASSETS_DIR)

    def test_extract(retriever: ZentraSetupRetriever):
        retriever.extract()

        checks = [
            retriever.config == ZENTRA_INIT_VALID["config"],
            retriever.demo_dir_path == ZENTRA_INIT_VALID["demo_dir_path"],
            retriever.demo_filenames == ZENTRA_INIT_VALID["demo_filenames"],
        ]
        assert all(checks)
