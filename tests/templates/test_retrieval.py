import pytest
import typer

from cli.conf.constants import GITHUB_INIT_ASSETS_DIR, CommonErrorCodes
from cli.templates.retrieval import CodeRetriever, ZentraSetupRetriever, create_soup
from tests.mappings.retrieval import ZENTRA_INIT_CODE_VALID, ZENTRA_INIT_VALID


def test_create_soup_fail():
    with pytest.raises(typer.Exit) as e:
        create_soup("https://github.com/randomtest")

    assert e.value.exit_code == CommonErrorCodes.REQUEST_FAILED


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
        assert result == ZENTRA_INIT_CODE_VALID["full_file"], result
