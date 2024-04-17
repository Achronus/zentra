from pydantic import ValidationError
import pytest

from zentra.core import DataArray


class TestDataArray:
    @staticmethod
    def test_invalid_name_string():
        with pytest.raises(ValidationError):
            DataArray(
                name="WORKS",
                type_name="artwork",
                data=[{"artist": "Ornella Binni", "art": "url"}],
            )

    @staticmethod
    def test_invalid_parameter_string():
        with pytest.raises(ValidationError):
            DataArray(
                name="works",
                type_name="amazing artworks",
                data=[{"artist": "Ornella Binni", "art": "url"}],
            )

    @staticmethod
    def test_data_dict_list_missing1():
        with pytest.raises(ValidationError):
            DataArray(name="works", type_name="artwork", data=[])

    @staticmethod
    def test_data_dict_list_missing2():
        with pytest.raises(ValidationError):
            DataArray(name="works", type_name="artwork", data=[{}])

    @staticmethod
    def test_data_dict_list_invalid_keys():
        with pytest.raises(ValidationError):
            DataArray(
                name="works",
                type_name="amazing artworks",
                data=[
                    {"artist": "Ornella Binni", "art": "url"},
                    {"artist": "Ornella Binni", "test": "url"},
                ],
            )

    @staticmethod
    def test_data_dict_list_invalid_value_types():
        with pytest.raises(ValidationError):
            DataArray(
                name="works",
                type_name="amazing artworks",
                data=[
                    {"artist": "Ornella Binni", "art": "url"},
                    {"artist": 1, "art": "url"},
                ],
            )
