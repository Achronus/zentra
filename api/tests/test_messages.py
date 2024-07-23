import pytest

from zentra_api.responses.messages import HTTP_MSG_MAPPING, HTTPMessage


class TestHttpMapping:
    @staticmethod
    def test_300_valid():
        assert isinstance(HTTP_MSG_MAPPING[300], HTTPMessage)
