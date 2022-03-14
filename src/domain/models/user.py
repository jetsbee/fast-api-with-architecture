from typing import Optional

from pydantic import BaseModel


class UserModel(BaseModel):
    username: str
    password: Optional[str]
    hashed_password: Optional[str]

    def encrypt_password(self):
        if self.password is None:
            raise Exception("Password not found.")

        self.hashed_password = "!VERY_SECRET_PASSWORD!"
        self.__dispose_raw_password()

    def __dispose_raw_password(self):
        self.password = None
