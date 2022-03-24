from typing import ClassVar, Optional

from pydantic import BaseModel
from passlib.context import CryptContext


class UserModel(BaseModel):
    username: str
    password: Optional[str]
    hashed_password: Optional[str]
    __pwd_context: ClassVar[CryptContext] = CryptContext(
        schemes=["bcrypt"], deprecated="auto"
    )

    @classmethod
    def verify_password(cls, plain_password, hashed_password):
        return cls.__pwd_context.verify(plain_password, hashed_password)

    @classmethod
    def __get_password_hash(cls, password):
        return cls.__pwd_context.hash(password)

    def encrypt_password(self):
        if self.password is None:
            raise Exception("Password not found.")

        self.hashed_password = self.__get_password_hash(self.password)
        self.__dispose_raw_password()

    def __dispose_raw_password(self):
        self.password = None
