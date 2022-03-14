from fastapi import APIRouter, Depends, status

from ...application.dto.user import UserIn
from ...dependencies.services_factory import (
    generateUserCreationService,
    generateAuthCreationService,
)

router = APIRouter()


@router.post("/auth/signup/", status_code=status.HTTP_201_CREATED)
async def signup(
    user_in_dto: UserIn,
    user_creation_service=Depends(generateUserCreationService),
    auth_creation_service=Depends(generateAuthCreationService),
):
    user_out_dto = user_creation_service.execute(user_in_dto)
    auth_out_dto = auth_creation_service.execute(user_out_dto)

    return auth_out_dto


@router.post("/auth/login/")
async def login():
    # Todo: Implement
    return {"message": "Login working on it"}
