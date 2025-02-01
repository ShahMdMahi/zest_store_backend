from ninja.errors import HttpError
from http import HTTPStatus

class APIError(HttpError):
    def __init__(self, message: str, status_code: int = HTTPStatus.BAD_REQUEST):
        super().__init__(status_code, {"message": message})

class AuthenticationError(APIError):
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, HTTPStatus.UNAUTHORIZED)

class PermissionError(APIError):
    def __init__(self, message: str = "Permission denied"):
        super().__init__(message, HTTPStatus.FORBIDDEN) 