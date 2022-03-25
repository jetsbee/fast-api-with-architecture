from fastapi import FastAPI

from .components.auth.errors import (
    exceptions as auth_exceptions,
    handlers as auth_handlers,
)


def add_custom_exception_handlers(app: FastAPI) -> None:
    app.exception_handler(auth_exceptions.UserAlreadyExistenceException)(
        auth_handlers.user_already_existence_exception_handler
    )
