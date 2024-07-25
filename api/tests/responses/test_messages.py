from zentra_api.responses.messages import HTTP_MSG_MAPPING, HTTPMessage


class TestHTTPMessage:
    @staticmethod
    def test_headers_none():
        msg = HTTPMessage(status_code=100, detail="Continue sending the request body.")
        assert msg.headers == {}

    @staticmethod
    def test_headers_dict():
        msg = HTTPMessage(
            status_code=100,
            detail="Continue sending the request body.",
            headers={"test": "value"},
        )
        assert msg.headers == {"test": "value"}


class TestHttpMapping:
    @staticmethod
    def test_100_valid():
        assert isinstance(HTTP_MSG_MAPPING[100], HTTPMessage)

    @staticmethod
    def test_101_valid():
        assert isinstance(HTTP_MSG_MAPPING[101], HTTPMessage)

    @staticmethod
    def test_102_valid():
        assert isinstance(HTTP_MSG_MAPPING[102], HTTPMessage)

    @staticmethod
    def test_103_valid():
        assert isinstance(HTTP_MSG_MAPPING[103], HTTPMessage)

    @staticmethod
    def test_200_valid():
        assert isinstance(HTTP_MSG_MAPPING[200], HTTPMessage)

    @staticmethod
    def test_201_valid():
        assert isinstance(HTTP_MSG_MAPPING[201], HTTPMessage)

    @staticmethod
    def test_202_valid():
        assert isinstance(HTTP_MSG_MAPPING[202], HTTPMessage)

    @staticmethod
    def test_203_valid():
        assert isinstance(HTTP_MSG_MAPPING[203], HTTPMessage)

    @staticmethod
    def test_204_valid():
        assert isinstance(HTTP_MSG_MAPPING[204], HTTPMessage)

    @staticmethod
    def test_205_valid():
        assert isinstance(HTTP_MSG_MAPPING[205], HTTPMessage)

    @staticmethod
    def test_206_valid():
        assert isinstance(HTTP_MSG_MAPPING[206], HTTPMessage)

    @staticmethod
    def test_207_valid():
        assert isinstance(HTTP_MSG_MAPPING[207], HTTPMessage)

    @staticmethod
    def test_208_valid():
        assert isinstance(HTTP_MSG_MAPPING[208], HTTPMessage)

    @staticmethod
    def test_226_valid():
        assert isinstance(HTTP_MSG_MAPPING[226], HTTPMessage)

    @staticmethod
    def test_300_valid():
        assert isinstance(HTTP_MSG_MAPPING[300], HTTPMessage)

    @staticmethod
    def test_301_valid():
        assert isinstance(HTTP_MSG_MAPPING[301], HTTPMessage)

    @staticmethod
    def test_302_valid():
        assert isinstance(HTTP_MSG_MAPPING[302], HTTPMessage)

    @staticmethod
    def test_303_valid():
        assert isinstance(HTTP_MSG_MAPPING[303], HTTPMessage)

    @staticmethod
    def test_304_valid():
        assert isinstance(HTTP_MSG_MAPPING[304], HTTPMessage)

    @staticmethod
    def test_305_valid():
        assert isinstance(HTTP_MSG_MAPPING[305], HTTPMessage)

    @staticmethod
    def test_307_valid():
        assert isinstance(HTTP_MSG_MAPPING[307], HTTPMessage)

    @staticmethod
    def test_308_valid():
        assert isinstance(HTTP_MSG_MAPPING[308], HTTPMessage)

    @staticmethod
    def test_400_valid():
        assert isinstance(HTTP_MSG_MAPPING[400], HTTPMessage)

    @staticmethod
    def test_401_valid():
        assert isinstance(HTTP_MSG_MAPPING[401], HTTPMessage)

    @staticmethod
    def test_402_valid():
        assert isinstance(HTTP_MSG_MAPPING[402], HTTPMessage)

    @staticmethod
    def test_403_valid():
        assert isinstance(HTTP_MSG_MAPPING[403], HTTPMessage)

    @staticmethod
    def test_404_valid():
        assert isinstance(HTTP_MSG_MAPPING[404], HTTPMessage)

    @staticmethod
    def test_405_valid():
        assert isinstance(HTTP_MSG_MAPPING[405], HTTPMessage)

    @staticmethod
    def test_406_valid():
        assert isinstance(HTTP_MSG_MAPPING[406], HTTPMessage)

    @staticmethod
    def test_407_valid():
        assert isinstance(HTTP_MSG_MAPPING[407], HTTPMessage)

    @staticmethod
    def test_408_valid():
        assert isinstance(HTTP_MSG_MAPPING[408], HTTPMessage)

    @staticmethod
    def test_409_valid():
        assert isinstance(HTTP_MSG_MAPPING[409], HTTPMessage)

    @staticmethod
    def test_410_valid():
        assert isinstance(HTTP_MSG_MAPPING[410], HTTPMessage)

    @staticmethod
    def test_411_valid():
        assert isinstance(HTTP_MSG_MAPPING[411], HTTPMessage)

    @staticmethod
    def test_412_valid():
        assert isinstance(HTTP_MSG_MAPPING[412], HTTPMessage)

    @staticmethod
    def test_413_valid():
        assert isinstance(HTTP_MSG_MAPPING[413], HTTPMessage)

    @staticmethod
    def test_414_valid():
        assert isinstance(HTTP_MSG_MAPPING[414], HTTPMessage)

    @staticmethod
    def test_415_valid():
        assert isinstance(HTTP_MSG_MAPPING[415], HTTPMessage)

    @staticmethod
    def test_416_valid():
        assert isinstance(HTTP_MSG_MAPPING[416], HTTPMessage)

    @staticmethod
    def test_417_valid():
        assert isinstance(HTTP_MSG_MAPPING[417], HTTPMessage)

    @staticmethod
    def test_418_valid():
        assert isinstance(HTTP_MSG_MAPPING[418], HTTPMessage)

    @staticmethod
    def test_421_valid():
        assert isinstance(HTTP_MSG_MAPPING[421], HTTPMessage)

    @staticmethod
    def test_422_valid():
        assert isinstance(HTTP_MSG_MAPPING[422], HTTPMessage)

    @staticmethod
    def test_423_valid():
        assert isinstance(HTTP_MSG_MAPPING[423], HTTPMessage)

    @staticmethod
    def test_424_valid():
        assert isinstance(HTTP_MSG_MAPPING[424], HTTPMessage)

    @staticmethod
    def test_425_valid():
        assert isinstance(HTTP_MSG_MAPPING[425], HTTPMessage)

    @staticmethod
    def test_426_valid():
        assert isinstance(HTTP_MSG_MAPPING[426], HTTPMessage)

    @staticmethod
    def test_428_valid():
        assert isinstance(HTTP_MSG_MAPPING[428], HTTPMessage)

    @staticmethod
    def test_429_valid():
        assert isinstance(HTTP_MSG_MAPPING[429], HTTPMessage)

    @staticmethod
    def test_431_valid():
        assert isinstance(HTTP_MSG_MAPPING[431], HTTPMessage)

    @staticmethod
    def test_451_valid():
        assert isinstance(HTTP_MSG_MAPPING[451], HTTPMessage)

    @staticmethod
    def test_500_valid():
        assert isinstance(HTTP_MSG_MAPPING[500], HTTPMessage)

    @staticmethod
    def test_501_valid():
        assert isinstance(HTTP_MSG_MAPPING[501], HTTPMessage)

    @staticmethod
    def test_502_valid():
        assert isinstance(HTTP_MSG_MAPPING[502], HTTPMessage)

    @staticmethod
    def test_503_valid():
        assert isinstance(HTTP_MSG_MAPPING[503], HTTPMessage)

    @staticmethod
    def test_504_valid():
        assert isinstance(HTTP_MSG_MAPPING[504], HTTPMessage)

    @staticmethod
    def test_505_valid():
        assert isinstance(HTTP_MSG_MAPPING[505], HTTPMessage)

    @staticmethod
    def test_506_valid():
        assert isinstance(HTTP_MSG_MAPPING[506], HTTPMessage)

    @staticmethod
    def test_507_valid():
        assert isinstance(HTTP_MSG_MAPPING[507], HTTPMessage)

    @staticmethod
    def test_508_valid():
        assert isinstance(HTTP_MSG_MAPPING[508], HTTPMessage)

    @staticmethod
    def test_510_valid():
        assert isinstance(HTTP_MSG_MAPPING[510], HTTPMessage)

    @staticmethod
    def test_511_valid():
        assert isinstance(HTTP_MSG_MAPPING[511], HTTPMessage)
