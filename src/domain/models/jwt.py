from abc import ABC, abstractmethod


class JWTModel(ABC):
    @classmethod
    @abstractmethod
    def create(cls, username):
        pass

    @classmethod
    @abstractmethod
    def revoke(cls):
        pass

    @classmethod
    @abstractmethod
    def verify(cls):
        pass

    @classmethod
    @abstractmethod
    def renew(cls):
        pass
