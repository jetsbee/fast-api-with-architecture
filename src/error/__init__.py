from fastapi import FastAPI

from .exceptions import StarletteHTTPException, RequestValidationError, APIException
from .handlers import (
    custom_http_exception_handler,
    validation_exception_handler,
    api_exception_exception_handler,
)


def add_custom_exception_handlers(app: FastAPI) -> None:
    app.exception_handler(StarletteHTTPException)(custom_http_exception_handler)
    app.exception_handler(RequestValidationError)(validation_exception_handler)
    app.exception_handler(APIException)(api_exception_exception_handler)
