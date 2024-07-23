from . import success_response_model

from fastapi import status


HTTP_SUCCESS_200 = success_response_model(
    status.HTTP_200_OK,
    "The request was successful and the server responded with the requested resource.",
)

HTTP_SUCCESS_201 = success_response_model(
    status.HTTP_201_CREATED,
    "The request was successful and a new resource was created as a result. The URI of the new resource is provided in the `Location` header.",
)

HTTP_SUCCESS_202 = success_response_model(
    status.HTTP_202_ACCEPTED,
    "The request has been accepted for processing, but the processing has not been completed. The result of the processing may be available later.",
)

HTTP_SUCCESS_203 = success_response_model(
    status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
    "The request was successful, but the information provided may be from a third-party source and not authoritative.",
)

HTTP_SUCCESS_204 = success_response_model(
    status.HTTP_204_NO_CONTENT,
    "The request was successful, but there is no content to send in the response. The client should not expect a message body.",
)

HTTP_SUCCESS_205 = success_response_model(
    status.HTTP_205_RESET_CONTENT,
    "The request was successful and the client should reset the document view. This response is typically used in cases where the user needs to clear or reset a form.",
)

HTTP_SUCCESS_206 = success_response_model(
    status.HTTP_206_PARTIAL_CONTENT,
    "The server is delivering only a part of the resource due to a range header sent by the client. This is typically used for partial downloads.",
)

HTTP_SUCCESS_207 = success_response_model(
    status.HTTP_207_MULTI_STATUS,
    "The request was successful, but it resulted in multiple status codes, which are provided in the response body. This is typically used with WebDAV.",
)

HTTP_SUCCESS_208 = success_response_model(
    status.HTTP_208_ALREADY_REPORTED,
    "The members of a DAV binding have already been enumerated in a previous response. This status code is used to prevent the enumerated bindings from being listed again.",
)

HTTP_SUCCESS_226 = success_response_model(
    status.HTTP_226_IM_USED,
    "The server has fulfilled a GET request for the resource, and the response is a representation of the result of one or more instance-manipulations applied to the current instance.",
)
