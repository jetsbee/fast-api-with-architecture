from typing import ClassVar, Literal

from pydantic import BaseModel

from .jwt import JWTModel, JWTType
from ...dependencies.jwt_factory import inject_jwt_impl_instance


class AuthModel(BaseModel):
    jwt_string: str
    jwt_type: Literal[JWTType.ACCESS, JWTType.REFRESH]
    __jwt_model: ClassVar[JWTModel] = inject_jwt_impl_instance()

    @classmethod
    def init(cls, username, jwt_type) -> BaseModel:
        token = cls.__jwt_model.create(username=username, jwt_type=jwt_type)

        return cls(jwt_string=token, jwt_type=jwt_type)
