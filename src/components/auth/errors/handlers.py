from fastapi import Request
from fastapi.responses import JSONResponse

from . import exceptions


async def user_already_existence_exception_handler(
    request: Request, exc: exceptions.UserAlreadyExistenceException
) -> JSONResponse:
    print("#PoorSimpleLoggerForOnlySamplePurpose:", exc)
    return JSONResponse(status_code=409, content={"detail": exc.detail})
