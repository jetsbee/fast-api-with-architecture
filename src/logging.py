import logging
import time
from contextlib import suppress
from dataclasses import dataclass
from datetime import datetime
from functools import wraps
from inspect import FrameInfo, trace
from typing import Any, Callable, Awaitable, Dict, Optional

from fastapi import Request
from fastapi.logger import logger
from fastapi.routing import APIRoute
from starlette.responses import Response

from .config import get_settings
from .error.exceptions import RequestValidationError

logger.setLevel(get_settings().LOG_LEVEL)
logger.addHandler(logging.StreamHandler())

ErrorHanderCallable = Callable[[Request, Exception], Awaitable[Response]]


@dataclass
class ErrorDetail:
    err_func: Optional[str] = None
    err_location: Optional[str] = None
    exc: Optional[Exception] = None


time_format = "%Y/%m/%d %H:%M:%S"


@dataclass
class LoggingInfo:
    error_detail: Optional[ErrorDetail] = None
    ip: Optional[str] = None
    url: Optional[str] = None
    method: Optional[str] = None
    headers: Any = None
    cookies: Optional[Dict[str, str]] = None
    query_params: Any = None
    req_body: Any = None
    process_time: Optional[str] = None
    UTC: str = datetime.utcnow().strftime(time_format)


def enable_exc_logging(original_function: ErrorHanderCallable) -> ErrorHanderCallable:
    @wraps(original_function)
    async def wrapper(request: Request, exc: Exception) -> Awaitable[Response]:
        # Logging Info
        logging_info = LoggingInfo()

        ip = (
            request.headers["x-forwarded-for"]
            if "x-forwarded-for" in request.headers.keys()
            else request.client.host
        )
        logging_info.ip = ip.split(",")[0] if "," in ip else ip
        logging_info.url = f"{request.url.hostname}{request.url.path}"
        logging_info.method = request.method
        logging_info.headers = request.headers
        logging_info.cookies = request.cookies
        logging_info.query_params = request.query_params

        # Extract request body from expected error handled by custom handler
        with suppress(AttributeError):
            setattr(logging_info, "req_body", getattr(exc, "req_body"))
        # Extract request body from unexpected error wrapped in APIException
        with suppress(AttributeError):
            setattr(
                logging_info, "req_body", getattr(exc.exc, "req_body")
            ) if logging_info.req_body is None else None
        # Process Time
        with suppress(AttributeError):
            process_time = time.time() - request.state.start_time
            logging_info.process_time = f"{round(process_time * 1000, 5)}ms"

        # Error Details
        error_detail = ErrorDetail()

        t = trace()
        if t:
            frame: FrameInfo = t[-1]
            error_detail.err_func = frame.function

            error_file = frame.filename
            error_line = frame.lineno
            error_detail.err_location = f'"{error_file}", line {error_line}'

        error_detail.exc = exc

        logging_info.error_detail = error_detail
        # End of Error Details
        # End of Logging Info

        response = await original_function(request, exc)

        # Logging with level
        if isinstance(exc, RequestValidationError):
            logger.info(f"{logging_info.__dict__}")
        elif exc.status_code < 500:
            logger.info(f"{logging_info.__dict__}")
        else:
            logger.error(f"{logging_info.__dict__}")

        return response

    return wrapper


class ErrorLoggingRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            try:
                return await original_route_handler(request)
            except Exception as exc:

                body = await request.body()
                setattr(exc, "req_body", body)
                raise exc

        return custom_route_handler
