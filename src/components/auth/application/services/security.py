from ...application.dto.user import UserOut
from ...application.dto.auth import AuthOut

from ...domain.models.auth import AuthModel, JWTType


class CreationService:
    def execute(self, user_out_dto: UserOut) -> AuthOut:
        user = user_out_dto.to_model()
        access_auth = AuthModel.init(username=user.username, jwt_type=JWTType.ACCESS)
        refresh_auth = AuthModel.init(username=user.username, jwt_type=JWTType.REFRESH)
        auth_out_dto = AuthOut.from_model_type(access_auth, refresh_auth)

        return auth_out_dto
