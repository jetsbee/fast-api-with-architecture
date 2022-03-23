from pydantic import BaseModel

from ...domain.models.user import UserModel


class UserBase(BaseModel):
    username: str


class UserIn(UserBase):
    password: str

    def to_model(self):
        return UserModel(**self.dict())


class UserOut(UserBase):
    hashed_password: str

    @classmethod
    def from_model_type(cls, user: UserModel):
        return cls(**user.dict())

    def to_model(self):
        return UserModel(**self.dict())
