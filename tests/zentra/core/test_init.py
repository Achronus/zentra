import pytest

from zentra_models.core import ReactFile, Block, Zentra
from zentra_models.ui.control import Input


class TestZentra:
    @pytest.fixture
    def zentra(self) -> Zentra:
        return Zentra()

    @pytest.fixture
    def test_file(self) -> ReactFile:
        return ReactFile(
            name="Test",
            block=Block(
                name="Test",
                components=[Input(id="test")],
            ),
        )

    @staticmethod
    def test_register_invalid(zentra: Zentra):
        with pytest.raises(ValueError):
            zentra.register("test")

    @staticmethod
    def test_register_invalid_list(zentra: Zentra):
        with pytest.raises(ValueError):
            zentra.register(["test"])

    @staticmethod
    def test_register_valid(zentra: Zentra, test_file: ReactFile):
        zentra.register(test_file)

    @staticmethod
    def test_register_valid_single(zentra: Zentra, test_file: ReactFile):
        zentra.register([test_file])
