import time
from functools import wraps
from typing import Callable, Awaitable

from fastapi import Request
from starlette.responses import Response
from starlette.middleware.base import RequestResponseEndpoint

from .error import APIException
from .error.handlers import api_exception_exception_handler

MiddlewareCallable = Callable[[Request, RequestResponseEndpoint], Awaitable[Response]]


def add_logging_info(original_function: MiddlewareCallable) -> MiddlewareCallable:
    @wraps(original_function)
    async def wrapper(
        request: Request, call_next: RequestResponseEndpoint
    ) -> Awaitable[Response]:
        request.state.start_time = time.time()
        response = await original_function(request, call_next)
        return response

    return wrapper


@add_logging_info
async def handle_unexpected_exc(
    request: Request, call_next: RequestResponseEndpoint
) -> Awaitable[Response]:
    try:
        response = await call_next(request)
    except Exception as exc:
        api_exc = APIException(exc=exc, detail=str(exc))
        response = await api_exception_exception_handler(request=request, exc=api_exc)

    return response
