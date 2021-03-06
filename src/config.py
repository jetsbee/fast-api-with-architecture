import logging

from pathlib import Path
from functools import lru_cache

from pydantic import BaseSettings


class GlobalSettings(BaseSettings):
    ENV_STATE: str = "dev"
    # JWT
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRES: int = 30 * 60  # minutes
    REFRESH_TOKEN_EXPIRES: int = 15 * 86400  # days
    AUTH_HEADER_TYPE: str = "bearer"
    # End of JWT

    class Config:
        env_file = str(Path(__file__).resolve().parent / "env" / ".env")


class RequiredSettings(BaseSettings):
    # JWT
    SECRET_KEY: str
    # End of JWT
    LOG_LEVEL: int


class DevSettings(GlobalSettings, RequiredSettings):
    LOG_LEVEL: int = logging.INFO

    class Config:
        env_file = str(Path(__file__).resolve().parent / "env" / "dev.env")


class ProdSettings(GlobalSettings, RequiredSettings):
    LOG_LEVEL: int = logging.ERROR

    class Config:
        env_file = str(Path(__file__).resolve().parent / "env" / "prod.env")


class FactorySettings:
    @staticmethod
    def load():
        env_state = GlobalSettings().ENV_STATE
        if env_state == "dev":
            return DevSettings()
        elif env_state == "prod":
            return ProdSettings()
        else:
            raise Exception("Check the ENV_STATE.")


@lru_cache()
def get_settings():
    return FactorySettings.load()
