from fastapi import BackgroundTasks

from ..application.services.user import CreationService as UserCreationService
from ..application.services.security import CreationService as AuthCreationService
from ..infrastructure.json_repository import JsonUserRepository


async def generate_user_creation_service(
    background_tasks: BackgroundTasks,
) -> UserCreationService:
    return UserCreationService(
        user_repository=await JsonUserRepository.async_init(),
        background_tasks=background_tasks,
    )


def generate_auth_creation_service() -> AuthCreationService:
    return AuthCreationService()
