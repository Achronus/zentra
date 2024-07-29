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
        msg = HTTP_MSG_MAPPING[100]
        assert isinstance(msg, HTTPMessage)
        assert msg.status == "info"

    @staticmethod
    def test_101_valid():
        msg = HTTP_MSG_MAPPING[101]
        assert isinstance(msg, HTTPMessage)
        assert msg.status == "info"

    @staticmethod
    def test_102_valid():
        msg = HTTP_MSG_MAPPING[102]
        assert isinstance(msg, HTTPMessage)
        assert msg.status == "info"

    @staticmethod
    def test_103_valid():
        msg = HTTP_MSG_MAPPING[103]
        assert isinstance(msg, HTTPMessage)
        assert msg.status == "info"

    @staticmethod
    def test_200_valid():
        msg = HTTP_MSG_MAPPING[200]
        assert isinstance(msg, HTTPMessage)
        assert msg.status == "success"

    @staticmethod
    def test_201_valid():
        msg = HTTP_MSG_MAPPING[201]
        assert isinstance(msg, HTTPMessage)
        assert msg.status == "success"

    @staticmethod
    def test_202_valid():
        msg = HTTP_MSG_MAPPING[202]
        assert isinstance(msg, HTTPMessage)
        assert msg.status == "success"

    @staticmethod
    def test_203_valid():
        msg = HTTP_MSG_MAPPING[203]
        assert isinstance(msg, HTTPMessage)
        assert msg.status == "success"

    @staticmethod
    def test_204_valid():
        msg = HTTP_MSG_MAPPING[204]
        assert isinstance(msg, HTTPMessage)
        assert msg.status == "success"

    @staticmethod
    def test_205_valid():
        msg = HTTP_MSG_MAPPING[205]
        assert isinstance(msg, HTTPMessage)
        assert msg.status == "success"

    @staticmethod
    def test_206_valid():
        msg = HTTP_MSG_MAPPING[206]
        assert isinstance(msg, HTTPMessage)
        assert msg.status == "success"

    @staticmethod
    def test_207_valid():
        msg = HTTP_MSG_MAPPING[207]
        assert isinstance(msg, HTTPMessage)
        assert msg.status == "success"

    @staticmethod
    def test_208_valid():
        msg = HTTP_MSG_MAPPING[208]
        assert isinstance(msg, HTTPMessage)
        assert msg.status == "success"

    @staticmethod
    def test_226_valid():
        msg = HTTP_MSG_MAPPING[226]
        assert isinstance(msg, HTTPMessage)
        assert msg.status == "success"

    @staticmethod
    def test_300_valid():
        msg = HTTP_MSG_MAPPING[300]
        assert isinstance(msg, HTTPMessage)
        assert msg.status == "redirect"

    @staticmethod
    def test_301_valid():
        msg = HTTP_MSG_MAPPING[301]
        assert isinstance(msg, HTTPMessage)
        assert msg.status == "redirect"

    @staticmethod
    def test_302_valid():
        msg = HTTP_MSG_MAPPING[302]
        assert isinstance(msg, HTTPMessage)
        assert msg.status == "redirect"

    @staticmethod
    def test_303_valid():
        msg = HTTP_MSG_MAPPING[303]
        assert isinstance(msg, HTTPMessage)
        assert msg.status == "redirect"

    @staticmethod
    def test_304_valid():
        msg = HTTP_MSG_MAPPING[304]
        assert isinstance(msg, HTTPMessage)
        assert msg.status == "redirect"

    @staticmethod
    def test_305_valid():
        msg = HTTP_MSG_MAPPING[305]
        assert isinstance(msg, HTTPMessage)
        assert msg.status == "redirect"

    @staticmethod
    def test_307_valid():
        msg = HTTP_MSG_MAPPING[307]
        assert isinstance(msg, HTTPMessage)
        assert msg.status == "redirect"

    @staticmethod
    def test_308_valid():
        msg = HTTP_MSG_MAPPING[308]
        assert isinstance(msg, HTTPMessage)
        assert msg.status == "redirect"

    @staticmethod
    def test_400_valid():
        msg = HTTP_MSG_MAPPING[400]
        assert isinstance(msg, HTTPMessage)
        assert msg.status == "error"

    @staticmethod
    def test_401_valid():
        msg = HTTP_MSG_MAPPING[401]
        assert isinstance(msg, HTTPMessage)
        assert msg.status == "error"

    @staticmethod
    def test_402_valid():
        msg = HTTP_MSG_MAPPING[402]
        assert isinstance(msg, HTTPMessage)
        assert msg.status == "error"

    @staticmethod
    def test_403_valid():
        msg = HTTP_MSG_MAPPING[403]
        assert isinstance(msg, HTTPMessage)
        assert msg.status == "error"

    @staticmethod
    def test_404_valid():
        msg = HTTP_MSG_MAPPING[404]
        assert isinstance(msg, HTTPMessage)
        assert msg.status == "error"

    @staticmethod
    def test_405_valid():
        msg = HTTP_MSG_MAPPING[405]
        assert isinstance(msg, HTTPMessage)
        assert msg.status == "error"

    @staticmethod
    def test_406_valid():
        msg = HTTP_MSG_MAPPING[406]
        assert isinstance(msg, HTTPMessage)
        assert msg.status == "error"

    @staticmethod
    def test_407_valid():
        msg = HTTP_MSG_MAPPING[407]
        assert isinstance(msg, HTTPMessage)
        assert msg.status == "error"

    @staticmethod
    def test_408_valid():
        msg = HTTP_MSG_MAPPING[408]
        assert isinstance(msg, HTTPMessage)
        assert msg.status == "error"

    @staticmethod
    def test_409_valid():
        msg = HTTP_MSG_MAPPING[409]
        assert isinstance(msg, HTTPMessage)
        assert msg.status == "error"

    @staticmethod
    def test_410_valid():
        msg = HTTP_MSG_MAPPING[410]
        assert isinstance(msg, HTTPMessage)
        assert msg.status == "error"

    @staticmethod
    def test_411_valid():
        msg = HTTP_MSG_MAPPING[411]
        assert isinstance(msg, HTTPMessage)
        assert msg.status == "error"

    @staticmethod
    def test_412_valid():
        msg = HTTP_MSG_MAPPING[412]
        assert isinstance(msg, HTTPMessage)
        assert msg.status == "error"

    @staticmethod
    def test_413_valid():
        msg = HTTP_MSG_MAPPING[413]
        assert isinstance(msg, HTTPMessage)
        assert msg.status == "error"

    @staticmethod
    def test_414_valid():
        msg = HTTP_MSG_MAPPING[414]
        assert isinstance(msg, HTTPMessage)
        assert msg.status == "error"

    @staticmethod
    def test_415_valid():
        msg = HTTP_MSG_MAPPING[415]
        assert isinstance(msg, HTTPMessage)
        assert msg.status == "error"

    @staticmethod
    def test_416_valid():
        msg = HTTP_MSG_MAPPING[416]
        assert isinstance(msg, HTTPMessage)
        assert msg.status == "error"

    @staticmethod
    def test_417_valid():
        msg = HTTP_MSG_MAPPING[417]
        assert isinstance(msg, HTTPMessage)
        assert msg.status == "error"

    @staticmethod
    def test_418_valid():
        msg = HTTP_MSG_MAPPING[418]
        assert isinstance(msg, HTTPMessage)
        assert msg.status == "error"

    @staticmethod
    def test_421_valid():
        msg = HTTP_MSG_MAPPING[421]
        assert isinstance(msg, HTTPMessage)
        assert msg.status == "error"

    @staticmethod
    def test_422_valid():
        msg = HTTP_MSG_MAPPING[422]
        assert isinstance(msg, HTTPMessage)
        assert msg.status == "error"

    @staticmethod
    def test_423_valid():
        msg = HTTP_MSG_MAPPING[423]
        assert isinstance(msg, HTTPMessage)
        assert msg.status == "error"

    @staticmethod
    def test_424_valid():
        msg = HTTP_MSG_MAPPING[424]
        assert isinstance(msg, HTTPMessage)
        assert msg.status == "error"

    @staticmethod
    def test_425_valid():
        msg = HTTP_MSG_MAPPING[425]
        assert isinstance(msg, HTTPMessage)
        assert msg.status == "error"

    @staticmethod
    def test_426_valid():
        msg = HTTP_MSG_MAPPING[426]
        assert isinstance(msg, HTTPMessage)
        assert msg.status == "error"

    @staticmethod
    def test_428_valid():
        msg = HTTP_MSG_MAPPING[428]
        assert isinstance(msg, HTTPMessage)
        assert msg.status == "error"

    @staticmethod
    def test_429_valid():
        msg = HTTP_MSG_MAPPING[429]
        assert isinstance(msg, HTTPMessage)
        assert msg.status == "error"

    @staticmethod
    def test_431_valid():
        msg = HTTP_MSG_MAPPING[431]
        assert isinstance(msg, HTTPMessage)
        assert msg.status == "error"

    @staticmethod
    def test_451_valid():
        msg = HTTP_MSG_MAPPING[451]
        assert isinstance(msg, HTTPMessage)
        assert msg.status == "error"

    @staticmethod
    def test_500_valid():
        msg = HTTP_MSG_MAPPING[500]
        assert isinstance(msg, HTTPMessage)
        assert msg.status == "error"

    @staticmethod
    def test_501_valid():
        msg = HTTP_MSG_MAPPING[501]
        assert isinstance(msg, HTTPMessage)
        assert msg.status == "error"

    @staticmethod
    def test_502_valid():
        msg = HTTP_MSG_MAPPING[502]
        assert isinstance(msg, HTTPMessage)
        assert msg.status == "error"

    @staticmethod
    def test_503_valid():
        msg = HTTP_MSG_MAPPING[503]
        assert isinstance(msg, HTTPMessage)
        assert msg.status == "error"

    @staticmethod
    def test_504_valid():
        msg = HTTP_MSG_MAPPING[504]
        assert isinstance(msg, HTTPMessage)
        assert msg.status == "error"

    @staticmethod
    def test_505_valid():
        msg = HTTP_MSG_MAPPING[505]
        assert isinstance(msg, HTTPMessage)
        assert msg.status == "error"

    @staticmethod
    def test_506_valid():
        msg = HTTP_MSG_MAPPING[506]
        assert isinstance(msg, HTTPMessage)
        assert msg.status == "error"

    @staticmethod
    def test_507_valid():
        msg = HTTP_MSG_MAPPING[507]
        assert isinstance(msg, HTTPMessage)
        assert msg.status == "error"

    @staticmethod
    def test_508_valid():
        msg = HTTP_MSG_MAPPING[508]
        assert isinstance(msg, HTTPMessage)
        assert msg.status == "error"

    @staticmethod
    def test_510_valid():
        msg = HTTP_MSG_MAPPING[510]
        assert isinstance(msg, HTTPMessage)
        assert msg.status == "error"

    @staticmethod
    def test_511_valid():
        msg = HTTP_MSG_MAPPING[511]
        assert isinstance(msg, HTTPMessage)
        assert msg.status == "error"
