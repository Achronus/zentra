import pytest

from cli.conf.constants import GITHUB_COMPONENTS_DIR, GITHUB_INIT_ASSETS_DIR
from cli.templates.retrieval import (
    CodeRetriever,
    ComponentRetriever,
    ZentraSetupRetriever,
)
from tests.mappings.retrieval import (
    COMPONENT_GITHUB_VALID,
    ZENTRA_INIT_CODE_VALID,
    ZENTRA_INIT_VALID,
)


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

        ui = retriever.storage.ui
        ui_checks = [
            ui.base == COMPONENT_GITHUB_VALID["ui_storage"]["base"],
            ui.templates == COMPONENT_GITHUB_VALID["ui_storage"]["templates"],
            ui.lib == COMPONENT_GITHUB_VALID["ui_storage"]["lib"],
        ]

        ut = retriever.storage.uploadthing
        ut_checks = [
            ut.base == COMPONENT_GITHUB_VALID["ut_storage"]["base"],
            ut.templates == COMPONENT_GITHUB_VALID["ut_storage"]["templates"],
            ut.lib == COMPONENT_GITHUB_VALID["ut_storage"]["lib"],
        ]
        checks = ui_checks + ut_checks
        assert all(checks)


class TestZentraSetupRetriever:
    @pytest.fixture
    def retriever(self) -> ZentraSetupRetriever:
        return ZentraSetupRetriever(url=GITHUB_INIT_ASSETS_DIR)

    @staticmethod
    def test_extract(retriever: ZentraSetupRetriever):
        retriever.extract()

        files = retriever.storage
        checks = [
            files.config == ZENTRA_INIT_VALID["config"],
            files.demo_dir_path == ZENTRA_INIT_VALID["demo_dir_path"],
            files.demo_filenames == ZENTRA_INIT_VALID["demo_filenames"],
        ]
        assert all(checks)


class TestCodeRetriever:
    @pytest.fixture
    def retriever(self) -> CodeRetriever:
        URL = "https://github.com/Astrum-AI/Zentra/blob/ui-components/init/__init__.py"
        return CodeRetriever(url=URL)

    @staticmethod
    def test_code(retriever: CodeRetriever):
        result = retriever.code(retriever.url)
        assert result == ZENTRA_INIT_CODE_VALID["rawlines"]

    @staticmethod
    def test_extract(retriever: CodeRetriever):
        result = retriever.extract()
        assert result == ZENTRA_INIT_CODE_VALID["full_file"]
