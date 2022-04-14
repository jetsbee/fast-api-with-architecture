from fastapi import Depends, status

from ...application.dto.user import UserIn
from ...dependencies.services_factory import (
    generate_user_creation_service,
    generate_auth_creation_service,
)
from .....routing import router


@router.post("/auth/signup/", status_code=status.HTTP_201_CREATED)
def signup(
    user_in_dto: UserIn,
    user_creation_service=Depends(generate_user_creation_service),
    auth_creation_service=Depends(generate_auth_creation_service),
):
    user_out_dto = user_creation_service.execute(user_in_dto)
    auth_out_dto = auth_creation_service.execute(user_out_dto)

    return auth_out_dto


@router.post("/auth/login/")
async def login():
    # Todo: Implement
    return {"message": "Login working on it"}
