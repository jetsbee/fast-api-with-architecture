from pydantic import BaseSettings
from pydantic import BaseModel
from fastapi_jwt_auth import AuthJWT

from ..domain.models.jwt import JWTModel, JWTType


class Settings(BaseSettings):
    SECRET_KEY: str = "c175fcc672c7a6eb4fb53dcbd95b4e8d043018d54926e97badcfb4bd2642cbac"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRES: int = 30 * 60  # minutes
    REFRESH_TOKEN_EXPIRES: int = 15 * 86400  # days
    AUTH_HEADER_TYPE: str = "bearer"


settings = Settings()


class JwtSettings(BaseModel):
    authjwt_secret_key: str = settings.SECRET_KEY
    authjwt_algorithm: str = settings.ALGORITHM
    authjwt_access_token_expires: int = settings.ACCESS_TOKEN_EXPIRES
    authjwt_refresh_token_expires: int = settings.REFRESH_TOKEN_EXPIRES
    authjwt_header_type: str = settings.AUTH_HEADER_TYPE


@AuthJWT.load_config
def get_config():
    return JwtSettings()


class JWTImpl(JWTModel):
    __authorization: AuthJWT = AuthJWT()

    @classmethod
    def __create_token(cls, username: str, jwt_type: JWTType):
        token = None
        if jwt_type == JWTType.ACCESS:
            token = cls.__authorization.create_access_token(subject=username)
        elif jwt_type == JWTType.REFRESH:
            token = cls.__authorization.create_refresh_token(subject=username)

        return token

    @classmethod
    def create(cls, username: str, jwt_type: JWTType) -> str:
        super().create(username, jwt_type)  # Confirm parent's signiture

        token = cls.__create_token(username=username, jwt_type=jwt_type)

        return token

    @classmethod
    def revoke(cls):
        pass

    @classmethod
    def verify(cls):
        pass

    @classmethod
    def renew(cls):
        pass
