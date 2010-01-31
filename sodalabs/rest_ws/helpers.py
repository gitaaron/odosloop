from django.http import HttpResponse, HttpResponseNotAllowed

class NoContentResponse(HttpResponse):
    content_type = "None"

class ResponseOK(NoContentResponse):
    status_code = 200

class ResponseForbidden(NoContentResponse):
    status_code = 403

class ResponseNotFound(NoContentResponse):
    status_code = 404

class ResponseBadRequest(NoContentResponse):
    status_code = 400

class ResponseUnAuthorized(NoContentResponse):
    status_code = 401

class ResponseExpectationFailed(NoContentResponse):
    status_code = 417

class ResponseRequestEntityTooLarge(NoContentResponse):
    status_code = 413

class ResponseNotAllowed(HttpResponseNotAllowed):
    """
    returns status code 405
    """
    content_type = "None"

    def __init__(self, permitted_methods):
        HttpResponseNotAllowed.__init__(self, permitted_methods)

class ResponsePreconditionFailed(NoContentResponse):
    status_code = 412


