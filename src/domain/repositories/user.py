from abc import ABC, abstractmethod


class UserRepository(ABC):
    @abstractmethod
    def save(self):
        raise NotImplementedError("Method is not implemented in class.")
