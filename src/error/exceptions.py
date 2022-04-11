from typing import Optional

from fastapi.exceptions import RequestValidationError as RequestValidationError  # noqa
from starlette.exceptions import HTTPException as StarletteHTTPException  # noqa


class APIException(Exception):
    def __init__(
        self,
        exc: Optional[Exception] = None,
        msg: str = "Internal Server Error",
        detail: Optional[str] = None,
        status_code: int = 500,
        code: str = "000000",
    ) -> None:
        self.exc = exc
        self.msg = msg
        self.detail = detail
        self.status_code = status_code
        self.code = code

        # To use parent's __str__()
        super().__init__(
            {
                "exc": exc,
                "msg": msg,
                "detail": detail,
                "status_code": status_code,
                "code": code,
            }
        )
