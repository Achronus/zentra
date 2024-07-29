from . import build_json_response_model
from .messages import HTTP_MSG_MAPPING

HTTP_INFO_100 = build_json_response_model(HTTP_MSG_MAPPING[100])
HTTP_INFO_101 = build_json_response_model(HTTP_MSG_MAPPING[101])
HTTP_INFO_102 = build_json_response_model(HTTP_MSG_MAPPING[102])
HTTP_INFO_103 = build_json_response_model(HTTP_MSG_MAPPING[103])

HTTP_REDIRECT_300 = build_json_response_model(HTTP_MSG_MAPPING[300])
HTTP_REDIRECT_301 = build_json_response_model(HTTP_MSG_MAPPING[301])
HTTP_REDIRECT_302 = build_json_response_model(HTTP_MSG_MAPPING[302])
HTTP_REDIRECT_303 = build_json_response_model(HTTP_MSG_MAPPING[303])
HTTP_REDIRECT_304 = build_json_response_model(HTTP_MSG_MAPPING[304])
HTTP_REDIRECT_305 = build_json_response_model(HTTP_MSG_MAPPING[305])
HTTP_REDIRECT_306 = build_json_response_model(HTTP_MSG_MAPPING[306])
HTTP_REDIRECT_307 = build_json_response_model(HTTP_MSG_MAPPING[307])
HTTP_REDIRECT_308 = build_json_response_model(HTTP_MSG_MAPPING[308])

HTTP_ERROR_400 = build_json_response_model(HTTP_MSG_MAPPING[400])
HTTP_ERROR_401 = build_json_response_model(HTTP_MSG_MAPPING[401])
HTTP_ERROR_402 = build_json_response_model(HTTP_MSG_MAPPING[402])
HTTP_ERROR_403 = build_json_response_model(HTTP_MSG_MAPPING[403])
HTTP_ERROR_404 = build_json_response_model(HTTP_MSG_MAPPING[404])
HTTP_ERROR_405 = build_json_response_model(HTTP_MSG_MAPPING[405])
HTTP_ERROR_406 = build_json_response_model(HTTP_MSG_MAPPING[406])
HTTP_ERROR_407 = build_json_response_model(HTTP_MSG_MAPPING[407])
HTTP_ERROR_408 = build_json_response_model(HTTP_MSG_MAPPING[408])
HTTP_ERROR_409 = build_json_response_model(HTTP_MSG_MAPPING[409])
HTTP_ERROR_410 = build_json_response_model(HTTP_MSG_MAPPING[410])
HTTP_ERROR_411 = build_json_response_model(HTTP_MSG_MAPPING[411])
HTTP_ERROR_412 = build_json_response_model(HTTP_MSG_MAPPING[412])
HTTP_ERROR_413 = build_json_response_model(HTTP_MSG_MAPPING[413])
HTTP_ERROR_414 = build_json_response_model(HTTP_MSG_MAPPING[414])
HTTP_ERROR_415 = build_json_response_model(HTTP_MSG_MAPPING[415])
HTTP_ERROR_416 = build_json_response_model(HTTP_MSG_MAPPING[416])
HTTP_ERROR_417 = build_json_response_model(HTTP_MSG_MAPPING[417])
HTTP_ERROR_418 = build_json_response_model(HTTP_MSG_MAPPING[418])
HTTP_ERROR_421 = build_json_response_model(HTTP_MSG_MAPPING[421])
HTTP_ERROR_422 = build_json_response_model(HTTP_MSG_MAPPING[422])
HTTP_ERROR_423 = build_json_response_model(HTTP_MSG_MAPPING[423])
HTTP_ERROR_424 = build_json_response_model(HTTP_MSG_MAPPING[424])
HTTP_ERROR_425 = build_json_response_model(HTTP_MSG_MAPPING[425])
HTTP_ERROR_426 = build_json_response_model(HTTP_MSG_MAPPING[426])
HTTP_ERROR_428 = build_json_response_model(HTTP_MSG_MAPPING[428])
HTTP_ERROR_429 = build_json_response_model(HTTP_MSG_MAPPING[429])
HTTP_ERROR_431 = build_json_response_model(HTTP_MSG_MAPPING[431])
HTTP_ERROR_451 = build_json_response_model(HTTP_MSG_MAPPING[451])

HTTP_ERROR_500 = build_json_response_model(HTTP_MSG_MAPPING[500])
HTTP_ERROR_501 = build_json_response_model(HTTP_MSG_MAPPING[501])
HTTP_ERROR_502 = build_json_response_model(HTTP_MSG_MAPPING[502])
HTTP_ERROR_503 = build_json_response_model(HTTP_MSG_MAPPING[503])
HTTP_ERROR_504 = build_json_response_model(HTTP_MSG_MAPPING[504])
HTTP_ERROR_505 = build_json_response_model(HTTP_MSG_MAPPING[505])
HTTP_ERROR_506 = build_json_response_model(HTTP_MSG_MAPPING[506])
HTTP_ERROR_507 = build_json_response_model(HTTP_MSG_MAPPING[507])
HTTP_ERROR_508 = build_json_response_model(HTTP_MSG_MAPPING[508])
HTTP_ERROR_510 = build_json_response_model(HTTP_MSG_MAPPING[510])
HTTP_ERROR_511 = build_json_response_model(HTTP_MSG_MAPPING[511])
