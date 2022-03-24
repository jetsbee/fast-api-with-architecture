from typing import ClassVar, Literal
from enum import Enum

from pydantic import BaseModel, PrivateAttr

from .jwt import JWTModel
from ...dependencies.jwt_factory import inject_jwt_impl_instance


class AuthType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"


class AuthModel(BaseModel):
    jwt_string: str
    type: Literal[AuthType.ACCESS, AuthType.REFRESH]
    expires_in: int
    __jwt_model: ClassVar[JWTModel] = inject_jwt_impl_instance()

    @classmethod
    def init(cls, username, type):
        jwt_string, expires_in = cls.__jwt_model.create(username)

        return cls(jwt_string=jwt_string, type=type, expires_in=expires_in)
