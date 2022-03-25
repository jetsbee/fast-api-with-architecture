from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from . import exceptions


def add_custom_exception_handlers(app: FastAPI) -> None:
    app.exception_handler(exceptions.UserAlreadyExistenceException)(
        user_already_existence_exception_handler
    )


async def user_already_existence_exception_handler(
    request: Request, exc: exceptions.UserAlreadyExistenceException
) -> JSONResponse:
    print("#PoorSimpleLoggerForOnlySamplePurpose:", exc)
    return JSONResponse(status_code=409, content={"detail": exc.detail})
