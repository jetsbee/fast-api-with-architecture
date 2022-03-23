from pydantic import BaseModel

from ...domain.models.auth import AuthModel


class AuthOut(BaseModel):
    access_jwt: str
    refresh_jwt: str
    type: str = "Bearer"

    @classmethod
    def fromModelType(
        cls, access_auth: AuthModel, refresh_auth: AuthModel, type="Bearer"
    ):
        return cls(
            access_jwt=access_auth.jwt_string,
            refresh_jwt=refresh_auth.jwt_string,
            type=type,
        )
