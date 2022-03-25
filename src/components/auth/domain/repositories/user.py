from abc import ABC, abstractmethod

from ..models.user import UserModel


class UserRepository(ABC):
    @abstractmethod
    def save(self, user: UserModel) -> None:
        pass

    @abstractmethod
    def exists_by_username(self, username: str) -> bool:
        pass
