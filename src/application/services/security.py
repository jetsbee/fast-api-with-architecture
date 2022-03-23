from ...application.dto.user import UserOut
from ...application.dto.auth import AuthOut

from ...domain.models.auth import AuthModel, AuthType


class CreationService:
    def __init__(self):
        pass

    def execute(self, user_out_dto: UserOut) -> AuthOut:
        user = user_out_dto.toModel()
        access_auth = AuthModel.init(username=user.username, type=AuthType.ACCESS)
        refresh_auth = AuthModel.init(username=user.username, type=AuthType.REFRESH)
        auth_out_dto = AuthOut.fromModelType(access_auth, refresh_auth)

        return auth_out_dto
