from ..application.services.user import CreationService as UserCreationService
from ..application.services.security import CreationService as AuthCreationService
from ..infrastructure.json_repository import JsonUserRepository


def generateUserCreationService() -> UserCreationService:
    return UserCreationService(user_repository=JsonUserRepository())


def generateAuthCreationService() -> AuthCreationService:
    return AuthCreationService()
