from ..dto.user import UserIn
from ..dto.user import UserOut
from ...domain.repositories.user import UserRepository
from ...errors import UserAlreadyExistenceException


class CreationService:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    async def execute(self, user_in_dto: UserIn) -> UserOut:
        user = user_in_dto.to_model()
        user.encrypt_password()
        if self.user_repository.exists_by_username(user.username):
            raise UserAlreadyExistenceException(username=user.username)
        await self.user_repository.save(user)
        user_out_dto = UserOut.from_model_type(user)

        return user_out_dto
