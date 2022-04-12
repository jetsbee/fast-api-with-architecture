import logging
from functools import wraps
from typing import Callable, Awaitable

from fastapi import Request
from fastapi.logger import logger
from starlette.responses import Response

from .config import get_settings

"""
# Logging issue under uvicorn

logger.debug(), logger.info() is not working, even if do logger.setLevel()

- Ref 1. https://github.com/tiangolo/fastapi/issues/2019#issuecomment-687845486
- Ref 2. https://github.com/encode/uvicorn/issues/945#issuecomment-819692145
"""
# Todo: specify level with config or env
logging.basicConfig(level=get_settings().LOG_LEVEL)  # Set all of loggers level

ErrorHanderCallable = Callable[[Request, Exception], Awaitable[Response]]


def add_exc_logger(original_function: ErrorHanderCallable) -> ErrorHanderCallable:
    @wraps(original_function)
    async def wrapper(request: Request, exc: Exception) -> Awaitable[Response]:
        logger.info("Hello, info logger!")
        logger.error("Hello, error logger!")
        response = await original_function(request, exc)
        return response

    return wrapper
