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

    def verify_password(self, plain_password: str) -> bool:
        return UserModel.__pwd_context.verify(plain_password, self.hashed_password)

    @classmethod
    def __get_password_hash(cls, password: str) -> str:
        return cls.__pwd_context.hash(password)

    def encrypt_password(self) -> None:
        if self.password is None:
            raise Exception("Password not found.")

        self.hashed_password = self.__get_password_hash(self.password)
        self.__dispose_raw_password()

    def __dispose_raw_password(self) -> None:
        self.password = None
