class APIException(Exception):
    status_code = 400
    default_detail = "A server error occurred."

    def __init__(self, detail: str | None = None, status_code: int | None = None) -> None:
        self.detail = detail or self.default_detail
        if status_code is not None:
            self.status_code = status_code
        super().__init__(self.detail)


class BadRequestException(APIException):
    status_code = 400
    default_detail = "Bad request."


class ValidationException(BadRequestException):
    default_detail = "Validation failed."


class AuthenticationException(APIException):
    status_code = 401
    default_detail = "Authentication failed."


class AuthorizationException(APIException):
    status_code = 403
    default_detail = "Not authorized."


class NotFoundException(APIException):
    status_code = 404
    default_detail = "Resource not found."
