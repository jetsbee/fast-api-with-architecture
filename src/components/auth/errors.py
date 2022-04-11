from typing import Optional
from fastapi import status
from ...error.exceptions import APIException


class UserAlreadyExistenceException(APIException):
    def __init__(self, username: str, exc: Optional[Exception] = None) -> None:
        super().__init__(
            exc=exc,
            msg="User already exists.",
            detail=f"User already exists with username: [{username}]",
            status_code=status.HTTP_409_CONFLICT,
            code=f"{status.HTTP_409_CONFLICT}{'1'.zfill(4)}",
        )
