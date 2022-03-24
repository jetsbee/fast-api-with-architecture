from enum import Enum
from abc import ABC, abstractmethod


class JWTType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"


class JWTModel(ABC):
    @classmethod
    @abstractmethod
    def create(cls, username, jwt_type) -> str:
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
