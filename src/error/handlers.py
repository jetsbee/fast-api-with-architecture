from fastapi import Request
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.responses import JSONResponse

from .exceptions import StarletteHTTPException, RequestValidationError, APIException


async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    # print(f"OMG! An HTTP error!: {repr(exc)}")
    return await http_exception_handler(request, exc)


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # print(f"OMG! The client sent invalid data!: {exc}")
    return await request_validation_exception_handler(request, exc)


async def api_exception_exception_handler(
    request: Request, exc: APIException
) -> JSONResponse:
    # print("#PoorSimpleLoggerForOnlySamplePurpose:", exc)
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.code,
            "msg": exc.msg,
        },
    )
