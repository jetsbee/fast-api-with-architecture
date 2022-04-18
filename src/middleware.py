import time
from functools import wraps

from starlette.requests import Request
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from .error import APIException
from .error.handlers import api_exception_exception_handler


def add_logging_info(original_function):
    @wraps(original_function)
    async def wrapper(self, scope: Scope, receive: Receive, send: Send):
        request = Request(scope)
        request.state.start_time = time.time()
        return await original_function(self, scope, receive, send)

    return wrapper


class UnexpectedErrorMiddleware:
    """
    Handles unexpected error by custom error handler

    Inspired by ServerErrorMiddleware from starlette.middleware.errors
    Ref. https://github.com/encode/starlette/discussions/1537#discussioncomment-2293341

    Never use middlewares subclassing BaseHTTPMiddleware, as using BackgroundTasks from fastapi
    Ref. https://github.com/encode/starlette/issues/919#issuecomment-672908610
    """

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    @add_logging_info
    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        response_started = False

        async def _send(message: Message) -> None:
            nonlocal response_started, send

            if message["type"] == "http.response.start":
                response_started = True
            await send(message)

        try:
            await self.app(scope, receive, _send)
        except Exception as unexpected_exc:
            request = Request(scope)
            api_exc = APIException(exc=unexpected_exc, detail=str(unexpected_exc))
            response = await api_exception_exception_handler(
                request=request, exc=api_exc
            )

            if not response_started:
                await response(scope, receive, send)
