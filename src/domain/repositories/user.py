from abc import ABC, abstractmethod

from ..models.user import UserModel


class UserRepository(ABC):
    @abstractmethod
    def save(self, user: UserModel) -> None:
        pass
