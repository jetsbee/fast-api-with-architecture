import logging
from functools import wraps
from typing import Callable, Awaitable

from fastapi import Request
from fastapi.logger import logger
from starlette.responses import Response

from .config import get_settings
from .error.exceptions import (
    StarletteHTTPException,
    RequestValidationError,
    APIException,
)

logger.setLevel(get_settings().LOG_LEVEL)
logger.addHandler(logging.StreamHandler())

ErrorHanderCallable = Callable[[Request, Exception], Awaitable[Response]]


def enable_exc_logging(original_function: ErrorHanderCallable) -> ErrorHanderCallable:
    @wraps(original_function)
    async def wrapper(request: Request, exc: Exception) -> Awaitable[Response]:
        if isinstance(exc, APIException):
            if exc.status_code >= 500:
                logger.error(f"Hello, error logger!: {exc}")
            else:
                logger.info(f"Hello, info logger!: {exc}")
        elif isinstance(exc, RequestValidationError):
            logger.info(f"OMG! The client sent invalid data!: {exc}")
        elif isinstance(exc, StarletteHTTPException):
            if exc.status_code >= 500:
                logger.error(f"OMG! An HTTP error!: {repr(exc)}")
            else:
                logger.info(f"OMG! An HTTP error!: {repr(exc)}")

        response = await original_function(request, exc)
        return response

    return wrapper
