from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str = "c175fcc672c7a6eb4fb53dcbd95b4e8d043018d54926e97badcfb4bd2642cbac"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRES: int = 30 * 60  # minutes
    REFRESH_TOKEN_EXPIRES: int = 15 * 86400  # days
    AUTH_HEADER_TYPE: str = "bearer"


@lru_cache()
def get_settings():
    return Settings()
