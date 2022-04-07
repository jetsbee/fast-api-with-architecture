from pydantic import BaseModel

from ...domain.models.user import UserModel


class UserBase(BaseModel):
    username: str

    def to_model(self) -> UserModel:
        return UserModel(**self.dict())


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    hashed_password: str

    @classmethod
    def from_model_type(cls, user: UserModel) -> BaseModel:
        return cls(**user.dict())
