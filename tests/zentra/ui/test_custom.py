import pytest

from pydantic_core import PydanticCustomError

from zentra_models.custom import CustomUrl


class TestCustomUrl:
    @staticmethod
    def test_whitespace_error():
        with pytest.raises(PydanticCustomError):
            CustomUrl(url="/white space here").validate_url()

    @staticmethod
    def test_url_start_error():
        with pytest.raises(PydanticCustomError):
            CustomUrl(url="not a url").validate_url()
