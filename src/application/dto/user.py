from pydantic import BaseModel

from ...domain.models.user import UserModel


class UserBase(BaseModel):
    username: str


class UserIn(UserBase):
    password: str

    def toModel(self):
        return UserModel(**self.dict())


class UserOut(UserBase):
    hashed_password: str

    @classmethod
    def fromModelType(cls, user: UserModel):
        return cls(**user.dict())

    def toModel(self):
        return UserModel(**self.dict())
