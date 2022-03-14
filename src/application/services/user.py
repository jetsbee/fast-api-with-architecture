from ..dto.user import UserIn
from ..dto.user import UserOut
from ...domain.repositories.user import UserRepository


class CreationService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, user_in_dto: UserIn) -> UserOut:
        user = user_in_dto.toModel()
        user.encrypt_password()
        self.user_repository.save(user)
        user_out_dto = UserOut.fromModelType(user)

        return user_out_dto
