from fastapi import Request
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.responses import JSONResponse

from .exceptions import StarletteHTTPException, RequestValidationError, APIException
from ..logging import enable_exc_logging


@enable_exc_logging
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    return await http_exception_handler(request, exc)


@enable_exc_logging
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return await request_validation_exception_handler(request, exc)


@enable_exc_logging
async def api_exception_exception_handler(request: Request, exc: APIException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.code,
            "msg": exc.msg,
        },
    )
