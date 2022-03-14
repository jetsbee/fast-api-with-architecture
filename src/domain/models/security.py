from typing import Literal

from enum import Enum

from pydantic import BaseModel


class AuthType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"


class AuthModel(BaseModel):
    jwt: str
    type: Literal[AuthType.ACCESS, AuthType.REFRESH]
    expires_in: int

    @classmethod
    def generateAuth(cls, username, type):
        jwt = f"{username}!@#$1234"
        expires_in = 20220314

        return cls(jwt=jwt, type=type, expires_in=expires_in)
