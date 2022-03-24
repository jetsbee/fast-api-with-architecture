from pydantic import BaseModel, Field

from ...domain.models.auth import AuthModel


class AuthOut(BaseModel):
    access_jwt: str
    refresh_jwt: str
    auth_type: str = Field("Bearer", alias="type")

    @classmethod
    def from_model_type(
        cls, access_auth: AuthModel, refresh_auth: AuthModel, auth_type: str = "Bearer"
    ) -> BaseModel:
        return cls(
            access_jwt=access_auth.jwt_string,
            refresh_jwt=refresh_auth.jwt_string,
            auth_type=auth_type,
        )
